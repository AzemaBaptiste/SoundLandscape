# -*- coding: utf-8 -*-
import time
import playsound
import pyproj
import requests
import pygame
import serial
import pynmea2

pygame.mixer.init()


class Runner(object):
    """Get the GPS information about a picture."""

    def __init__(self):
        """Initiator."""
        self.data = None
        self.GEOD = pyproj.Geod(ellps='WGS84')
        self.m_serial = serial.Serial("COM4", 4800)
        self.music_params = {
            'acousticness': 0.5, 'danceability': 0.5, 'energy': 0.5,
            'instrumentalness': 0.5, 'tempo': 80, 'country': 'FR',
            'valence': 0.5, 'popularity': 60, 'seed_genres': ['french']
        }

    def get_latlon_from_gps(self):
        """Read the latlon&time from the gps.

        :return: (list) lat, lon, datetime
        """
        data_line = self.m_serial.readline().decode()
        data = data_line.split(",")
        if data[0] == "$GPGGA":
            msg = pynmea2.parse(data_line)
            try:
                print(msg.latitude)
                print(msg.longitude)
                return msg
            except:
                return self.get_latlon_from_gps()
        else:
            return self.get_latlon_from_gps()

    @staticmethod
    def play_sound(key):
        """Play song based on the environment.

        :param key: (str) Env typ
        """
        if "stadium" in key:
            playsound.playsound("../references/psg.mp3", False)
            return None
        if "museum" in key:
            playsound.playsound("../references/museum.mp3", False)
            return None
        if "church" in key:
            playsound.playsound("../references/church.mp3", False)
            return None
        if "school" in key:
            playsound.playsound("../references/school.mp3", False)
            return None
        if "park" in key:
            playsound.playsound("../references/forest.mp3", False)
            return None
        if "forest" in key:
            playsound.playsound("../references/forest.mp3", False)
            return None
        if "water" in key:
            playsound.playsound("../references/water.mp3", False)
            return None

    @staticmethod
    def sound_to_play(dict_poi):
        """Define which sound to play based on poi.

        :param dict_poi: (dict) poi info
        :return: (str) sound key
        """
        l_sounds = []
        for k, v in dict_poi.items():
            if "stadium" in v[0]:
                l_sounds.append("stadium")
            if 'museum' in v[0]:
                l_sounds.append("museum")
            if "park" in v[0]:
                l_sounds.append("park")
            if "school" in v[0]:
                l_sounds.append("school")
            if "church" in v[0]:
                l_sounds.append("church")

        return l_sounds

    def compute_seed(self, data):
        """Find the current speed.

        :param data: (dict) data from gps photo
        :return: (int) speed
        """
        _, _, dist = self.GEOD.inv(
            data["longitude"], data["latitude"], self.data["longitude"], self.data["latitude"])
        t2 = sum([a * b for a, b in zip([3600, 60, 1], map(int, str(data["datetime"]).split(':')))])
        t1 = sum([a * b for a, b in zip([3600, 60, 1], map(int, str(self.data["datetime"]).split(':')))])

        return (dist / (t2-t1)) * 3.6

    @staticmethod
    def get_features(url, params):
        """Get features from url.

        :param url: (str) url api
        :param params: (dict) json request
        :return: (str) result from api
        """
        print(url)

        return requests.post('http://127.0.0.1:5000/api/' + url, json=params).json()['result']

    @staticmethod
    def get_img_features(url, data, headers):
        """Get features from image.

        :param url: (str) url api
        :param data: (str) image.content
        :param headers: (dict) header
        :return: (str) result from api
        """
        print(url)

        return requests.post('http://127.0.0.1:5000/api/' + url, data=data, headers=headers).json()['result']

    @staticmethod
    def get_music(music):
        """Take music which contains preview song.

        :param music: (dict) spotify results
        :return: (str) url
        """
        for t in music["tracks"]:
            res = t["preview_url"]
            if res:
                return res
        return "empty"

    @staticmethod
    def play_music_from_url(url):
        """Play song from spotify url.

        :param url: (str) url
        """
        r = requests.get(url, stream=True)
        pygame.mixer.music.load(r.raw)
        # pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def update_params(self, data):
        """Change dict value based on the env.

        :param data: (dict) env data
        """
        if not data["sound"]:
            data["sound"] = []
        if not data["sounds"]:
            data["sounds"] = []

        if "forest" in data["sound"] or "forest" in data["sounds"]:
            self.music_params["energy"] = 0.5
            self.music_params["valence"] = 0.5
        elif "water" in data["sound"] or "water" in data["sounds"]:
            self.music_params["energy"] = 0.8
            self.music_params["valence"] = 0.8
        else:
            self.music_params["energy"] = 0.7
            self.music_params["valence"] = 0.7

        if data["speed"] < 30:
            self.music_params["tempo"] = 50
        else:
            self.music_params["tempo"] = int(data["speed"] * 2)
            self.music_params["energy"] += 0.1

    def api_calls(self, gps):
        """Call all the api.

        :param gps: (gps.obj) gps values
        :return: (dict) data
        """
        latitude = gps.latitude
        longitude = gps.longitude
        #latitude = 48.840924
        #longitude = 2.251493
        #latitude = 48.861539
        #longitude = 2.339039
        params = {"latitude": latitude, "longitude": longitude}
        headers = {'content-type': 'image/jpeg'}
        data = dict()
        data["latitude"] = latitude
        data["longitude"] = longitude
        data["datetime"] = gps.timestamp
        if self.data:
            data["speed"] = self.compute_seed(data)
            data["speed"] = 0
        else:
            data["speed"] = 0
        data["weather"] = "Rainy"
        data["ratios"] = self.get_features("features/get_ratio_mask_from_latlon", params)
        data["sound"] = self.get_features("features/get_song_from_latlon", params)
        data["poi_information"] = self.get_features("features/get_interesting_poi_information_from_latlon", params)
        sun = self.get_features("features/get_sun_position_from_latlon", params)
        data["sunrise"] = sun["sunrise"]
        data["sunset"] = sun["sunset"]
        img_encoded = requests.post('http://127.0.0.1:5000/api/frame/get_camera_face')
        data["mood"] = self.get_img_features("mood/get_mood_from_image", img_encoded.content, headers)
        data["face"] = self.get_img_features("face/get_face_from_image", img_encoded.content, headers)
        img_encoded = requests.post('http://127.0.0.1:5000/api/frame/get_camera_front')
        data["landscape"] = self.get_img_features("landscape/get_landscape_from_image", img_encoded.content, headers)
        sounds = self.sound_to_play(data["poi_information"])
        sounds = sounds + [data["sound"]]
        if sounds:
            self.play_sound(sounds)
        try:
            self.music_params["seed_genres"] = self.get_features("music/get_driver_preferences", data["face"][0][0])
        except:
            self.music_params["seed_genres"] = self.get_features("music/get_driver_preferences", "julien")

        data["sounds"] = sounds
        self.update_params(data)
        music = self.get_features("music/get_recommendations", self.music_params)
        data["music"] = self.get_music(music)
        self.play_music_from_url(data["music"])
        print(self.music_params["seed_genres"])

        return data

    def run(self):
        """Run the application."""
        while True:
            print("check")
            gps = self.get_latlon_from_gps()
            self.data = self.api_calls(gps)
            print(self.data)
            time.sleep(5)


if __name__ == '__main__':
    print("Start ...")
    Runner().run()

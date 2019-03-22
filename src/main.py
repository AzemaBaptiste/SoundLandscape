# -*- coding: utf-8 -*-
import cv2
import time
import pyproj
import playsound
import requests
from GPSPhoto import gpsphoto

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Runner(FileSystemEventHandler):
    """Get the GPS information about a picture."""

    def __init__(self):
        """Initiator."""
        self.data = None
        self.GEOD = pyproj.Geod(ellps='WGS84')

    @staticmethod
    def play_sound(key):
        """Play song based on the environment.

        :param key: (str) Env typ
        """
        if "forest" in key:
            playsound.playsound("../references/forest.mp3", True)
        if "water" in key:
            playsound.playsound("../references/water.mp3", True)
        if "stadium" in key:
            playsound.playsound("../references/psg.mp3", True)
        if "museum" in key:
            playsound.playsound("../references/museum.mp3", True)

    @staticmethod
    def sound_to_play(dict_poi):
        """Define which sound to play based on poi.

        :param dict_poi: (dict) poi info
        :return: (str) sound key
        """
        for k, v in dict_poi.items():
            if "stadium" in v[0]:
                return "stadium"
            if 'museum' in v[0]:
                return "museum"

        return None

    def compute_seed(self, data):
        """Find the current speed.

        :param data: (dict) data from gps photo
        :return: (int) speed
        """
        _, _, dist = self.GEOD.inv(
            data["Longitude"], data["Latitude"], self.data["Longitude"], self.data["Latitude"])
        t2 = sum([a * b for a, b in zip([3600, 60, 1], map(int, data["UTC-Time"].split(':')))])
        t1 = sum([a * b for a, b in zip([3600, 60, 1], map(int, self.data["UTC-Time"].split(':')))])

        return (dist / (t2-t1)) * 3.6

    def on_created(self, event):
        """Save the lat&lon from the picture, at each new picture

        :param event: (Observer) the new file
        :return: (dict) save the lat, lon & datetime of the picture
        """
        # print(event.src_path)
        time.sleep(2)
        try:
            data = gpsphoto.getGPSData(event.src_path)
            if self.data:
                data["speed"] = self.compute_seed(data)
            latitude = data["Latitude"]
            longitude = data["Longitude"]
            self.data = data
            latitude = 48.840924
            longitude = 2.251493
            #latitude = 48.861539
            #longitude = 2.339039
            # response = requests.post(
            #    'http://127.0.0.1:5000/api/features/get_weather_from_latlon',
            #    json={"latitude": latitude, "longitude": longitude})
            # data["weather"] = response.json()["result"]
            data["weather"] = "Rainy"
            response = requests.post(
                'http://127.0.0.1:5000/api/features/get_ratio_mask_from_latlon',
                json={"latitude": latitude, "longitude": longitude})
            data["ratios"] = response.json()["result"]
            response = requests.post(
                'http://127.0.0.1:5000/api/features/get_song_from_latlon',
                json={"latitude": latitude, "longitude": longitude})
            data["sound"] = response.json()["result"]
            response = requests.post(
                'http://127.0.0.1:5000/api/features/get_sun_position_from_latlon',
                json={"latitude": latitude, "longitude": longitude})
            sun = response.json()["result"]
            data["sunrise"] = sun["sunrise"]
            data["sunset"] = sun["sunset"]
            response = requests.post(
                'http://127.0.0.1:5000/api/features/get_interesting_poi_information_from_latlon',
                json={"latitude": latitude, "longitude": longitude})
            data["poi_information"] = response.json()['result']
            headers = {'content-type': 'image/jpeg'}
            img_encoded = requests.post('http://127.0.0.1:5000/api/frame/get_camera_face')
            response = requests.post(
                'http://127.0.0.1:5000/api/mood/get_mood_from_image',
                data=img_encoded.content, headers=headers)
            data["mood"] = response.json()["result"]
            response = requests.post(
                'http://127.0.0.1:5000/api/face/get_face_from_image',
                data=img_encoded.content, headers=headers)
            data["face"] = response.json()["result"]
            img = cv2.imread(event.src_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            _, img_encoded = cv2.imencode('.jpg', img)
            response = requests.post(
                'http://127.0.0.1:5000/api/landscape/get_landscape_from_image',
                data=img_encoded.tostring(), headers=headers)
            data["landscape"] = response.json()["result"]
            print(data)
            sound = self.sound_to_play(data["poi_information"])
            if sound:
                self.play_sound(sound)
            if data["sound"]:
                self.play_sound(data["sound"])
        except Exception as e:
            print(event.src_path, e)


if __name__ == '__main__':
    print("Start ...")
    observer = Observer()
    event_handler = Runner()
    observer.schedule(event_handler, path="C:/Users/julie/Dropbox/Chargements appareil photo/")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

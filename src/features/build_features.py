# -*- coding: utf-8 -*-
import os
import cv2
import json
import requests
import datetime
import operator

import numpy as np
from PIL import Image
from googleplaces import GooglePlaces

from src import settings
from src.config.welcoming_sequence import WelcomingSequenceSettings


class Featuring(object):
    """Module to generate data information."""

    def __init__(self):
        """Initiator."""
        self.lng = 2.233111
        self.lat = 48.830446
        self.accuweather_key = settings.accuweather_key
        self.google_key = settings.google_key
        self.google_poi = GooglePlaces(self.google_key)
        self.welcome = WelcomingSequenceSettings()
        self.forest_lower = (180.0, 220.0, 170.0)
        self.forest_upper = (210.0, 240.0, 230.0)
        self.water_lower = (170.0, 200.0, 200.0)
        self.water_upper = (180.0, 220.0, 255.0)

    def get_image_mask(self, image):
        """Select only the image area which contains forest or water.

        :arg image: (PIL) image to analysis
        :return: (dict) np.array of the masks
        """
        return {
            "forest_mask": cv2.inRange(image, self.forest_lower, self.forest_upper),
            "water_mask": cv2.inRange(image, self.water_lower, self.water_upper)
        }

    @staticmethod
    def _compute_ratio(**kwargs):
        """Compute the ratio of forest & water."""
        ratios = dict()
        for arg in kwargs:
            ratios[arg + "_ratio"] = round(np.mean(kwargs[arg] != 0), 3)

        return ratios

    def get_ratio_percent_forest_water_from_picture(self, image):
        """Get ratio based on a gsp image.

        :param image: (np.array) image
        :return: (dict) ratios
        """
        masks = self.get_image_mask(image)

        return self._compute_ratio(**masks)

    def get_song_from_picture(self, image):
        """Get song based on a gsp image.

        :param image: (np.array) image
        :return: (str) kind of song
        """
        ratios = self.get_ratio_percent_forest_water_from_picture(image)
        max_key = max(ratios.items(), key=operator.itemgetter(1))[0]
        if ratios[max_key] > 0.2:
            return max_key
        else:
            return None

    @staticmethod
    def extract_value_from_web(url):
        """Get information from url.

        :param url: (str) url of the request
        :return: (str) content of the url
        """
        return json.loads(requests.get(url).content)

    def get_weather_from_position(self, lat, lng):
        """Get weather from the position using ACCUWEATHER.

        :param lat: (float) latitude
        :param lng: (float) longitude
        :return: (float) weather
        """
        base_url = "http://dataservice.accuweather.com"
        url = f"{base_url}/locations/v1/cities/geoposition/search?apikey={self.accuweather_key}&q={lat}%2C%20{lng}"
        key_id = self.extract_value_from_web(url)['Key']
        url2 = f"{base_url}/currentconditions/v1/{key_id}?apikey={self.accuweather_key}"

        return self.extract_value_from_web(url2)[0]["WeatherText"]

    def get_sun_position_time_from_position(self, lat, lng):
        """Get the sunrise and sunset based on lat, long & time.

        :param lat: (str) latitude
        :param lng: (str) longitude
        :return: (dict) sunrise time & sunset time
        """
        url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0'
        res = self.extract_value_from_web(url)
        sunrise_time = res['results']['sunrise']
        sunset_time = res['results']['sunset']
        now_time = datetime.datetime.now().isoformat()

        return {'time': now_time, 'sunrise': sunrise_time, 'sunset': sunset_time}

    @staticmethod
    def _interesting_poi(poi):
        """Check if we have a interesting poi for our needs.

        :arg poi: (google_places) poi
        :return: (bool) True if we've 1 or more good poi
        """
        list_poi = [
            'art_gallery', 'embassy', 'museum',
            'neighborhood', 'park', 'school'
        ]

        return bool(len(set(list_poi).intersection(set(poi.types))) > 0)

    def get_poi_from_position(self, lat, lng):
        """Get the poi around me.

        :param lat: (str) latitude
        :param lng: (str) longitude
        :return: (dict) all poi.name|poi.types
        """
        pois = self.google_poi.nearby_search(lat_lng={"lat": lat, "lng": lng}, radius=50)
        res = {}
        for poi in pois.places:
            res[poi.name] = poi.types

        return res

    def get_poi_information_from_position(self, lat, lng):
        """Select poi based on rules, and get their names and info about them.

        :param lat: (str) latitude
        :param lng: (str) longitude
        :return: (dict) poi name|information
        """
        pois = self.google_poi.nearby_search(lat_lng={"lat": lat, "lng": lng}, radius=50)
        dict_poi = dict()
        for poi in pois.places:
            if self._interesting_poi(poi):
                dict_poi[poi.name] = self.welcome.information_about_poi(poi)

        if bool(dict_poi):
            return dict_poi
        return "None"


if __name__ == '__main__':
    obj = Featuring()
    img_path = os.path.join(settings.IMAGE_GPS_PATH, "48.8584+2.29466.jpg")
    np_img = np.asarray(Image.open(img_path))
    ratios = obj.get_ratio_percent_forest_water_from_picture(np_img)
    print("ratio:", ratios)
    song = obj.get_song_from_picture(np_img)
    print("song:", song)
    poi = obj.get_poi_from_position(obj.lat, obj.lng)
    for point in poi.places:
        print("poi:", point.name)
    poi = obj.get_poi_information_from_position(obj.lat, obj.lng)
    print("Information poi:", poi)
    sun_position = obj.get_sun_position_time_from_position(obj.lat, obj.lng)
    print(sun_position)
    weather = obj.get_weather_from_position(obj.lat, obj.lng)
    print("weather:", weather)

# -*- coding: utf-8 -*-
import json
import requests

from dateutil import parser

from src import settings


class Featuring(object):
    """Module to generate data information."""

    def __init__(self):
        """Initiator."""
        self.lng = 2.233111
        self.lat = 48.830446
        self.accuweather_key = settings.accuweather_key

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

        return self.extract_value_from_web(url2)[0]["weather"]

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
        now_time = parser.parse(res.headers['Date']).isoformat()

        return {'time': now_time, 'sunrise': sunrise_time, 'sunset': sunset_time}

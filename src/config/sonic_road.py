# -*- coding: utf-8 -*-
import json
import math
import bisect
import datetime
import spotipy
import pandas as pd

from dateutil import parser
import spotipy.oauth2 as oauth2

from src import settings


class SonicRoadSettings(object):
    """Some utils function for SonicRoad."""

    def __init__(self):
        """Initiator."""
        self.credentials = oauth2.SpotifyClientCredentials(
            client_id=settings.spotify_id,
            client_secret=settings.spotify_pwd
        )
        self.schema = {
            'variable': str,
            'value': str,
            'target_acousticness': float,
            'target_energy': float,
            'target_loudness': float,
            'target_liveness': float,
            'target_danceability':float,
            'target_instrumentalness': float,
            'target_valence': float,
            'seed_genres': str
        }
        self.rules = self.get_dict_config(settings.RULES_PATH, self.schema)
        self.mood_preferences = ""
        self.driver_genre_preferences = ""

    @staticmethod
    def get_dict_config(config_filepath, schema):
        """Parse the csv file to get a correct config file in python dict type.

        :param config_filepath: (str) the filepath to the meta rule python dict
        :param schema: (dict) file schema
        :return: (dict) python config file dictionary
        """
        rule_dataframe = pd.read_csv(config_filepath, sep=";", dtype=schema, na_values="")
        rule_dataframe.seed_genres = rule_dataframe.seed_genres.str.split("/")

        grouped_rule_dataframe = rule_dataframe.groupby(["variable"])
        params = {}

        for k, v in grouped_rule_dataframe.indices.items():
            tmp_dict = {}
            for i in v:
                row = rule_dataframe.iloc[i]
                value = row.value
                update_dict = {
                    "target_acousticness": float(row.target_acousticness),
                    "target_energy": float(row.target_energy),
                    "target_danceability": float(row.target_danceability),
                    "target_instrumentalness": float(row.target_instrumentalness),
                    "target_valence": float(row.target_valence),
                    "target_loudness": float(row.target_loudness),
                    "target_liveness": float(row.target_liveness)
                }
                if not type(row.seed_genres) == float:
                    update_dict["seed_genres"] = row.seed_genres
                tmp_dict.update({value: update_dict})
            params.update({k: tmp_dict})

        return params

    def add_config_dict(self, dict_to_add):
        """Adds a dictionary to base one. The parameters are added to the base dict.

        :param dict_to_add: (dict) dict to add
        :return: (dict) a resulting dictionary that is made with the following rules
        """
        for variable, d in dict_to_add.items():
            for value, dd in d.items():
                for param, param_value in dd.items():
                    base_value = self.rules[variable][value][param]
                    try:
                        self.rules[variable][value][param] = base_value + param_value
                    finally:
                        pass

        return self.rules

    @staticmethod
    def sigmoid_from_speed(speed, min, max, neutral_speed):
        """This is the energy function based on speed (the smooth coeff 0.1 is for now fixed).

        :param speed: (float) speed from the api
        :param min: (float) the - inf asymptote of the sigmoid
        :param max: (float) the + inf asymptote of the sigmoid
        :param neutral_speed: (float) the offset put to the function to get 0 energy at this speed
        :return: (float) the deducted energy from the speed based on laurent expertise
        """
        offset = 10 * math.log((min - max) / min - 1) + neutral_speed

        return (max - min) / (1 + math.exp(-0.1 * (speed - offset))) + min

    @staticmethod
    def min_tempo_from_speed(speed):
        """Get min_tempo from speed.

        :param speed: (float) speed of the car
        :return: (float) the min_tempo deducted
        """
        if speed < 100:
            return 0
        else:
            return speed * 2 - 80

    def category_from_now_sunset_sunrise_time(self, **kwargs):
        """Get category (among night, afternoon, morning, sunset, sunrise) based on sunset, sunrise and now time.

        :param now_time: (datetime) local time in str ex : 2019-02-06T07:13:15+00:00
        :param sunrise_time: (datetime) local sunrise time in str ex : 2019-02-06T07:13:15+00:00
        :param sunset_time: (datetime) local sunset time in str ex : 2019-02-06T07:13:15+00:00
        :return: (str) night, afternoon, morning, sunset or sunrise
        """
        now_time = parser.parse(kwargs["now_time"])
        sunrise_time = parser.parse(kwargs["sunrise_time"])
        sunset_time = parser.parse(kwargs["sunset_time"])
        noon_time = now_time.replace(hour=12, minute=0, second=0)

        sunrise_time_start = sunrise_time - datetime.timedelta(minutes=15)
        sunrise_time_end = sunrise_time + datetime.timedelta(minutes=15)
        sunset_time_start = sunset_time - datetime.timedelta(minutes=15)
        sunset_time_end = sunset_time + datetime.timedelta(minutes=15)

        time_seq = [sunrise_time_start, sunrise_time_end, noon_time, sunset_time_start, sunset_time_end]
        bisect_index = bisect.bisect_left(time_seq, now_time)
        categories = ["night", "sunrise", "morning", "afternoon", "sunset", "night"]

        return self.rules["day/night"][categories[bisect_index]]

    def load_user_preferences(self, driver):
        """Load user preferences.

        :arg driver: (str) driver name
        :return: (dict) read user preferences
        """
        with open(settings.USER_PREFERENCES_PATH) as f:
            driver_genre_preferences = json.load(f)
        self.driver_genre_preferences = driver_genre_preferences[driver]

        return self.driver_genre_preferences

    def load_mood_preferences(self, mood):
        """Load user preferences.

        :arg mood: (str) mood
        :return: (dict) read user preferences
        """
        return self.rules["mood"][mood]

    def get_recommendations_from_params(self, params):
        """Get spotify recommendations.

        :return: (str) URL of mp3 preview of the recommended song
        """
        token = self.credentials.get_access_token()
        spotify = spotipy.Spotify(auth=token)
        # import pdb; pdb.set_trace()

        return spotify.recommendations(limit=50, **params)

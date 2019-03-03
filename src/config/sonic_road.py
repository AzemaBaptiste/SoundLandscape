# -*- coding: utf-8 -*-
import math
import bisect
import datetime
import pandas as pd

from dateutil import parser


def get_dict_config(config_filepath, schema):
    """Parse the csv file to get a correct config file in python dict type.

    :param config_filepath: (str) the filepath to the meta rule python dict
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
            update_dict = {"target_acousticness": float(row.target_acousticness),
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


def add_config_dict(base_dict, dict_to_add):
    """Adds a dictionary to base one. The parameters are added to the base dict.

    :param base_dict: (dict) base dict
    :param dict_to_add: (dict) dict to add
    :return: (dict) a resulting dictionary that is made with the following rules
    """
    for variable, d in dict_to_add.items():
        for value, dd in d.items():
            for param, param_value in dd.items():
                base_value = base_dict[variable][value][param]
                try:
                    base_dict[variable][value][param] = base_value + param_value
                finally:
                    pass

    return base_dict


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


def min_tempo_from_speed(speed):
    """Get min_tempo from speed.

    :param speed: (float) speed of the car
    :return: (float) the min_tempo deducted
    """
    if speed < 100:
        return 0
    else:
        return speed * 2 - 80


def category_from_now_sunset_sunrise_time(now_time, sunrise_time, sunset_time):
    """Get category (among night, afternoon, morning, sunset, sunrise) based on sunset, sunrise and now time.

    :param now_time: (datetime) local time in str ex : 2019-02-06T07:13:15+00:00
    :param sunrise_time: (datetime) local sunrise time in str ex : 2019-02-06T07:13:15+00:00
    :param sunset_time: (datetime) local sunset time in str ex : 2019-02-06T07:13:15+00:00
    :return: (str) night, afternoon, morning, sunset or sunrise
    """
    now_time = parser.parse(now_time)
    sunrise_time = parser.parse(sunrise_time)
    sunset_time = parser.parse(sunset_time)
    noon_time = now_time.replace(hour=12, minute=0, second=0)

    sunrise_time_start = sunrise_time - datetime.timedelta(minutes=15)
    sunrise_time_end = sunrise_time + datetime.timedelta(minutes=15)
    sunset_time_start = sunset_time - datetime.timedelta(minutes=15)
    sunset_time_end = sunset_time + datetime.timedelta(minutes=15)

    time_seq = [sunrise_time_start, sunrise_time_end, noon_time, sunset_time_start, sunset_time_end]
    bisect_index = bisect.bisect_left(time_seq, now_time)
    categories = ["night", "sunrise", "morning", "afternoon", "sunset", "night"]

    return categories[bisect_index]

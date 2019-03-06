# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request

from src.webservice import status
from src.features.build_features import Featuring
from src.data.google_maps_images import GoogleImages

FEATURES_APP = Blueprint('features_app', __name__)
FEATURING = Featuring()
GOOGLE = GoogleImages()


@FEATURES_APP.route("/api/features/get_weather_from_latlon", methods=["POST", "GET"])
def get_weather_from_latlon():
    """Get the weather from the lat lng.

    :return: (str) weather type
    """
    res = json.loads(request.data)
    lat = res["latitude"]
    lng = res["longitude"]

    return status.get_resource(FEATURING.get_weather_from_position(lat, lng))


@FEATURES_APP.route("/api/features/get_ratio_mask_from_latlon", methods=["POST", "GET"])
def get_ratio_mask_from_latlon():
    """Get mask ration from lat lng.

    :return: (dict) ratios mask
    """
    res = json.loads(request.data)
    lat = res["latitude"]
    lng = res["longitude"]
    img = GOOGLE.image_gps(lat, lng)

    return status.get_resource(FEATURING.get_ratio_percent_forest_water_from_picture(img))


@FEATURES_APP.route("/api/features/get_song_from_latlon", methods=["POST", "GET"])
def get_song_from_latlon():
    """Get mask ration from lat lng.

    :return: (dict) ratios mask
    """
    res = json.loads(request.data)
    lat = res["latitude"]
    lng = res["longitude"]
    img = GOOGLE.image_gps(lat, lng)

    return status.get_resource(FEATURING.get_song_from_picture(img))


@FEATURES_APP.route("/api/features/get_sun_position_from_latlon", methods=["POST", "GET"])
def get_sun_position_from_latlon():
    """Get sun' position from latlon.

    :return: (dict) sunset & sunrise
    """
    res = json.loads(request.data)
    lat = res["latitude"]
    lng = res["longitude"]

    return status.get_resource(FEATURING.get_sun_position_time_from_position(lat, lng))


@FEATURES_APP.route("/api/features/get_all_poi_from_latlon", methods=["POST", "GET"])
def get_all_poi_from_latlon():
    """Get all poi around me.

    :return: (google_place.places) Don't use it, return complex obj
    """
    res = json.loads(request.data)
    lat = res["latitude"]
    lng = res["longitude"]

    return status.get_resource(FEATURING.get_poi_from_position(lat, lng))


@FEATURES_APP.route("/api/features/get_interesting_poi_information_from_latlon", methods=["POST", "GET"])
def get_interesting_poi_information_from_latlon():
    """Get information about some poi.

    :return: (dict) poi name|information
    """
    res = json.loads(request.data)
    lat = res["latitude"]
    lng = res["longitude"]

    return status.get_resource(FEATURING.get_poi_information_from_position(lat, lng))

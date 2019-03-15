# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request

from src.config.sonic_road import SonicRoadSettings
from src.webservice import status

MUSIC_APP = Blueprint('music_app', __name__)
SONICROAD = SonicRoadSettings()


@MUSIC_APP.route("/api/music/get_params", methods=["POST", "GET"])
def get_params():
    """Get the spotify params.

    :return: (dict) spotify params
    """
    return status.get_resource(SONICROAD.rules)


@MUSIC_APP.route("/api/music/get_recommendations", methods=["POST", "GET"])
def get_recommendations():
    """Get spotify get_recommendations.

    :return: (dict) spotify get_recommendations
    """
    params = json.loads(request.data)

    return status.get_resource(SONICROAD.get_recommendations_from_params(**params))


@MUSIC_APP.route("/api/music/update_params", methods=["POST", "GET"])
def update_params():
    """Update the params with new params.

    :return: (dict) spotify params
    """
    new_params = json.loads(request.data)

    return status.get_resource(SONICROAD.add_config_dict(new_params))


@MUSIC_APP.route("/api/music/get_day_time", methods=["POST", "GET"])
def get_day_time():
    """Get category over (among night, afternoon, morning, sunset, sunrise).

    :return: (str) day time
    """
    day_time = json.loads(request.data)

    return status.get_resource(SONICROAD.category_from_now_sunset_sunrise_time(**day_time))


@MUSIC_APP.route("/api/music/get_driver_preferences", methods=["POST", "GET"])
def get_driver_preferences():
    """Get driver preferences.

    :return: (list) driver preferences
    """
    driver = request.data

    return status.get_resource(SONICROAD.load_user_preferences(driver))


@MUSIC_APP.route("/api/music/get_speed_energy", methods=["POST", "GET"])
def get_speed_energy():
    """Get target_energy based on speed.

    :return: (dict) energy target
    """
    speed = request.data

    return status.get_resource(({'target_energy': SONICROAD.sigmoid_from_speed(speed, -0.1, 0.4, 50)}))


@MUSIC_APP.route("/api/music/get_mood", methods=["POST", "GET"])
def get_mood():
    """Get mood update params.

    :return: (dict) params update
    """
    mood = request.data

    return status.get_resource(SONICROAD.load_mood_preferences(mood))

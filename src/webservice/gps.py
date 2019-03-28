# -*- coding: utf-8 -*-
from flask import Blueprint

from src.webservice import status
from src.data.gps_data import GPSInfo

GPS_APP = Blueprint('gps_app', __name__)
GPS = GPSInfo("COM5")


@GPS_APP.route("/api/gps/get_latlon", methods=["POST", "GET"])
def get_latlon():
    """Get latlon from gps.

    :return: (dict) latlon
    """
    return status.get_resource(GPS.get_latlon_from_gps())


@GPS_APP.route("/api/gps/get_speed", methods=["POST", "GET"])
def get_speed():
    """Get speed from gps.

    :return: (dict) speed
    """
    return status.get_resource(GPS.get_speed_from_gps())

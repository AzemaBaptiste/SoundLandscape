# -*- coding: utf-8 -*-
from flask import Blueprint

from src.config.sonic_road import SonicRoadSettings

MUSIC_APP = Blueprint('music_app', __name__)
SONICROAD = SonicRoadSettings()


@MUSIC_APP.route("/api/music/get_params", methods=["POST", "GET"])
def get_params():
    """Get the spotify params.

    :return: (dict) spotify params
    """
    pass

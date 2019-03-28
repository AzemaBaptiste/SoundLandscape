# -*- coding: utf-8 -*-
import json
import pygame
import requests
import playsound

import numpy as np

from flask import Blueprint, request
from src.webservice import status

PLAYER_APP = Blueprint('player_app', __name__)
pygame.mixer.init()


@PLAYER_APP.route("/api/player/play_sound", methods=["POST", "GET"])
def play_sound():
    """Play song based on the environment."""
    key = json.loads(request.data)
    if "stadium" in key:
        playsound.playsound("../../references/psg.mp3", False)
        return None
    if "museum" in key:
        playsound.playsound("../../references/museum.mp3", False)
        return None
    if "church" in key:
        playsound.playsound("../../references/church.mp3", False)
        return None
    if "school" in key:
        playsound.playsound("../../references/school.mp3", False)
        return None
    if "park" in key:
        playsound.playsound("../../references/forest.mp3", False)
        return None
    if "forest" in key:
        playsound.playsound("../../references/forest.mp3", False)
        return None
    if "water" in key:
        playsound.playsound("../../references/water.mp3", False)
        return None


@PLAYER_APP.route("/api/player/sound_to_play", methods=["POST", "GET"])
def sound_to_play():
    """Define which sound to play based on poi.

    :return: (list) sound key
    """
    dict_poi = json.loads(request.data)
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

    return status.get_resource(l_sounds)


@PLAYER_APP.route("/api/player/select_music_to_play", methods=["POST", "GET"])
def select_music_to_play(music):
    """Take music which contains preview song. Take it based on weighted random choice

    :param music: (dict) spotify results
    :return: (str) url
    """
    dmusic = {"empty": "empty"}
    for idx, t in enumerate(music["tracks"][::-1]):
        res = t["preview_url"]
        if res:
            dmusic[t] = idx + 1

    p = [x/sum(dmusic.values()) for x in dmusic.values()]

    return np.random.choice(list(dmusic.keys()), 1, p=p)


@PLAYER_APP.route("/api/player/play_music_from_url", methods=["POST", "GET"])
def play_music_from_url(url):
    """Play song from spotify url.

    :param url: (str) url
    """
    r = requests.get(url, stream=True)
    pygame.mixer.music.load(r.raw)
    pygame.mixer.music.play()

# -*- coding: utf-8 -*-
import base64
import json
import cv2

from flask import Blueprint, request

import numpy as np

from src.webservice import status
from src.models.predict_model import PredictMood

MOOD_APP = Blueprint('mood_app', __name__)
MOOD_MODEL = PredictMood()


@MOOD_APP.route("/api/mood/get_mood_from_image", methods=["POST", "GET"])
def get_mood_from_image():
    """Get the mood from a picture.

    :return: (src) mood
    """
    try:
        data = base64.b64decode(json.loads(request.data.decode())["data"])
    except Exception as _:
        data = base64.b64decode(json.loads(request.content.decode())["data"])

    img_array = np.fromstring(data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return status.get_resource(MOOD_MODEL.predict(img))

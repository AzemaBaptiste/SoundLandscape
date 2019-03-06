# -*- coding: utf-8 -*-
import cv2

from flask import Blueprint, request

import numpy as np

from src.webservice import status
from src.models.predict_model import PredictLandscape

LANDSCAPE_APP = Blueprint('landscape_app', __name__)
LANDSCAPE_MODEL = PredictLandscape()


@LANDSCAPE_APP.route("/api/landscape/get_landscape_from_image", methods=["POST", "GET"])
def get_landscape_from_image():
    """Get the landscape from a picture.

    :return: (src) landscape
    """
    try:
        data = request.data
    except Exception as _:
        data = request.content
    img = np.fromstring(data, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    return status.get_resource(LANDSCAPE_MODEL.predict(img))

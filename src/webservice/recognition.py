# -*- coding: utf-8 -*-
import base64
import json

import cv2

from flask import Blueprint, request

import numpy as np

from src.webservice import status
from src.models.predict_model import PredictFace

FACE_APP = Blueprint('face_app', __name__)
FACE_MODEL = PredictFace()


@FACE_APP.route("/api/face/get_face_from_image", methods=["POST", "GET"])
def get_face_from_image():
    """Get the face'name from a picture.

    :return: (src) face'name
    """
    try:
        data = base64.b64decode(json.loads(request.data.decode())["data"])
    except Exception as _:
        data = base64.b64decode(json.loads(request.content.decode())["data"])
    img = np.fromstring(data, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    return status.get_resource(FACE_MODEL.predict(img))

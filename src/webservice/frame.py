# -*- coding: utf-8 -*-
import base64

import cv2

from flask import Blueprint, send_file, make_response

from src.data.webcam_images import VideoCamera

CAMERA_APP = Blueprint('camera_app', __name__)


@CAMERA_APP.route("/api/frame/get_camera_face", methods=["POST", "GET"])
def get_camera_face():
    """Get the weather from the lat lng.

    :return: (str) weather type
    """
    CAMERA_FACE = VideoCamera(0)
    frame = CAMERA_FACE.get_frame()
    _, img_encoded = cv2.imencode('.jpg', frame)
    CAMERA_FACE.__del__()

    jpg_as_text = base64.b64encode(img_encoded)

    return jpg_as_text

@CAMERA_APP.route("/api/frame/get_camera_front", methods=["POST", "GET"])
def get_camera_front():
    """Get the weather from the lat lng.

    :return: (str) weather type
    """
    CAMERA_FRONT = VideoCamera(1)
    frame = CAMERA_FRONT.get_frame()
    _, img_encoded = cv2.imencode('.jpg', frame)
    CAMERA_FRONT.__del__()

    jpg_as_text = base64.b64encode(img_encoded)

    return jpg_as_text

# -*- coding: utf-8 -*-
import cv2

from flask import Blueprint

from src.webservice import status
from src.data.webcam_images import VideoCamera

CAMERA_APP = Blueprint('camera_app', __name__)
CAMERA_FACE = VideoCamera(0)
CAMERA_FRONT = VideoCamera(1)


@CAMERA_APP.route("/api/frame/get_camera_face", methods=["POST", "GET"])
def get_camera_face():
    """Get the weather from the lat lng.

    :return: (str) weather type
    """
    frame = CAMERA_FACE.get_frame()
    _, img_encoded = cv2.imencode('.jpg', frame)
    CAMERA_FACE.__del__()

    return status.get_resource(img_encoded.tostring())


@CAMERA_APP.route("/api/frame/get_camera_front", methods=["POST", "GET"])
def get_camera_front():
    """Get the weather from the lat lng.

    :return: (str) weather type
    """
    frame = CAMERA_FRONT.get_frame()
    _, img_encoded = cv2.imencode('.jpg', frame)
    CAMERA_FRONT.__del__()

    return status.get_resource(img_encoded.tostring())

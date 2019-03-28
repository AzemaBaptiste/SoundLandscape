# -*- coding: utf-8 -*-
import cv2

from flask import Blueprint

from src.data.webcam_images import VideoCamera

CAMERA_APP = Blueprint('camera_app', __name__)


@CAMERA_APP.route("/api/frame/get_camera_face", methods=["POST", "GET"])
def get_camera_face():
    """Get img from face.

    :return: (str) face image
    """
    CAMERA_FACE = VideoCamera(0)
    frame = CAMERA_FACE.get_frame()
    _, img_encoded = cv2.imencode('.jpg', frame)
    CAMERA_FACE.__del__()

    return img_encoded.tostring()


@CAMERA_APP.route("/api/frame/get_camera_front", methods=["POST", "GET"])
def get_camera_front():
    """Get img from front.

    :return: (str) front image
    """
    CAMERA_FRONT = VideoCamera(1)
    frame = CAMERA_FRONT.get_frame()
    _, img_encoded = cv2.imencode('.jpg', frame)
    CAMERA_FRONT.__del__()

    return img_encoded.tostring()

# -*- coding: utf-8 -*-
import sys
import flask

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_dir))

from src.webservice.features import FEATURES_APP
from src.webservice.landscape import LANDSCAPE_APP
from src.webservice.mood import MOOD_APP
from src.webservice.recognition import FACE_APP
from src.webservice.frame import CAMERA_APP


if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.register_blueprint(FACE_APP)
    app.register_blueprint(MOOD_APP)
    app.register_blueprint(LANDSCAPE_APP)
    app.register_blueprint(FEATURES_APP)
    app.register_blueprint(CAMERA_APP)
    app.run(host="127.0.0.1", port=5000, threaded=False)

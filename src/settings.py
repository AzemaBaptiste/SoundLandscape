# -*- coding: utf-8 -*-
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_STREET_PATH = os.path.join(PROJECT_DIR, "data", "raw", "streetview")
IMAGE_GPS_PATH = os.path.join(PROJECT_DIR, "data", "raw", "gps")
IMAGE_FACE_PATH = os.path.join(PROJECT_DIR, "data", "raw", "faces")

LAND_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "landscape_model.h5")
MOOD_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "mood_model.h5")
FACE_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "face_model.p")
ENCO_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "face_encoding.p")
NAME_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "face_names.p")

accuweather_key = os.environ.get("accuweathher_api_key")
google_key = os.environ.get("google_key")
spotify_id = os.environ.get("spotify_id")
spotify_pwd = os.environ.get("spotify_pwd")

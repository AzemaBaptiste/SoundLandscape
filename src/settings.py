# -*- coding: utf-8 -*-
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_STREET_PATH = os.path.join(PROJECT_DIR, "data", "raw", "streetview")
IMAGE_GPS_PATH = os.path.join(PROJECT_DIR, "data", "raw", "gps")
IMAGE_FACE_PATH = os.path.join(PROJECT_DIR, "data", "raw", "faces")

MOOD_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "mood_model.h5")
LAND_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "land_model.h5")
LAND_ARCHI_PATH = os.path.join(PROJECT_DIR, "models", "land_architecture.json")
FACE_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "face_model.p")
ENCO_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "face_encoding.p")
NAME_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "face_names.p")

accuweather_key = os.environ.get("accuweathher_api_key")
google_key = os.environ.get("google_key")
spotify_id = os.environ.get("spotify_id")
spotify_pwd = os.environ.get("spotify_pwd")

RULES_PATH = os.path.join(PROJECT_DIR, "references", "settings.csv")
USER_PREFERENCES_PATH = os.path.join(PROJECT_DIR, "references", "user_preferences.json")
MOOD_PREFERENCES_PATH = os.path.join(PROJECT_DIR, "references", "mood_preferences.json")

lat_lon = os.path.join(PROJECT_DIR, "data", "raw", "settings.json")

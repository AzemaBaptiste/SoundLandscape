# -*- coding: utf-8 -*-
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


PROJECT_DIR = Path(__file__).resolve().parents[1]
IMAGE_STREET_PATH = os.path.join(PROJECT_DIR, "data", "raw", "streetview")
IMAGE_GPS_PATH = os.path.join(PROJECT_DIR, "data", "raw", "gps")

LAND_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "landscape_model.h5")
MOOD_MODEL_PATH = os.path.join(PROJECT_DIR, "models", "mood_model.h5")

accuweather_key = os.environ.get("accuweathher_api_key")
google_key = os.environ.get("google_key")

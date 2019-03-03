# -*- coding: utf-8 -*-
import keras

from src import settings


class PredictMood(object):
    """."""

    def __init__(self):
        """."""
        self.model = keras.models.load_model(settings.MOOD_MODEL_PATH)


class PredictLandscape(object):
    """."""

    def __init__(self):
        """."""
        self.model = keras.models.load_model(settings.LAND_MODEL_PATH)

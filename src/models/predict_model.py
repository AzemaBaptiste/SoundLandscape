# -*- coding: utf-8 -*-
import cv2
import pickle

from PIL import Image

import face_recognition
import numpy as np
import keras

from src import settings
# from src.models.train_model import TrainFaceDetector


class PredictFace(object):
    """Predict face based on a picture."""

    def __init__(self):
        """Initiator."""
        self.face_encoding = pickle.load(open(settings.ENCO_MODEL_PATH, "rb"))
        self.face_name = pickle.load(open(settings.NAME_MODEL_PATH, "rb"))

    def predict(self, image):
        """Predict the location and the name of people in the image.

        :param image: (np.array) image in gray
        :return: (list) (list) names & locations
        """
        if not isinstance(image, np.ndarray):
            image = np.asarray(image, dtype=np.uint8)
        image.setflags(write=True)
        names = list()
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)
        for encoding in encodings:
            matches = face_recognition.compare_faces(self.face_encoding, encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.face_name[first_match_index]
            names.append(name)

        return names, locations


class PredictMood(object):
    """Module to predict the mood based on a picture."""

    def __init__(self):
        """Initiator."""
        self.model = keras.models.load_model(settings.MOOD_MODEL_PATH)
        self.mood_classes = {
            0: 'angry', 1: 'disgust', 2: 'fear',
            3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprised'
        }

    @staticmethod
    def crop_face(img):
        """Crop image to select only the face, but works only for the 1 person.

        :param img: (np.array) image
        :return: (np.array) image cropped
        """
        top, right, bottom, left = face_recognition.face_locations(img)[0]

        return img[top:bottom, left:right]

    def process_img(self, img):
        """Transform image to go through the deep architecture.

        :param img: (PIL.image) image
        :return: (np.array) image processed
        """
        if not isinstance(img, np.ndarray):
            img = np.asarray(img, dtype=np.uint8)
        img.setflags(write=True)
        try:
            crop_img = self.crop_face(img)
        except Exception as _:
            crop_img = img
        resized = cv2.resize(crop_img, (71, 71))
        resized_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        resized_gray = resized_gray[np.newaxis, :, :, np.newaxis]
        resized_gray_scale = resized_gray / 255.0

        return resized_gray_scale

    def predict(self, img):
        """Predict the mood based on a picture.

        :param img: (PIL.image) image
        :return: (str) mood
        """
        processed_img = self.process_img(img)
        mood_index = np.argmax(self.model.predict(processed_img))

        return self.mood_classes[mood_index]


class PredictLandscape(object):
    """Predict landscape based on a picture."""

    def __init__(self):
        """Initiator."""
        self.model = keras.models.load_model(settings.LAND_MODEL_PATH)
        self.landscape_classes = {
            0: "city", 1: "field", 2: "forest", 3: "lake",
            4: "mountain", 5: "ocean", 6: "road"
        }

    @staticmethod
    def process_img(img):
        """Transform image to go through the deep architecture.

        :param img: (PIL.image) image
        :return: (np.array) image processed
        """
        if not isinstance(img, np.ndarray):
            img = np.asarray(img, dtype=np.uint8)
        img.setflags(write=True)
        resized = cv2.resize(img, (224, 224))
        resized_rgb = resized[np.newaxis, :, :]
        resized_rgb_scale = resized_rgb / 255.0

        return resized_rgb_scale

    def predict(self, img):
        """Predict the landscape based on a picture.

        :param img: (PIL.image) image
        :return: (str) landscape
        """
        processed_img = self.process_img(img)
        landscape_index = np.argmax(self.model.predict(processed_img))

        return self.landscape_classes[landscape_index]


if __name__ == '__main__':
    model_landscape = PredictLandscape()
    im = Image.open("C:/Users/julie/PycharmProjects/SoundLandscape/data/raw/landscape/forest.jpg")
    landscape = model_landscape.predict(im)
    print(landscape)

    model_mood = PredictMood()
    im = Image.open("C:/Users/julie/PycharmProjects/SoundLandscape/data/raw/mood/happy.jpg")
    mood = model_mood.predict(im)
    print(mood)

    model_face = PredictFace()
    im = Image.open("C:/Users/julie/PycharmProjects/SoundLandscape/data/raw/faces/adam.png")
    face = model_face.predict(im)
    print(face)

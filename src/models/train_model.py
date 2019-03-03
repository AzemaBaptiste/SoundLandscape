# -*- coding: utf-8 -*-
import os
import cv2

import numpy as np

import face_recognition

import keras_metrics
from keras.applications import MobileNet
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, Dense, Dropout
from keras.layers import Flatten, GlobalAveragePooling2D, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet import preprocess_input


class TrainFaceDetector(object):
    """Module to predict the name & location of someone in a picture."""

    def __init__(self,):
        """Initiator."""
        self.face_name = list()
        self.face_encoding = list()

    def fit(self, images_paths):
        """Build an encoding for each people in the data directory.

        :param images_paths: (list) paths of all the images
        """
        for path in images_paths:
            name = path.split(os.path.sep)[-1].split(".")[0]
            vars()[name] = face_recognition.load_image_file(path)
            vars()[name + "_encoding"] = face_recognition.face_encodings(vars()[name])[0]
            self.face_encoding.append(vars()[name + "_encoding"])
            self.face_name.append(name)

    def predict(self, image):
        """Predict the location and the name of people in the image.

        :param image: (np.array) image in gray
        :return: (list) (list) names & locations
        """
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


class TrainMoodDetector(object):
    """Module to predict the mood & location of someone in a picture."""

    def __init__(self):
        """Initiator."""
        self.classes = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
        self.model = self.__model__()

    def __model__(self):
        """Build & compile the keras model.

        :return: (Keras.Sequential) model deep
        """
        model = Sequential()
        model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(48, 48, 1)))
        model.add(MaxPooling2D(pool_size=(5, 5), strides=(2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Conv2D(128, (3, 3), activation='relu'))
        model.add(Conv2D(128, (3, 3), activation='relu'))
        model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(len(self.classes), activation='softmax'))
        metrics = ['accuracy', keras_metrics.precision(), keras_metrics.recall()]
        model.compile(loss='categorical_crossentropy', optimizer="Adam", metrics=metrics)

        return model

    @staticmethod
    def process_image_area(image, location):
        """Select the area, and process it.

        :param image: (np.array) image
        :param location: (list) area of the face
        :return: (np.array) image for the prediction
        """
        top, right, bottom, left = location
        face = image[top:bottom, left:right]
        face_resized = cv2.resize(face, (48, 48))
        face_resized_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)

        return face_resized_gray[np.newaxis, :, :, np.newaxis] / 255

    def fit(self, data_path):
        """Build model to predict the mood from an image.

        :param data_path: (str) path of the images.
        """
        # TODO

    def predict(self, image):
        """Predict the mood of each people in the image.

        :param image: (np.array) image
        :return: (str) mood
        """
        moods = list()
        locations = face_recognition.face_locations(image)
        for location in locations:
            processed_img = self.process_image_area(image, location)
            prediction = self.model.predict(processed_img)
            max_idx = np.argmax(prediction[0])
            mood = self.classes[max_idx]
            moods.append(mood)

        return moods, locations


class TrainLandscapeDetector(object):
    """Module to predict the landscape."""

    def __init__(self):
        """Initiator."""
        self.number_classes = 7
        self.batch_size = 128
        self.epochs = 20
        self.loss = self.__loss__()
        self.class_mode = self.loss.split("_")[0]
        self.model = self.__model__()
        self.train_data = ImageDataGenerator()
        self.test_data = ImageDataGenerator()
        self.labels = self.__labels__()

    def __loss__(self):
        """Find loss function based on the number of classes.

        :return: (str) loss
        """
        return "categorical_crossentropy" if self.number_classes > 2 else "binary_crossentropy"

    def build_generator(self, data_path):
        """Build generator to train the model.

        :param data_path: (str) path of the images
        """
        data_generator = ImageDataGenerator(
            preprocessing_function=preprocess_input, horizontal_flip=True,
            width_shift_range=0.2, height_shift_range=0.2
        )
        self.train_data = data_generator.flow_from_directory(
            data_path + "/train", target_size=(224, 224), color_mode='rgb',
            batch_size=self.batch_size, class_mode=self.class_mode, shuffle=True
        )
        self.test_data = data_generator.flow_from_directory(
            data_path + "/test", target_size=(224, 224), color_mode='rgb',
            batch_size=self.batch_size, class_mode=self.class_mode, shuffle=False
        )

    def __labels__(self):
        """Get images labels.

        :return: (dict) all images categories
        """
        return dict((v, k) for k, v in self.train_data.class_indices.items())

    def __model__(self):
        """Build & compile model keras.

        :return: (Keras.Sequential) model deep
        """
        # TODO refactor this shit code
        mobilenet = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        init = mobilenet.output
        pool1 = GlobalAveragePooling2D()(init)
        l1 = Dense(1024)(pool1)
        act1 = Activation(activation="relu")(l1)
        drop1 = Dropout(0.2)(act1)
        l2 = Dense(self.number_classes)(drop1)
        output = Activation(activation="softmax")(l2)
        model = Model(inputs=mobilenet.input, outputs=output)
        for layer in model.layers[:-6]:
            layer.trainable = False
        metrics = ['accuracy', keras_metrics.precision(), keras_metrics.recall()]
        model.compile(optimizer='Adam', loss=self.loss, metrics=metrics)

        return model

    def fit(self, data_path):
        """Build model to predict the landscape type from an image.

        :param data_path: (str) path of the images.
        """
        self.build_generator(data_path)
        self.model.fit_generator(
            generator=self.train_data, validation_data=self.test_data, epochs=self.epochs, verbose=2
        )

    def predict(self, image):
        """Predict the landscape type of the image.

        :param image: (np.array) image
        :return: (str) landscape type
        """
        prediction = self.model.predict(image)
        classe = np.argmax(prediction, axis=1)

        return self.labels[classe]

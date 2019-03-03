# -*- coding: utf-8 -*-
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.image import imread

import numpy as np

from src import settings


class GoogleImages(object):
    """Analyse the % of water/forest/mountain in a gmaps picture."""

    def __init__(self, show=False):
        """Initiator.

        :arg show: (bool) show or not the images
        """
        self.show = show
        self.forest_lower = (180.0, 220.0, 170.0)
        self.forest_upper = (210.0, 240.0, 230.0)
        self.water_lower = (170.0, 200.0, 200.0)
        self.water_upper = (180.0, 220.0, 255.0)

    def get_image_mask(self, image):
        """Select only the image area which contains forest or water.

        :arg image: (PIL) image to analysis
        :return: (dict) np.array of the masks
        """
        return {
            "forest_mask": cv2.inRange(image, self.forest_lower, self.forest_upper),
            "water_mask": cv2.inRange(image, self.water_lower, self.water_upper)
        }

    def compute_ratio(self, **kwargs):
        """Compute the ratio of forest & water."""
        ratios = dict()
        for arg in kwargs:
            if self.show:
                plt.imshow(kwargs[arg])
                plt.show()
            ratios[arg + "_ratio"] = round(np.mean(kwargs[arg] != 0), 3)

        return ratios

    def main(self, image):
        """Main function.

        :arg image: (PIL) image to analysis
        :return: (dict) ratios
        """
        masks = self.get_image_mask(image)

        return self.compute_ratio(**masks)


if __name__ == '__main__':
    path = os.path.join(settings.IMAGE_GPS_PATH, "48.8584+2.29465.jpg")
    img = imread(path)
    rates = GoogleImages().main(img)

# -*- coding: utf-8 -*-
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

import os
import gmaps
import requests
import google_streetview.api

from src import settings


class GoogleImages(object):
    """Save pictures from google using the lat lon."""

    def __init__(self, show=False):
        """Initiator.

        :arg show: (bool) show or not the images
        """
        self.key = settings.google_key
        self.show = show
        self.size = "600x300"
        self.zoom = "16"
        self.roadmap = "roadmap"
        self.base_url = "https://maps.googleapis.com/maps/api/staticmap?"
        self.url = "{base_url}center={lat}+{lng}&zoom={zoom}&size={size}&maptype={roadmap}&key={key}"
        gmaps.configure(api_key=self.key)

    def show_img(self, img):
        """Show the picture.

        :arg img: (PIL) image
        """
        if self.show:
            plt.imshow(img)
            plt.show()

    @staticmethod
    def save_image(img, lat, lng):
        """Save the picture into the directory.

        :param img: (PIL) image
        :param lat: (float) latitude
        :param lng:  (float) longitude
        """
        path = os.path.join(settings.IMAGE_GPS_PATH, f"{lat}+{lng}.jpg")
        img.convert('RGB').save(path)

    def image_gps(self, lat, lng):
        """Get image from google maps api.

        :arg lat: (float) latitude
        :arg lng: (float) longitude
        """
        url = self.url.format(**{
            "lat": lat, "lng": lng, "key": self.key, "size": self.size,
            "zoom": self.zoom, "roadmap": self.roadmap, "base_url": self.base_url
        })
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        self.show_img(img)
        self.save_image(img, lat, lng)

    def image_street(self, lat, lng):
        """Get image from google street api.

        :arg lat: (float) latitude
        :arg lng: (float) longitude
        """
        directory = f"{lat}+{lng}"
        for head in ["0", "090", "180", "270"]:
            params = [
                {
                    "size": "300x200", "location": f"{lat},{lng}",
                    "heading": head, "pitch": "0", "fov": "90", "key": self.key
                }
            ]
            response = google_streetview.api.results(params)
            path = os.path.join(settings.IMAGE_STREET_PATH, directory)
            response.download_links(f"{path}/{head}")


if __name__ == '__main__':
    GoogleImages(show=False).image_gps(48.8584, 2.29466)

# -*- coding: utf-8 -*-
import wikipedia


class WelcomingSequenceSettings(object):
    """Some utils function for this module."""

    def __init__(self):
        """Initiator."""
        pass

    @staticmethod
    def information_about_poi(poi):
        """Information about a poi.

        :param poi: (google_places) poi
        :return: (str) information about this poi or the name
        """
        try:
            return wikipedia.summary(poi.name, sentences=1)
        except:
            return poi.name

# -*- coding: utf-8 -*-
import serial
import pynmea2


class GPSInfo(object):
    """Get gps informations."""

    def __init__(self, com="COM4"):
        """Initiator."""
        self.m_serial = serial.Serial(com, 4800)

    def get_latlon_from_gps(self):
        """Read the latlon&time from the gps.

        :return: (list) lat, lon, datetime
        """
        data_line = self.m_serial.readline().decode()
        data = data_line.split(",")
        if data[0] == "$GPGGA":
            msg = pynmea2.parse(data_line)
            try:
                print(msg.latitude)
                print(msg.longitude)
                return msg
            except:
                return self.get_latlon_from_gps()
        else:
            return self.get_latlon_from_gps()

    def get_speed_from_gps(self):
        """Get speed from gps

        :return: (float) speed
        """
        data_line = self.m_serial.readline().decode()
        data = data_line.split(",")
        if data[0] == "$GPRMC":
            try:
                print(data[7])
                return data[7]
            except:
                return self.get_speed_from_gps()
        else:
            return self.get_speed_from_gps()

# -*- coding: utf-8 -*-

"""
chroma.core
~~~~~~~~~~~~~

Provides Color object

"""

# On tuples and values:
# Whenever possible try to accpet both tuples and values as arguments for
# ease of use (FOR API), but try to impose tuples as arguments / returns
#
# Internally, tuples are assumed to be passed and returned

import colorsys

class Color(object):
    """
    Chroma Color object stores 'color value' to be given in any format
    by one of the properties
    """
    def __init__(self, color_value, format = 'HEX'):
        # self.color is the main storage for the color in the format of a
        # tuple of RGB float
        if format == 'HEX':
            self.color = self._rgb_from_hex(color_value)

    @property
    def rgb(self):
        return self.color

    @property
    def rgb256(self):
        return map(lambda x: int(x*255), self.color)

    @property
    def hex(self):
        r = self._float_to_hex(self.color[0])
        g = self._float_to_hex(self.color[1])
        b = self._float_to_hex(self.color[2])

        return '#' + r + g + b

    def _rgb_from_hex(self, color_value):
        hex_value = str(color_value)

        # Remove hash if exists
        if hex_value[0] == '#':
            hex_value = hex_value[1:]

        # Check length
        if len(hex_value) > 6:
            raise Exception('Invalid Hex Input: %s' % (color_value))

        # Return rgb from hex
        try:
            return (int(hex_value[0:2], 16) / 255.0,
                    int(hex_value[2:4], 16) / 255.0,
                    int(hex_value[4:6], 16) / 255.0)
        except Exception, e:
            raise Exception('Invalid Hex Input: %s' % (color_value))

    def _float_to_hex(self, float_value):
        # Convert from float to in to hex, remove '0x'
        hex_value = hex(int(float_value*255))[2:]

        # If hex is only one digit, pad with 0
        if len(hex_value) == 1:
            hex_value = '0' + hex_value

        return hex_value



# -*- coding: utf-8 -*-

"""
chroma.core
~~~~~~~~~~~~~

Provides Color object

"""

# Tuples are assumed to be passed and returned

import colorsys

class Color(object):
    """
    Chroma Color object stores 'color value' to be given in any format
    by one of the properties
    """
    def __init__(self, color_value = '#FFFFFF', format = 'HEX'):
        if format == 'HEX':
            self.rgb = self._rgb_from_hex(color_value)

    #
    # RGB
    #
    # self.color is the main storage for the color in the format of a
    # tuple of RGB float
    @property
    def rgb(self):
        return self.color

    @property
    def rgb256(self):
        return tuple(map(lambda x: int(x*255), self.color))

    @rgb.setter
    def rgb(self, color_tuple):
        """Used as main setter (rgb256, hls, hls256, hsv, hsv256)"""
        # Check bounds
        self.color = tuple(map(self._apply_float_bounds, color_tuple))

    @rgb256.setter
    def rgb256(self, color_tuple):
        self.rgb = map(lambda x: x/255.0, color_tuple)

    #
    # HLS
    #
    @property
    def hls(self):
        r, g, b = self.color
        return colorsys.rgb_to_hls(r, g, b)

    @property
    def hls256(self):
        r, g, b = self.rgb
        hls = colorsys.rgb_to_hls(r, g, b)
        return tuple(map(lambda x: int(x*255), hls))

    @hls.setter
    def hls(self, color_tuple):
        h, l, s = color_tuple
        self.rgb = colorsys.hls_to_rgb(h, l, s)

    @hls256.setter
    def hls256(self, color_tuple):
        self.hls = map(lambda x: x/255.0, color_tuple)

    #
    # HSV
    #
    @property
    def hsv(self):
        r, g, b = self.color
        return colorsys.rgb_to_hsv(r, g, b)

    @property
    def hsv256(self):
        r, g, b = self.rgb
        hsv = colorsys.rgb_to_hsv(r, g, b)
        return tuple(map(lambda x: int(x*255), hsv))

    @hsv.setter
    def hsv(self, color_tuple):
        h, s, v = color_tuple
        self.rgb = colorsys.hsv_to_rgb(color_tuple)

    @hsv256.setter
    def hsv256(self, color_tuple):
        self.hsv = map(lambda x: x/255.0, color_tuple)

    #
    # HEX
    #
    @property
    def hex(self):
        r = self._float_to_hex(self.color[0])
        g = self._float_to_hex(self.color[1])
        b = self._float_to_hex(self.color[2])

        return '#' + r + g + b

    @hex.setter
    def hex(self, color_value):
        self.rgb = self._rgb_from_hex(color_value)

    #
    # INTERNAL
    #
    def _rgb_from_hex(self, color_value):
        hex_value = str(color_value)

        # Remove hash if exists
        if hex_value[0] == '#':
            hex_value = hex_value[1:]

        # Check length
        if len(hex_value) != 6:
            raise Exception('Invalid Hex Input: %s' % (color_value))

        # Return rgb from hex
        try:
            return (int(hex_value[0:2], 16) / 255.0,
                    int(hex_value[2:4], 16) / 255.0,
                    int(hex_value[4:6], 16) / 255.0)
        except Exception, e:
            raise Exception('Invalid Hex Input: %s' % (color_value))

    def _float_to_hex(self, float_value):
        # Convert from float to in to hex number, remove '0x'
        hex_value = hex(int(float_value*255))[2:]

        # If hex is only one digit, pad with 0
        if len(hex_value) == 1:
            hex_value = '0' + hex_value

        return hex_value

    def _apply_float_bounds(self, coordinate):
        """Assure coordinate is a float between 0 to 1"""
        if coordinate < 0.0:
            return 0.0
        elif coordinate > 1.0:
            return 1.0

        return float(coordinate)

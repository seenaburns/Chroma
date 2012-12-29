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
        # self.color is main storage for color format (tuple in RGB float form)
        # HEX input takes string, RGB / HLS / HSV take tuples

        self.color = (1.0, 1.0, 1.0)
        # If alpha is None, it is unset and assumed to be RGB
        # If non-negative, it has been set and use RGBA, HLSA, etc
        self.alpha = None

        if format.upper() == 'HEX':
            self.rgb = self._rgb_from_hex(color_value)
        elif format.upper() == 'RGB':
            self.rgb = color_value
        elif format.upper() == 'RGB256':
            self.rgb256 = color_value
        elif format.upper() == 'HLS':
            self.hls = color_value
        elif format.upper() == 'HLS256':
            self.hls256 = color_value
        elif format.upper() == 'HSV':
            self.hsv = color_value
        elif format.upper() == 'HSV256':
            self.hsv256 = color_value
        else:
            raise Exception('Unsported chroma.Color format: %s' % (format))
    #
    # RGB
    #
    # RGB is used as base, other formats will modify input into RGB and invoke
    # RGB getters / setters
    @property
    def rgb(self):
        return self._append_alpha_if_necessary(self.color)

    @property
    def rgb256(self):
        rgb = self._append_alpha_if_necessary(self.color)
        return tuple(map(lambda x: int(round(x*255)), rgb))

    @rgb.setter
    def rgb(self, color_tuple):
        """Used as main setter (rgb256, hls, hls256, hsv, hsv256)"""
        # Check bounds
        self.color = tuple(map(self._apply_float_bounds, color_tuple[:3]))

        # Include alpha if necessary
        if len(color_tuple) > 3:
            self.alpha = self._apply_float_bounds(color_tuple[3])

    @rgb256.setter
    def rgb256(self, color_tuple):
        self.rgb = map(lambda x: x / 255.0, color_tuple)

    #
    # HLS
    #
    @property
    def hls(self):
        r, g, b = self.color
        hls = colorsys.rgb_to_hls(r, g, b)
        return self._append_alpha_if_necessary(hls)

    @property
    def hls256(self):
        r, g, b = self.rgb
        hls = colorsys.rgb_to_hls(r, g, b)
        hls = self._append_alpha_if_necessary(hls)
        return tuple(map(lambda x: int(round(x*255)), hls))

    @hls.setter
    def hls(self, color_tuple):
        h, l, s = color_tuple[:3]
        rgb = colorsys.hls_to_rgb(h, l, s)

        # Append alpha if included
        if len(color_tuple) > 3:
            rgb += (color_tuple[3],)

        self.rgb = rgb

    @hls256.setter
    def hls256(self, color_tuple):
        self.hls = map(lambda x: x/255.0, color_tuple)

    #
    # HSV
    #
    @property
    def hsv(self):
        r, g, b = self.color
        hsv = colorsys.rgb_to_hsv(r, g, b)
        return self._append_alpha_if_necessary(hsv)

    @property
    def hsv256(self):
        r, g, b = self.rgb
        hsv = colorsys.rgb_to_hsv(r, g, b)
        hsv = self._append_alpha_if_necessary(hsv)
        return tuple(map(lambda x: int(round(x*255)), hsv))

    @hsv.setter
    def hsv(self, color_tuple):
        h, s, v = color_tuple
        rgb = colorsys.hsv_to_rgb(color_tuple)

        # Append alpha if included
        if len(color_tuple) > 3:
            rgb += (color_tuple[3],)

        self.rgb = rgb

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

    def _append_alpha_if_necessary(self, color_tuple):
        """Return color_tuple with alpha if self.alpha is not None"""
        if self.alpha is not None:
            return color_tuple + (self.alpha,)
        return color_tuple


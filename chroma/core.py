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
        # _alpha used internally
        self._alpha = None

        if format.upper() == 'HEX':
            self.rgb = self._rgb_from_hex(color_value)
        elif format.upper() == 'RGB':
            self.rgb = color_value
        elif format.upper() == 'RGB256':
            self.rgb256 = color_value
        elif format.upper() == 'HLS':
            self.hls = color_value
        elif format.upper() == 'HSV':
            self.hsv = color_value
        elif format.upper() == 'CMY':
            self.cmy = color_value
        elif format.upper() == 'CMYK':
            self.cmyk = color_value
        else:
            raise ValueError('Unsupported chroma.Color format: %s' % (format))

    # Color equality: difference is less than a tolerance
    # Use hex as the test for equals, as it is the greatest resolution without rounding issues
    def __eq__(self, other):
        return self.hex == other.hex

    def __ne__(self, other):
        return not (self == other)

    # Additive / subtractive mixing
    def __add__(self, other):
        return self.additive_mix(other)

    def __radd__(self, other):
        return other.additive_mix(self)

    def __sub__(self, other):
        return self.subtractive_mix(other)

    def __rsub__(self, other):
        return other.subtractive_mix(self)

    # Representation
    def __str__(self):
        return self.hex

    def __repr__(self):
        return self.__str__()

    #
    # Properties
    #

    # RGB
    # RGB is used as base, other formats will modify input into RGB and invoke
    # RGB getters / setters
    @property
    def rgb(self):
        return self._append_alpha_if_necessary(self.color)

    @property
    def rgb256(self):
        rgb256 = tuple(map(lambda x: int(round(x*255)), self.color))
        return self._append_alpha_if_necessary(rgb256)

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

    # HLS
    @property
    def hls(self):
        """
        HLS: (Hue°, Lightness%, Saturation%)
        Hue given as percent of 360, Lightness and Saturation given as percent
        """
        r, g, b = self.color
        hls = colorsys.rgb_to_hls(r, g, b)
        hls = (int(round(hls[0] * 360)), hls[1], hls[2])
        return self._append_alpha_if_necessary(hls)

    @hls.setter
    def hls(self, color_tuple):
        h, l, s = (self._apply_float_bounds(color_tuple[0]/360.0),
                   self._apply_float_bounds(color_tuple[1]),
                   self._apply_float_bounds(color_tuple[2]))
        rgb = colorsys.hls_to_rgb(h, l, s)

        # Append alpha if included
        if len(color_tuple) > 3:
            rgb += (color_tuple[3],)

        self.rgb = rgb

    # HSV
    @property
    def hsv(self):
        """
        HSV: (Hue°, Saturation%, Value%)
        Hue given as percent of 360, Saturation and Value given as percent
        """
        r, g, b = self.color
        hsv = colorsys.rgb_to_hsv(r, g, b)
        hsv = (int(round(hsv[0] * 360)), hsv[1], hsv[2])
        return self._append_alpha_if_necessary(hsv)

    @hsv.setter
    def hsv(self, color_tuple):
        h, s, v = (self._apply_float_bounds(color_tuple[0]/360.0),
                   self._apply_float_bounds(color_tuple[1]),
                   self._apply_float_bounds(color_tuple[2]))
        rgb = colorsys.hsv_to_rgb(h, s, v)

        # Append alpha if included
        if len(color_tuple) > 3:
            rgb += (color_tuple[3],)

        self.rgb = rgb

    # CMY / CMYK
    @property
    def cmy(self):
        """
        CMY: returned in range 0.0 - 1.0
        CMY is subtractive, e.g. black: (1, 1, 1), white (0, 0, 0)
        """
        r, g, b = self.color
        c = 1 - r
        m = 1 - g
        y = 1 - b

        return (c, m, y)

    @cmy.setter
    def cmy(self, color_tuple):
        c, m, y = tuple(map(lambda x: self._apply_float_bounds(x), color_tuple))[:3]
        r = 1 - c
        g = 1 - m
        b = 1 - y
        self.rgb = (r, g, b)

    @property
    def cmyk(self):
        """CMYK: all returned in range 0.0 - 1.0"""
        c, m, y = self.cmy
        k = min(c, m, y)

        # Handle division by zero in case of black = 1
        if k != 1:
            c = (c - k) / (1 - k)
            m = (m - k) / (1 - k)
            y = (y - k) / (1 - k)
        else:
            c, m, y = 1, 1, 1

        cmyk = (c, m, y, k)

        # Apply bound and return
        return tuple(map(lambda x: self._apply_float_bounds(x), cmyk))

    @cmyk.setter
    def cmyk(self, color_tuple):
        c, m, y, k = tuple(map(lambda x: self._apply_float_bounds(x), color_tuple))[:4]
        c = c * (1 - k) + k
        m = m * (1 - k) + k
        y = y * (1 - k) + k
        self.cmy = (c, m, y)

    # HEX
    @property
    def hex(self):
        r = self._float_to_hex(self.color[0])
        g = self._float_to_hex(self.color[1])
        b = self._float_to_hex(self.color[2])
        rgb = '#' + r + g + b

        # Append alpha hex if necessary
        if self.alpha is not None:
            rgb += self._float_to_hex(self.alpha)

        return rgb

    @hex.setter
    def hex(self, color_value):
        self.rgb = self._rgb_from_hex(color_value)

    # Alpha
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = self._apply_float_bounds(value)

    #
    # Color Functions
    # Note: color functions return a Color object when called directly
    #

    # Additive (Light) Mixing
    def additive_mix(self, other):
        rgb_mix = tuple([rgb1 + rgb2 for rgb1, rgb2 in zip(self.rgb, other.rgb)])
        return Color(rgb_mix, 'RGB')

    # Subtractive (Dye, Multiplicative) Mixing
    def subtractive_mix(self, other):
        cmy_mix = tuple([cmy1 + cmy2 for cmy1, cmy2 in zip(self.cmy, other.cmy)])
        return Color(cmy_mix, 'CMY')

    #
    # INTERNAL
    #
    def _rgb_from_hex(self, color_value):
        hex_value = str(color_value)

        # Remove hash if exists
        if hex_value[0] == '#':
            hex_value = hex_value[1:]

        # Check length
        # 6: 6 digit hex
        # 8: 6 digit hex + alpha
        if len(hex_value) not in [6, 8]:
            raise ValueError('Invalid Hex Input: %s' % (color_value))

        # Return rgb from hex
        try:
            rgb =  (int(hex_value[0:2], 16) / 255.0,
                    int(hex_value[2:4], 16) / 255.0,
                    int(hex_value[4:6], 16) / 255.0)

            # Append alpha if exists
            if len(hex_value) == 8:
                rgb += (int(hex_value[6:8], 16) / 255.0,)

            return rgb
        except Exception, e:
            raise ValueError('Invalid Hex Input: %s' % (color_value))

    def _float_to_hex(self, float_value):
        # Convert from float to in to hex number, remove '0x'
        int_value = int(round(float_value*255))
        hex_value = hex(int_value)[2:]

        # If hex is only one digit, pad with 0
        if len(hex_value) == 1:
            hex_value = '0' + hex_value

        return hex_value.upper()

    def _apply_float_bounds(self, coordinate):
        """Assure coordinate is a float between 0 to 1"""
        # Skip None for Alpha
        if coordinate == None:
            return None

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


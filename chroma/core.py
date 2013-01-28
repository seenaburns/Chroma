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
        print 'radd'
        return other.additive_mix(self)

    def __sub__(self, other):
        return self.subtractive_mix(other)

    def __rsub__(self, other):
        return other.subtractive_mix(self)

    # Override __getattr__ to warn users of Color.saturation property issues
    def __getattr__(self, name):
        if name is 'saturation':
            # Warn user of hls / saturation
            saturation_warning = 'Color.saturation is ambiguous. Use Color.hls_saturation or Color.hsv_saturation'
            raise AttributeError(saturation_warning)
        else:
            # Default
            raise AttributeError

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

    # HLS
    @property
    def hls(self):
        """
        HLS: (Hue°, Lightness%, Saturation%)
        Hue given as percent of 360, Lightness and Saturation given as percent
        """
        r, g, b = self.color
        hls = colorsys.rgb_to_hls(r, g, b)
        return self._append_alpha_if_necessary(hls)

    @hls.setter
    def hls(self, color_tuple):
        h, l, s = color_tuple[:3]
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
        return self._append_alpha_if_necessary(hsv)

    @hsv.setter
    def hsv(self, color_tuple):
        h, s, v = color_tuple[:3]
        rgb = colorsys.hsv_to_rgb(h, s, v)

        # Append alpha if included
        if len(color_tuple) > 3:
            rgb += (color_tuple[3],)

        self.rgb = rgb

    # CMYK
    @property
    def cmyk(self):
        """CMYK: all returned in range 0.0 - 1.0"""
        r, g, b = self.color
        k = min((1 - r, 1 - g, 1 - b))

        # Handle division by zero in case of black = 1
        if k != 1:
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
        else:
            c, m, y = 0, 0, 0

        cmyk = (c, m, y, k)

        # Apply bound and return
        return tuple(map(lambda x: self._apply_float_bounds(x), cmyk))

    @cmyk.setter
    def cmyk(self, color_value):
        c, m, y, k = tuple(map(lambda x: self._apply_float_bounds(x), color_value))
        r = 1 - (c * (1 - k)) - k
        g = 1 - (m * (1 - k)) - k
        b = 1 - (y * (1 - k)) - k
        self.rgb = (r, g, b)

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

    #
    # Direct coordinate modification properties
    # Getters not necessary, but available should to make API usage straightforward
    #

    # Alpha
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = self._apply_float_bounds(value)

    # RGB
    @property
    def red(self):
        return self.rgb[0]

    @property
    def green(self):
        return self.rgb[1]

    @property
    def blue(self):
        return self.rgb[2]

    @red.setter
    def red(self, value):
        self.rgb = (value, self.rgb[1], self.rgb[2])

    @green.setter
    def green(self, value):
        self.rgb = (self.rgb[0], value, self.rgb[2])

    @blue.setter
    def blue(self, value):
        self.rgb = (self.rgb[0], self.rgb[1], value)

    # Hue, Saturation, Lightness, Value
    @property
    def hue(self):
        return self.hls[0]

    @property
    def hls_saturation(self):
        return self.hls[2]

    @property
    def hsv_saturation(self):
        return self.hsv[1]

    @property
    def lightness(self):
        return self.hls[1]

    @property
    def value(self):
        return self.hsv[2]

    @hue.setter
    def hue(self, value):
        self.hls = (value, self.hls[1], self.hls[2])

    @hls_saturation.setter
    def hls_saturation(self, value):
        self.hls = (self.hls[0], self.hls[1], value)

    @hsv_saturation.setter
    def hsv_saturation(self, value):
        self.hsv = (self.hsv[0], value, self.hsv[2])

    @lightness.setter
    def lightness(self, value):
        self.hls = (self.hls[0], value, self.hls[2])

    @value.setter
    def value(self, value):
        self.hsv = (self.hsv[0], self.hsv[1], value)

    # Cyan, Magenta, Yellow, Black
    @property
    def cyan(self):
        return self.cmyk[0]

    @property
    def magenta(self):
        return self.cmyk[1]

    @property
    def yellow(self):
        return self.cmyk[2]

    @property
    def black(self):
        return self.cmyk[3]

    @cyan.setter
    def cyan(self, value):
        self.cmyk = (value, self.cmyk[1], self.cmyk[2], self.cmyk[3])

    @magenta.setter
    def magenta(self, value):
        self.cmyk = (self.cmyk[0], value, self.cmyk[2], self.cmyk[3])

    @yellow.setter
    def yellow(self, value):
        self.cmyk = (self.cmyk[0], self.cmyk[1], value, self.cmyk[3])

    @black.setter
    def black(self, value):
        self.cmyk = (self.cmyk[0], self.cmyk[1], self.cmyk[2], value)

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
        cmyk_mix = tuple([cmyk1 - cmyk2 for cmyk1, cmyk2 in zip(self.cmyk, other.cmyk)])
        return Color(cmyk_mix, 'CMYK')

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


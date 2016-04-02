#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chroma Test Suite
~~~~~~~~~~~~~~~~~~~

A series of unittests to check the basic functionality of the Chroma API.

"""

import unittest
import argparse

# Path hack. (for importing)
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
import chroma

class ChromaTestSuite(unittest.TestCase):
    def setUp(self):
        self.c1 = chroma.Color('#335577')
        self.c2 = chroma.Color('#446688')
        self.c3 = chroma.Color('#555555')

    def assertTupleAlmostEqual(self, t1, t2):
        for x, y in zip(t1, t2):
            self.assertEqual(round(x - y, 2), 0)

    def test_color_initialization(self):
        """Test construction of color object"""

        white = chroma.Color('#FFFFFF').hex

        self.assertEqual(chroma.Color((1,1,1), 'RGB').hex, white)
        self.assertEqual(chroma.Color((255, 255, 255), 'RGB256').hex, white)
        self.assertEqual(chroma.Color((0, 1, 1), 'HLS').hex, white)
        self.assertEqual(chroma.Color((0, 0, 1), 'HSV').hex, white)
        self.assertEqual(chroma.Color((0, 0, 0, 0), 'CMY').hex, white)
        self.assertEqual(chroma.Color((0, 0, 0, 0), 'CMYK').hex, white)

        # Test ValueError too
        self.assertRaises(ValueError, chroma.Color, (0, 0, 0), 'ERROR')

    def test_comparison_methods(self):
        """Test equality and inequality"""

        # Equality
        self.assertFalse(self.c1 == self.c2)
        self.assertTrue(self.c1 == chroma.Color('#335577'))

        # Inequality
        self.assertTrue(self.c1 != self.c2)
        self.assertFalse(self.c1 != chroma.Color('#335577'))

    def test_system_conversion(self):
        """Test conversion between systems"""

        # Use Wolfram Alpha as external reference
        # Everything -> RGB
        self.assertTupleAlmostEqual(chroma.Color((0.2, 0.3333, 0.4667), 'RGB').rgb, self.c1.rgb)
        self.assertTupleAlmostEqual(chroma.Color((51, 85, 119), 'RGB256').rgb, self.c1.rgb)
        self.assertTupleAlmostEqual(chroma.Color((210, 0.3333, 0.40), 'HLS').rgb, self.c1.rgb)
        self.assertTupleAlmostEqual(chroma.Color((210, 0.57, 0.466), 'HSV').rgb, self.c1.rgb)
        self.assertTupleAlmostEqual(chroma.Color((0.8, 0.67, 0.53), 'CMY').rgb, self.c1.rgb)
        self.assertTupleAlmostEqual(chroma.Color((0.57, 0.29, 0, 0.53), 'CMYK').rgb, self.c1.rgb)

        # RGB -> Everything
        self.assertTupleAlmostEqual(chroma.Color((0.2, 0.3333, 0.4667), 'RGB').rgb, self.c1.rgb)
        self.assertTupleAlmostEqual(chroma.Color((51, 85, 119), 'RGB256').rgb256, self.c1.rgb256)
        self.assertTupleAlmostEqual(chroma.Color((210, 0.3333, 0.40), 'HLS').hls, self.c1.hls)
        self.assertTupleAlmostEqual(chroma.Color((210, 0.57, 0.466), 'HSV').hsv, self.c1.hsv)
        self.assertTupleAlmostEqual(chroma.Color((0.8, 0.67, 0.53), 'CMY').cmy, self.c1.cmy)
        self.assertTupleAlmostEqual(chroma.Color((0.57, 0.29, 0, 0.53), 'CMYK').cmyk, self.c1.cmyk)

    def test_bad_input(self):
        """Test input that goes beyond color system bounds"""
        # Upper bound
        self.assertEqual(chroma.Color((10, -3, 0.5), 'RGB').rgb, chroma.Color((1, 0, 0.5), 'RGB').rgb)
        self.assertEqual(chroma.Color((300, -3, 50), 'RGB256').rgb256, chroma.Color((255, 0, 50), 'RGB256').rgb256)
        self.assertEqual(chroma.Color((400, -3, 10), 'HLS').hls, chroma.Color((360, 0, 1), 'HLS').hls)
        self.assertEqual(chroma.Color((-10, 40, -1), 'HLS').hls, chroma.Color((0, 1, 0), 'HLS').hls)
        self.assertEqual(chroma.Color((400, -3, 10), 'HSV').hsv, chroma.Color((360, 0, 1), 'HSV').hsv)
        self.assertEqual(chroma.Color((-10, 40, -1), 'HSV').hsv, chroma.Color((0, 1, 0), 'HSV').hsv)
        self.assertEqual(chroma.Color((10, -3, 0.5), 'CMY').cmy, chroma.Color((1, 0, 0.5), 'CMY').cmy)
        self.assertEqual(chroma.Color((10, -3, 0.5, 3), 'CMYK').cmyk, chroma.Color((1, 0, 0.5, 1), 'CMYK').cmyk)

        # Test alpha
        self.c1.rgb = (10, -1, 0.5, 10)
        self.assertEqual(self.c1.rgb, (1, 0, 0.5, 1))
        self.c1.rgb = (10, -1, 0.5, -10)
        self.assertEqual(self.c1.rgb, (1, 0, 0.5, 0))

    def test_alpha(self):
        """Test alpha support / no-support with various color systems"""
        alpha_value = 0.5
        hex_value = self.c1.hex + '80'

        # Test off
        self.assertEqual(self.c1.alpha, None)

        self.c1.alpha = alpha_value

        # Test color systems
        # Test if it is there, and the value is still correct
        self.assertEqual(self.c1.alpha, alpha_value)
        self.assertEqual(self.c1.hex, hex_value)
        self.assertEqual(self.c1.rgb[3], alpha_value)
        self.assertEqual(self.c1.rgb256[3], alpha_value)
        self.assertEqual(self.c1.hls[3], alpha_value)
        self.assertEqual(self.c1.hsv[3], alpha_value)

        # Test no alpha
        self.assertEqual(len(self.c1.cmy), 3)
        self.assertEqual(len(self.c1.cmyk), 4)

        # Test off after
        self.c1.alpha = None
        self.assertEqual(self.c1.alpha, None)
        self.assertEqual(len(self.c1.hex), 7)
        self.assertEqual(len(self.c1.rgb), 3)
        self.assertEqual(len(self.c1.rgb256), 3)
        self.assertEqual(len(self.c1.hls), 3)
        self.assertEqual(len(self.c1.hsv), 3)

    def test_color_blending(self):
        """Test additive and subtractive mixing"""

        # Additive mixing
        self.assertEqual(chroma.Color("#77BBFF"), self.c1 + self.c2)
        self.assertEqual(chroma.Color("#99BBDD"), self.c3 + self.c2)
        self.assertEqual(chroma.Color("#FFFFFF"), chroma.Color("#FFFFFF") + chroma.Color("#000000"))
        self.assertEqual(self.c1, self.c1 + chroma.Color("#000000"))

        # Subtractive mixing
        self.assertEqual(chroma.Color("#FFFF00"), chroma.Color("#FFFFFF") - chroma.Color("#FFFF00"))
        self.assertEqual(chroma.Color("#00FF00"), chroma.Color("#FFFF00") - chroma.Color("#00FFFF"))

    def test_color_blending_with_alpha(self):
        """Test additive mixing with alpha channels"""
        tc1 = chroma.Color("#000000")
        tc1.alpha = 1.0
        tc2 = chroma.Color("#FF0000")
        tc2.alpha = 0.5
        self.assertEqual(chroma.Color("#800000FF"), tc1+tc2)
        self.assertEqual(chroma.Color("#000000FF"), tc2+tc1)
        tc1.alpha = None
        self.assertEqual(chroma.Color("#800000FF"), tc1+tc2)
        self.assertEqual(chroma.Color("#000000FF"), tc2+tc1)


if __name__ == '__main__':
    unittest.main()

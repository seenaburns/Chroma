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
        pass

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


if __name__ == '__main__':
    # Run unit tests
    unittest.main()

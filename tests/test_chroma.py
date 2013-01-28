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
        self.c = chroma.Color()

    def test_color_initialization(self):
        """
        Test construction (and setters) of color object with all formats
        Compare against known rgb256 conversion
        """
        rgb256_value = (85,119,153)
        # Default format
        self.assertEqual(chroma.Color('#557799').rgb256, rgb256_value)
        # HEX
        self.assertEqual(chroma.Color('#557799', 'HEX').rgb256, rgb256_value)
        # RGB
        self.assertEqual(chroma.Color((0.333, 0.465, 0.6), 'RGB').rgb256, rgb256_value)
        # RGB256
        self.assertEqual(chroma.Color((85, 119, 153), 'RGB256').rgb256, rgb256_value)
        # HLS
        self.assertEqual(chroma.Color((0.583, 0.467, 0.286), 'HLS').rgb256, rgb256_value)
        # HSV
        self.assertEqual(chroma.Color((0.583, 0.444, 0.60), 'HSV').rgb256, rgb256_value)
        # CMYK
        self.assertEqual(chroma.Color((0.4444, 0.22, 0, 0.4), 'CMYK').rgb256, rgb256_value)
        # Error
        self.assertRaises(ValueError, chroma.Color, (210, 44, 60), 'ERROR')

    def test_comparison_methods(self):
        """
        Test equality and inequality magic methods
        """
        color1 = chroma.Color('#FF0000')
        color2 = chroma.Color('#557799')
        color3 = chroma.Color((85,119,153), 'RGB256')

        # Equality
        self.assertFalse(color1 == color2)
        self.assertTrue(color2 == color3)

        # Inequality
        self.assertTrue(color1 != color2)
        self.assertFalse(color2 != color3)

    def test_alpha(self):
        """
        Test alpha support with various formats
        """
        rgb256_value = (85,119,153)
        rgba256_value = (85,119,153, 255)
        alpha_value = 1.0

        self.assertEqual(self.c.alpha, None)
        self.c.rgb256 = rgba256_value
        self.assertEqual(self.c.alpha, alpha_value)
        self.assertEqual(self.c.hsv[3], alpha_value)
        self.c.alpha = None
        self.assertEqual(self.c.rgb256, rgb256_value)
        self.assertEqual(len(self.c.hls), 3)
        self.c = chroma.Color('#557799FF')
        self.assertEqual(self.c.rgb256, rgba256_value)

    def test_color_functions(self):
        """
        Test color functions:
            - Additive (Light) Mixing

        Note: Wolfram Alpha used as reference for expected outputs
        """
        color1 = chroma.Color("#335577")
        color2 = chroma.Color("#446688")
        color3 = chroma.Color("#77BBFF")

        # Additive mixing
        self.assertEqual("#77BBFF", color1.additive_mix(color2).hex)
        self.assertEqual("#BBFFFF", color3.additive_mix(color2).hex)
        self.assertEqual("#FFFFFF", chroma.Color("#FFFFFF").additive_mix(chroma.Color("#000000")).hex)
        self.assertEqual(color1.hex, color1.additive_mix(chroma.Color("#000000")).hex)

        # Subtractive mixing
        self.assertEqual("#FFFF00", chroma.Color("#FFFFFF").subtractive_mix(chroma.Color("#FFFF00")).hex)
        self.assertEqual("#00FF00", (chroma.Color("#FFFF00") - chroma.Color("#00FFFF")).hex)


if __name__ == '__main__':
    # Run unit tests
    unittest.main()

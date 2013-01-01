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
        # Error
        self.assertRaises(Exception, chroma.Color, (210, 44, 60), 'ERROR')

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

    def test_coordinate_properties(self):
        """
        Test support for direct modification of coordinate values
        """
        self.c.rgb256 = (100,100,100)
        self.c.red *= 1.1
        self.c.green *= 1.1
        self.c.blue *= 1.1
        for val in self.c.rgb256:
            self.assertAlmostEqual(val, 110)

        self.c.hls = (0.5, 0.5, 0.5)
        self.c.hue *= 1.1
        self.c.hls_saturation *= 1.1
        self.c.lightness *= 1.1
        for val in self.c.hls:
            self.assertAlmostEqual(val, 0.55)

        self.c.hsv = (0.5, 0.5, 0.5)
        self.c.hue *= 1.1
        self.c.hsv_saturation *= 1.1
        self.c.value *= 1.1
        for val in self.c.hsv:
            self.assertAlmostEqual(val, 0.55)

if __name__ == '__main__':
    # Run unit tests
    unittest.main()

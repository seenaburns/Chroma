History
=======

0.2.0 (2013-02-01)
------------------

(Breaks backwards compatibility)

- CMY, CMYK Support
- Color Blending (Addative and Subtractive Mixing)
- Comparison (eq, ne)
- Remove color coordinate properties (direct modification)

Major Bug Fixes

- Hex rounding
- Force alpha between 0 and 1

Other

- Hue (HLS, HSV) in degrees not percent of degrees
- RGB256 alpha in range 0-1, not 0-255
- Force Hex to output in uppercase
- ValueError on bad input
- Extensive documentation on Read the Docs

0.1.3 (2013-01-01)
------------------
- Direct modification of color coordinates

0.1.2 (2012-12-28)
------------------
- Remove HLS256, HSV256 (critical bug)
- Alpha support
- Add RGB, RGB256, HLS, HSV as formats for Color initialization
- Bug fixes

0.1.1 (2012-12-16)
------------------
- HLS, HSV Support
- API changes (setter methods)
- Bug Fixes
- Update to README

0.1.0 (2012-12-15)
------------------
- Initial Release
- RGB and Hex support

Chroma
------

Chroma is a Python module for handling colors with ease. Chroma supports HEX, RGB, HLS and HSV color coordinates and can seamlessly support alpha.

Quickstart
::

    import chroma

    # Create a Color object
    color = chroma.Color('#00FF00')

    # Get RGB, HLS, and HSV in either float or 0 - 255 (8bit)
    # Also, HEX
    color.rgb # (0.0, 1.0, 0.0)
    color.hls # (0.3333333333333333, 0.5, 1.0)
    color.rgb256 # (0, 255, 0)
    color.hex = # '#00FF00'

    # Set RGB, HLS, HSV (float or 256) and HEX
    color.rgb256 = (255, 0, 0)
    color.hls = (0.0, 1.0, 0.0)

BSD licensed. Hosted on `Github <https://github.com/seenaburns/Chroma>`_ and available on PyPI.

Currently Supports
-------------------
- Hex (#rrggbb, #rrggbbaa)
- RGB (float, 256)
- HLS (float)
- HSV (float)
- Alpha
- Direct modification of Red, Green, Blue, Lightness, Hue, Saturation (HLS, HSV), Value

Roadmap
-------
- More Hex formats (#RGB, #RRRGGGBBB, #RRRRGGGGBBBB)
- Color dectection in images

Documentation
-------------
Install Chroma with Pip:
::

    pip install chroma

To handle various color coordinates, Chroma uses a Color object. A Color object can be initialized with any available color format (HEX, RGB, RGB256, HLS, HSV).
::

    c = chroma.Color()  # defaults to white
    c = chroma.Color('#557799')  # default format is HEX
    c = chroma.Color((0.583, 0.444, 0.60), 'HSV')  # create Color object with HLS

To modify or access the color in any format, use Color's properties.
::

    c.hex
    c.rgb
    c.rgb256
    c.hls
    c.hsv

    c.hex = '#557799'
    c.hsv = (0.583, 0.444, 0.60)
    ...

Chroma Colors also support alpha. A Color object's alpha is set to None by default, and as long as it is None it will be ignored. If it is included when setting the color, it will be added to the getters returns as well.
::

    c.hex = '#557799'
    c.rgb  # (0.3333, 0.4666, 0.6)

    c.hex = '#557799FF'
    c.rgb  # (0.3333, 0.4666, 0.6, 1.0)
    c.hls  # (0.5833, 0.4666, 0.2857, 1.0)

    c.alpha = None
    c.rgb  # (0.3333, 0.4666, 0.6)

To simplify modifying color values, Chroma supports direct modification of color coordinates.
::
    c.red *= 1.1
    c.green *= 1.1
    c.blue *= 1.1

    c.hue *= 1.1
    c.lightness *= 1.1
    c.hls_saturation *= 1.1

    c.value *= 1.1
    c.hsv_saturation *= 1.1

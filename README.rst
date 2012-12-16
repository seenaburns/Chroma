Chroma
------

Chroma is a Python module for handling colors with ease.

Quickstart
::

    import chroma

    # Create a Color object
    color = chroma.Color('#00FF00')

    # Get RGB, HLS, and HSV in either float or 0 - 255 (8bit)
    # Also, HEX
    color.rgb # [0.0, 1.0, 0.0]
    color.hls # (0.3333333333333333, 0.5, 1.0)
    color.rgb256 # [0, 255, 0]
    color.hex = # '#00FF00'

    # Set RGB, HLS, HSV (float or 256) and HEX
    color.rgb256 = (255, 0, 0)
    color.hls = (0.0, 1.0, 0.0)

Currently supports RGB, HLS, HSV and HEX (#RRGGBB) coordinates.

BSD licensed. Hosted on `Github <https://github.com/seenaburns/Chroma>`_ and available on PyPI.

Installation: ::

    pip install tungsten

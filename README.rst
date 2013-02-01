Chroma
======

Chroma is a Python module for handling colors with ease.

Manipulating colors can quickly escalate into a tedious and complicated task, particularly when you become concerned with color systems beyond RGB. Chroma is here to provide a simple API to do the heavy lifting, so that you can stay focused on the important parts of your projects.

Before you ask, Chroma is BSD licensed, available on `Github <https://github.com/seenaburns/Chroma>`_ and PyPI.

Features
--------

- Hex (#rrggbb, #rrggbbaa)
- RGB
- HLS
- HSV
- CMY, CMYK
- Alpha
- Color Blending: additive and subtractive mixing

Roadmap
-------

- Coordinates (sRGB, YIQ, CIE, LAB and more)
- Color harmonies: complementary, analogous, triad
- Color difference
- Color detection in images

Quickstart
==========

Getting started with the power of Chroma is meant to be straightforward
::

    import chroma

    # Create a color object
    color = chroma.Color('#00FF00')

    # Handling different color systems
    color.cmy = (0.3, 0.7, 0.8)
    color.rgb    # (0.7, 0.3, 0.2)
    color.hls    # (0.0333, 0.45, 0.5556)

    # Alpha
    color.alpha = 0.5
    color.hsv    # (0.03333, 0.7143, 0.7, 0.5)

    # Color blending
    color + chroma.Color("#FF00FF")
    # #FF4DFF

And there you have it. The `documentation <https://chroma.readthedocs.org/en/latest/>`_ describes Chroma's functionality and usage in detail.

Installation
------------

Installation is as easy as
::

    pip install chroma

Or if you're an easy_install-er
::

    easy_install chroma

Chroma does not yet support Python 3, but, if you're interested, contribute!

Contribute
==========

Chroma is under active development and could use your support. Even bug reports, feature suggestions and feedback can help push Chroma forward in the right direction.

Chroma is hosted on `Github <https://github.com/seenaburns/Chroma>`_ and there are a number of ideas of where to start in the `issues section <https://github.com/seenaburns/Chroma/issues>`_.

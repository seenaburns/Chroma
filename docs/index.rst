Chroma Documentation
====================

Chroma is a Python module for handling colors with ease.

Manipulating colors can quickily escalate into a tedious and complicated task, particularly when you become concerned with color systems beyond RGB. Chroma is here to provide a simple API to do the heavy lifting, so that you can stay focused on the important parts of your projects.

Before you ask, Chroma is BSD licensed, available on `Github <https://github.com/seenaburns/Chroma>`_ and PyPI.

Features
--------
- :ref:`basic`
- Color Systems: :ref:`RGB <rgb>`, :ref:`HEX <hex>`, :ref:`HLS <hls>`, :ref:`HSV<hsv>`, :ref:`CMY and CMYK<cmyk>`
- :ref:`alpha`
- :ref:`blending`

Quickstart
----------

Getting started with the power of Chroma is meant to be straightfoward:

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

    # Additive mixing
    mix = color + chroma.Color("#FF00FF")

And there you have it. The rest of this document describes Chroma's functionality and usage in detail.

Installation
------------

Installation is as easy as:

::

    pip install chroma

Or if you're an easy_install-er:

::

    easy_install chroma

Chroma does not yet support Python 3, but, if you're interested: :ref:`contribute`

.. _basic:
Basic Color Tasks
-----------------

Color Systems
-------------

.. _rgb:
RGB - Red, Blue, Green
----------------------

.. _hex:
HEX - #rrggbb
-------------

.. _hls:
HLS - Hue, Saturation, Lightness
--------------------------------

.. _hsv:
HSV - Hue, Saturation, Value
----------------------------

.. _cmyk:
CMY and CMYK - Cyan, Magenta, Yellow (and Black)
------------------------------------------------

.. _alpha:
Alpha
-----


.. _blending:
Blending (Additive and Subtractive Mixing)
------------------------------------------

.. _contribute:
Contribute
----------
Chroma is under active development and could use your support. Even bug reports, feature suggestions and feedback can help push Chroma forward in the right direction.

Chroma is hosted on `Github <https://github.com/seenaburns/Chroma>`_ and there are a number of ideas of where to start in the `issues section <https://github.com/seenaburns/Chroma/issues>`_.

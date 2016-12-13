===============================
PyLuxafor
===============================


.. image:: https://img.shields.io/pypi/v/pyluxafor.svg
        :target: https://pypi.python.org/pypi/pyluxafor
        :remote:

.. image:: https://img.shields.io/travis/takeontom/pyluxafor.svg
        :target: https://travis-ci.org/takeontom/pyluxafor
        :remote:

.. image:: https://readthedocs.org/projects/pyluxafor/badge/?version=latest
        :target: https://pyluxafor.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
        :remote:

.. image:: https://pyup.io/repos/github/takeontom/pyluxafor/shield.svg
     :target: https://pyup.io/repos/github/takeontom/pyluxafor/
     :alt: Updates
     :remote:


Python API for the Luxafor Flag


* Free software: MIT license
* Documentation: https://pyluxafor.readthedocs.io.


Features
--------

* Python 3+
* Simple, clean API to control the
  `Luxafor Flag <http://luxafor.com/luxafor-flag/>`
* Where possible, allows the setting of multiple, specific LEDs at once.


Installation
------------

Install via pip::

    $ pip install pyluxafor

Create the file: `/etc/udev/rules.d/10-luxafor.rules` with the following
contents::

    ACTION=="add", SUBSYSTEM=="usb", ATTRS{idProduct}=="f372", ATTRS{idVendor}=="04d8", MODE:="666"

Then reload udev::

    $ sudo service udev reload

Then unplug your Luxafor Flag and reinsert it.

Example usage
-------------

::

    from pyluxafor import LuxaforFlag
    from time import sleep

    flag = LuxaforFlag()
    flag.off()
    flag.do_fade_colour(
        leds=[LuxaforFlag.LED_TAB_1, LuxaforFlag.LED_BACK_1, LuxaforFlag.LED_BACK_2],
        r=10, g=10, b=0,
        duration=255
    )
    flag.do_static_colour(leds=LuxaforFlag.LED_BACK_3, r=0, g=0, b=100)

    sleep(3)
    flag.off()

    flag.do_pattern(LuxaforFlag.PATTERN_POLICE, 3)


Credits
---------

Many thanks to `vmitchell85 <https://github.com/vmitchell85>` for his
`luxafor-python <https://github.com/vmitchell85/luxafor-python>` project,
which provided the initial inspiration for this project, and provided easy
answers to the problems I encountered.

If you're looking to control a Luxafor Flag in Windows using Python,
vmitchell85's project is probably the best bet:

* https://github.com/vmitchell85/luxafor-python

# -*- coding: utf-8 -*-
import usb


class LuxaforFlag(object):
    DEVICE_VENDOR_ID = 0x04d8
    DEVICE_PRODUCT_ID = 0xf372

    MODE_STATIC_COLOUR = 1
    MODE_FADE_COLOUR = 2
    MODE_STROBE = 3
    MODE_WAVE = 4
    MODE_PATTERN = 6

    LED_TAB_1 = 1
    LED_TAB_2 = 2
    LED_TAB_3 = 3
    LED_BACK_1 = 4
    LED_BACK_2 = 5
    LED_BACK_3 = 6
    LED_TAB_SIDE = 65
    LED_BACK_SIDE = 66
    LED_ALL = 255

    WAVE_SINGLE_SMALL = 1
    WAVE_SINGLE_LARGE = 2
    WAVE_DOUBLE_SMALL = 3
    WAVE_DOUBLE_LARGE = 4

    PATTERN_LUXAFOR = 1
    PATTERN_RANDOM1 = 2
    PATTERN_RANDOM2 = 3
    PATTERN_RANDOM3 = 4
    PATTERN_POLICE = 5
    PATTERN_RANDOM4 = 6
    PATTERN_RANDOM5 = 7
    PATTERN_RAINBOWWAVE = 8

    def __init__(self, device = None):
        self.device = device
        self.serial_number = None
        self.firmware_version = None
        
        if self.device:
            self.setup_device(device)

    def discover(self):
        """
        Return list of all devices, None if no devices present
        """

        devices = usb.core.find(find_all=True, idVendor=LuxaforFlag.DEVICE_VENDOR_ID, idProduct=LuxaforFlag.DEVICE_PRODUCT_ID)

        flags = list()

        for device in devices:
            flag = LuxaforFlag(device)
            flags.append(flag)

        if len(flags) > 0:
            return flags
        else:
            return None


    def get_device(self):
        """
        Retrieve a PyUSB device for the Luxafor Flag.

        Will lazy load the device as necessary.
        """
        if not self.device:
            self.device = self.find_device()
            self.setup_device(self.device)
        return self.device

    def setup_device(self, device):
        """
        Performs initialisation on the device.
        """
        try:
            # Gets around "Resource busy" errors
            device.detach_kernel_driver(0)
        except Exception as e:
            pass

        device.set_configuration()
        self.get_serial_number()

    def find_device(self):
        """
        Attempts to retrieve the Luxafor Flag device using the known Vendor
        and Product IDs.
        """
        device = usb.core.find(
            idVendor=LuxaforFlag.DEVICE_VENDOR_ID,
            idProduct=LuxaforFlag.DEVICE_PRODUCT_ID
        )
        return device
    
    def get_serial_number(self):
        """
        Populates the device's serial number
        """
        self.write([0x80,0,0,0,0,0,0,0])
        data = self.read(8)
        while data[0] != 0x80 :
            self.write([0x80,0,0,0,0,0,0,0])
            data = self.read(8)
        self.serial_number = (data[2]<<8) | data[3]
        self.firmware_version = data[1]


    def write(self, values):
        """
        Send values to the device.

        Expects the values to be a List of command byte codes. Refer to
        the individual commands for more information on the specific command
        codes.
        """
        self.get_device().write(1, values)

        # Sometimes the flag simply ignores the command. Unknown if this
        # is an issue with PyUSB or the flag itself. But sending the
        # command again works a treat.
        self.get_device().write(1, values)

    def read(self, bytecount):
        return self.get_device().read(0x81, bytecount)

    def create_static_colour_command(self, led, r, g, b):
        return [LuxaforFlag.MODE_STATIC_COLOUR, led, r, g, b]

    def create_fade_colour_command(self, led, r, g, b, duration=20):
        return [LuxaforFlag.MODE_FADE_COLOUR, led, r, g, b, duration]

    def create_strobe_command(self, led, r, g, b, duration=20, repeat=2):
        return [LuxaforFlag.MODE_STROBE, led, r, g, b, duration, 0, repeat]

    def create_wave_command(self, wave_type, r, g, b, duration=20, repeat=1):
        return [
            LuxaforFlag.MODE_WAVE, wave_type, r, g, b, duration, 0, repeat
        ]

    def create_pattern_command(self, pattern_id, repeat=1):
        return [LuxaforFlag.MODE_PATTERN, pattern_id, repeat]

    def off(self):
        """
        Turn off all LEDs.
        """
        self.do_static_colour(255, 0, 0, 0)

    def on(self):
        """
        Turn on all LEDs to white
        """
        self.do_static_colour(255,255,255,255)

    def do_static_colour(self, leds, r, g, b):
        """
        Set a single LED or multiple LEDs immediately to the specified colour.
        """
        self._do_multi_led_command(
            self.create_static_colour_command, leds, r, g, b
        )

    def do_fade_colour(self, leds, r, g, b, duration):
        """
        Fade a single LED or multiple LEDs from their current colour to a new
        colour for the supplied duration.
        """
        self._do_multi_led_command(
            self.create_fade_colour_command, leds, r, g, b, duration
        )

    def do_strobe(self, led, r, g, b, duration, repeat):
        """
        Flash the specified LED a specific colour, giving the duration of each
        flash and the number of times to repeat.

        Unfortunately this command does not support multiple specific LEDs.
        """
        command = self.create_strobe_command(led, r, g, b, duration, repeat)
        self.write(command)

    def do_wave(self, wave_type, r, g, b, duration, repeat):
        """
        Animate the flag with a wave pattern of the given type, using the
        specified colour, duration and number of times to repeat.
        """
        command = self.create_wave_command(
            wave_type, r, g, b, duration, repeat
        )
        self.write(command)

    def do_pattern(self, pattern, repeat):
        """
        Execute a built in pattern a given number of times.
        """
        command = self.create_pattern_command(pattern, repeat)
        self.write(command)

    def _do_multi_led_command(
        self, create_command_function, leds, *args, **kwargs
    ):
        try:
            iter(leds)
        except TypeError:
            command = create_command_function(leds, *args, **kwargs)
            self.write(command)
        else:
            for led in leds:
                command = create_command_function(led, *args, **kwargs)
                self.write(command)

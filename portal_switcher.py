
"""
`portal_switcher`
================================================================================
Simple touchscreen control surface for interfacing with mimoLive for controlling
an HDMI hardware switcher. This is my first project using CircuitPython on
an Adafruit PyPortal.

* Author: Jason Pecor

"""
import board
import time
import adafruit_touchscreen
from adafruit_pyportal import PyPortal

from adafruit_bitmap_font import bitmap_font
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from padded_button import PaddedButton


# The buttons on the TFT display will send keycodes just like a standard keyboard
keyboard = Keyboard()
keyboard_layout = KeyboardLayoutUS(keyboard)

# Setup touchscreen
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(320, 240), z_threshhold=5000)

# Enable/disable sending the keycodes.  This will help prevent surprise syntax errors
# in the code when testing the touchscreen.  :)
send_codes = True

# Load the font to be used on the buttons
font = bitmap_font.load_font("/fonts/Dina.bdf")

# Prepare TFT for graphics 
# I originally wrote this code for the M4 Express + TFT display combo, so there
# may be a more optimal way to to it with the PyPortal.  This works though, so...

# splash = displayio.Group(max_size=10)
# board.DISPLAY.show(splash)
#
# # Someday, I'll figure out what this code is really doing.
# color_bitmap = displayio.Bitmap(320, 240, 1)
# color_palette = displayio.Palette(1)
# color_palette[0] = 0x000000
#
# # Same here
# tilegrid_0 = displayio.TileGrid(color_bitmap,
#                                 pixel_shader=color_palette,
#                                 x=0,
#                                 y=0)
# splash.append(tilegrid_0)

# As it turns out, the code above can all be replaced with the following:
pyportal = PyPortal(default_bg=0x000000)

button_margin = (1, 1)

# Create the buttons
#
# This code is a bit verbose and clumsy, and it can be streamlined by pre-defining
# the sizes and anchor points for each button.  However, keeping it all here like
# this provides some additional context for making sense of what is passed into the
# init() function for each button.
#
# Also, this uses a class called PaddedButton which is based on the adafruit_button class
# It provides additional arguments for margin and padding

cut_button = PaddedButton(x=0, y=0, width=160, height=120,
                          fill_color=0x000000, outline_color=0xFFFFFF,
                          selected_outline=0x00ff00, selected_fill=0x00ff00,
                          label="Cut", label_font=font, label_color=0xffffFF,
                          style=1, margin=button_margin, padding=(5, 5))

cross_button = PaddedButton(x=160, y=0, width=160, height=120,
                            fill_color=0xd5d5d5, outline_color=0xd5d5d5,
                            selected_outline=0x00ff00, selected_fill=0x00ff00,
                            label="Cross", label_font=font, label_color=0x000000,
                            style=1, margin=button_margin, padding=(5, 5))

graphics_button = PaddedButton(x=0, y=120, width=64, height=120, label="GFX",
                               label_font=font, label_color=0xffffFF,
                               fill_color=0xC10721, outline_color=0xC10721,
                               selected_fill=0x00ff00, selected_outline=0x00ff00,
                               style=1, margin=button_margin)

cam_1_button = PaddedButton(x=64, y=120, width=64, height=120, label="Cam\n 1",
                            label_font=font, label_color=0xffffFF,
                            fill_color=0x094A85, outline_color=0x094A85,
                            selected_fill=0x00ff00, selected_outline=0x00ff00, style=1,
                            margin=button_margin, padding=(5, 5))

cam_2_button = PaddedButton(x=128, y=120, width=64, height=120, label="Cam\n 2",
                            label_font=font, label_color=0xffffFF,
                            fill_color=0x094A85, outline_color=0x094A85,
                            selected_fill=0x00ff00, selected_outline=0x00ff00, style=1,
                            margin=button_margin, padding=(5, 5))

cam_3_button = PaddedButton(x=192, y=120, width=64, height=120, label="Cam\n 3",
                            label_font=font, label_color=0xffffFF,
                            fill_color=0x094A85, outline_color=0x094A85,
                            selected_fill=0x00ff00, selected_outline=0x00ff00, style=1,
                            margin=button_margin, padding=(5, 5))

cam_4_button = PaddedButton(x=256, y=120, width=64, height=120, label="Cam\n 4",
                            label_font=font, label_color=0xffffFF,
                            fill_color=0x094A85, outline_color=0x094A85,
                            selected_fill=0x00ff00, selected_outline=0x00ff00, style=1,
                            margin=button_margin, padding=(5, 5))

# Add all of the buttons to a list
buttons = [graphics_button,
           cam_1_button,
           cam_2_button,
           cam_3_button,
           cam_4_button,
           cut_button,
           cross_button]

# Add margin and padding to all of the buttons
# And add to the display
for button in buttons:
    button.padding = (5, 5)
    button.margin = (10, 10)
    pyportal.splash.append(button.group)

# Ssetup SPI for touchscreen - Only needed for M4 w/TFT
# cs = digitalio.DigitalInOut(board.D8)
# st = Adafruit_STMPE610_SPI(spi, cs)

last_p = None  # Will be used to trap Off->On touch transition

while True:

    p = ts.touch_point

    if (p is not None) & (last_p is None):  # Only catch the Off->On transition

        (y, x, z) = p

        for i, b in enumerate(buttons):

            if b.contains(p):

                b.selected = True
                print("Button {} pressed.".format(b.label))

                if send_codes:
                    if b == cam_1_button:
                        keyboard.send(Keycode.ONE)  # 1
                    elif b == cam_2_button:
                        keyboard.send(Keycode.TWO)  # 2
                    elif b == cam_3_button:
                        keyboard.send(Keycode.THREE)  # 3
                    elif b == cam_4_button:
                        keyboard.send(Keycode.FOUR)  # 4
                    elif b == graphics_button:
                        keyboard.send(Keycode.GRAVE_ACCENT)  # `
                    elif b == cut_button:
                        keyboard.send(Keycode.C)  # C
                    elif b == cross_button:
                        keyboard.send(Keycode.ENTER)  # Enter

            else:
                b.selected = False

    else:
        # Toggle the cut and cross buttons back off when released
        cut_button.selected = False
        cross_button.selected = False

    # Capture state of p to setup one-shot compare
    time.sleep(0.5)
    last_p = p

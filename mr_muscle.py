import os
import time
from threading import Thread

import win32api
import win32con

from mss import mss
from PIL import Image


"""
All coordinates assume  a screen resolution of 1366x768, and Chrome
maximized with the Bookmarks Toolbar enabled.
X_PAD = 382
Y_PAD = 135
PLAY_AREA = X_PAD, Y_PAD, X_PAD + 602, Y_PAD + 96
"""

SCREEN_PATH = os.path.join(
            os.getcwd(), 'screens'
        )
SPACE = 0x20

X_PAD = 382
Y_PAD = 135


def screen_grab(sct, save=False):
    """Capture game screen shot"""
    box = (X_PAD, Y_PAD, X_PAD + 602, Y_PAD + 96)
    im = sct.grab(box)
    im = Image.frombytes("RGB", im.size, im.bgra, "raw", "BGRX")
    if save:
        im.save(
            f'{SCREEN_PATH}\\{time.time()}.png', 'PNG'
        )
    return im


def get_cords():
    """Get coordinates of mouse cursor with
    respect to X_PAD, Y_PAD"""
    x, y = win32api.GetCursorPos()
    x = x - X_PAD
    y = y - Y_PAD
    return x, y


def get_x(x):
    """Get x coords"""
    return x - X_PAD


def get_y(y):
    """Get y coords"""
    return y - Y_PAD


class Box:
    """
    Specific cords for Box
    """
    start_y = 192
    end_y = 228

    height = end_y - start_y
    width = 125


class Cords:
    """
    Specific cords for Mr.Muscle Game
    """
    # Mid point
    mid_x = get_x(683)

    # Y coordinate to check for RGB
    check_y = get_y(211)

    # X coordinates to check for RGB
    check_x = (
        mid_x - (Box.width//2),
        mid_x + (Box.width//2)
    )

    # Check coordinates
    check = (
        check_x, check_y
    )


class RGB:
    """
    Specific RGBs for Mr.Muscle Game
    """
    ready_white = (187, 210, 208)
    white = (193, 216, 214)
    box = (10, 41, 61)
    box_border_left = (16, 55, 71)
    box_border_right = (18, 61, 74)


class Bot:
    """
    Bot logic for Mr.Muscle game
    """
    image = None

    def see(self, sct):
        """Grab screen"""
        self.image = screen_grab(sct, save=False)

    def ready(self):
        """Check if game on top"""
        return self.image.getpixel(
            (Cords.mid_x, 1)
        ) == RGB.ready_white

    def perfect(self):
        """Check if time to act"""
        return self.image.getpixel(
            (Cords.check_x[0], Cords.check_y)
        ) == RGB.box and self.image.getpixel(
            (Cords.check_x[1], Cords.check_y)
        ) == RGB.box

    @staticmethod
    def act():
        """Press space"""
        win32api.keybd_event(SPACE, 0, 0, 0)
        time.sleep(.05)
        win32api.keybd_event(SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)

    def start(self, sct):
        """Start the bot"""
        self.see(sct)
        if self.perfect():
            self.act()


def main():
    bot = Bot()
    with mss() as sct:
        while True:
            bot.start(sct)


if __name__ == '__main__':
    threads = []
    for i in range(20):
        thread = Thread(target=main)
        thread.start()
        threads.append(thread)

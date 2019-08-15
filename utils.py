import os
import time

import win32api
import win32con

from PIL import Image


SCREEN_PATH = os.path.join(
            os.getcwd(), 'screens'
        )


def screen_grab(sct, box, save=False):
    """Capture screen"""
    im = sct.grab(box)
    im = Image.frombytes('RGB', im.size, im.bgra, 'raw', 'BGRX')
    if save:
        im.save(
            f'{SCREEN_PATH}\\{time.time()}.png', 'PNG'
        )
    return im


def press(key):
    """Press the passed key"""
    win32api.keybd_event(key, 0, 0, 0)
    time.sleep(.02)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

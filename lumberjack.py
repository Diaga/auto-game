import os
import time
from threading import Thread

from mss import mss

from utils import screen_grab, press


"""
All coordinates assume  a screen resolution of 1366x768, and Chrome
maximized with the Bookmarks Toolbar enabled.
X_PAD = 382
Y_PAD = 135
PLAY_AREA = X_PAD, Y_PAD, X_PAD + 215, Y_PAD + 30
"""

LEFT_ARROW = 0x25
RIGHT_ARROW = 0x27

X_PAD = 575
Y_PAD = 325

BOX = (X_PAD, Y_PAD, X_PAD + 215, Y_PAD + 30)


class Cords:
    """Cords for LumberJack game"""
    LEFT_CHECK_JACK = (48, 25)
    RIGHT_CHECK_JACK = (167, 25)

    LEFT_CHECK_WOOD = (48, 12)
    RIGHT_CHECK_WOOD = (167, 12)


class RGB:
    """RGBs for LumberJack game"""
    BACKGROUND = (211, 247, 255)
    WOOD = (136, 99, 50)
    JACK = (51, 93, 101)


class Bot:
    """Logic for LumberJack game"""
    image = None
    sct = None

    wait_counter = 0
    counter = 0

    location = ''

    def __init__(self, sct):
        """Initialize class"""
        self.sct = sct

    def get_location(self):
        """Populate location field"""
        if self.image.getpixel(Cords.LEFT_CHECK_JACK) == RGB.JACK:
            self.location = 'left'
        elif self.image.getpixel(Cords.RIGHT_CHECK_JACK) == RGB.JACK:
            self.location = 'right'
        else:
            self.location = None

    def get_wood(self):
        """Return wood location"""
        if self.image.getpixel(Cords.LEFT_CHECK_WOOD) == RGB.WOOD:
            return 'left'
        elif self.image.getpixel(Cords.RIGHT_CHECK_WOOD) == RGB.WOOD:
            return 'right'
        else:
            return ''

    def ready(self):
        """Check if game is up"""
        self.get_location()
        return self.location

    def see(self):
        """Capture the required area"""
        self.image = screen_grab(self.sct, BOX, False)

    def should_move(self):
        """Should the location change?"""
        wood = self.get_wood()
        if wood:
            self.wait_counter = 0
            return wood == self.location
        elif self.wait_counter < 5:
            self.wait_counter += 1
            time.sleep(0.02)
            return 'wait'
        else:
            self.wait_counter = 0
            return False

    def move(self):
        """Move Jack"""
        if self.location == 'right':
            press(LEFT_ARROW)
        elif self.location == 'left':
            press(RIGHT_ARROW)

    def next(self):
        """Next step"""
        if self.location == 'right':
            press(RIGHT_ARROW)
        elif self.location == 'left':
            press(LEFT_ARROW)

    def should_sleep(self):
        """Should wait?"""
        return self.counter < 0

    def sleep(self):
        """Return dynamic sleep values based on counter"""
        if self.should_sleep():
            time.sleep(0.1175)


def main():
    """Run"""
    with mss() as sct:
        bot = Bot(sct)
        while True:
            bot.see()
            if bot.ready():
                should_move = bot.should_move()
                if should_move == 'wait':
                    pass
                elif should_move:
                    bot.move()
                else:
                    bot.next()

                bot.counter += 1
                bot.sleep()


if __name__ == '__main__':
    main()

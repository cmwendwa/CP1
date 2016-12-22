# -*- coding: utf-8 -*-
import sys
import time

def spinningCursor():
    """ 
    generator for spinning cursor characters
    """
    while True:
        for cursor in '|/-\\':
            yield cursor


def playSpinner():
    """call to play spinning cursor on the terminal """ 
    spinner = spinningCursor()
    for _ in range(16):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
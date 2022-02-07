#!/usr/bin/env python3

"""Minimal waiting animation for the terminal.
Please refer to `__main__` for example usage.
"""

import functools
import itertools
import threading
import time


class Animation:
    """Provides start and stop methods for animated terminal output.
    Can be used in context managers.
    """
    symbol = itertools.cycle([
        ' ...      ',
        '  ...     ',
        '   ...    ',
        '    ...   ',
        '     ...  ',
        '      ... ',
        '       ...',
        ' .      ..',
        ' ..      .',
    ])

    def __init__(self):
        self.finished = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def _animate(self):
        while not self.finished:
            print(next(self.symbol), sep='', end='\r', flush=True)
            time.sleep(0.075)

    def start(self):
        """Starts the animation in a new thread."""
        threading.Thread(target=self._animate).start()

    def stop(self):
        """Stops the animation and clears the line."""
        self.finished = True
        print('          ', sep='', end='\r', flush=True)


def wait_for_it(func):
    """Plays an animation while func is running.
    Intended for the use as decorator.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        with Animation():
            return func(*args, **kwargs)
    return wrapped


if __name__ == '__main__':

    @wait_for_it
    def long_running_function():
        """For demonstration purposes."""
        time.sleep(2)

    print('Use as decorator')
    long_running_function()

    print('Use as context manager')
    with Animation() as animation:
        time.sleep(1)
        animation.stop()
        print(' ... animation stopped')
        time.sleep(2)

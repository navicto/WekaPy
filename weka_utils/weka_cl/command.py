__author__ = 'Victor'
import os

import subprocess

class WekaCommand(object):
    def __init__(self, heap='16g', cp=None):
        self._heap = heap
        self._cp = cp
        self._string = 'java -Xmx' + self._heap + ' '
        if self._cp:
            self._string += '-cp ' + self._cp + ' '

    def execute(self, verbose=False, shell=True):
        if verbose:
            print self
        subprocess.call(self._string, shell=shell)

    def add2command(self, addition):
        self._string += addition

    def __str__(self):
        return self._string

def concatenate(*commands):
    '''
    Concatenates command objects.
    :param commands: Command objects (or object from sublasses that preserve the ._string attribute)
    :return: cl --> Command object whose ._string attribute contains the concatenation of input commands
    '''
    if os.name == 'nt':
        separation = '&&'
    else:
        separation = ';'
    cl = WekaCommand()
    cl._string = commands[0]._string
    for command in commands[1:]:
        cl._string += separation + command._string
    return cl



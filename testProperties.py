#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mthornton
#
# Created:     20/02/2017
# Copyright:   (c) mthornton 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class C(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x


def testXproperty():
    testP = C()
    print testP.x # getter
    testP.x = 10  # setter
    del testP.x   # deleter

if __name__ == '__main__':
    testXproperty()

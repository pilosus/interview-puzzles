# -*- coding: utf-8 -*-

from ma import Second

class B(Second):
    def __init__(self, i):
        self.i = i
        self.magic = 5
        self.isSecond = 1

    def fnc(self, val1, val2):
        return val1 * val2 * self.magic

    def isFirst(self):
        return 0

# -*- coding: utf-8 -*-

"""
Coding time: 59 min


instanceof 

see: 

https://stackoverflow.com/questions/1549801/differences-between-isinstance-and-type-in-python
"""

class Parent(object):
    pass
        
class First(Parent):
    pass

class Second(Parent):
    pass

class MyError(Exception):
    pass

class A(First):
    def __init__(self):
        self.i = 3
        self.isSecond = 0

    def __setattr__(self, name, value):
        if name == 'isSecond' and value == 2:
            raise AttributeError()
        else:
            object.__setattr__(self, name, value)
        
    def fnc(self, val):
        if val == 7:
            raise MyError('Error text')
        else:
            return val * val * self.i

    def isFirst(self):
        return 1

    

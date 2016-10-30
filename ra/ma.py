# -*- coding: utf-8 -*-

"""
ma is a module for Ramax International's interview test problem.

This module shows the use of class inheritance in Python, setting and
getting object's attributes, as well as throwing exceptions.

The code below follows PEP8 style guide for Python code and
checked against pep8 tool.

Total coding time for ma and mb modules: 59 minutes.
Text editor: GNU/Emacs
"""

__author__ = 'Vitaly R. Samigullin'
__copyright__ = "Copyright 2016, Vitaly R. Samigullin"
__status__ = 'Production'


class MyError(Exception):
    """
    A custom error class derived from the Exception class.

    It used to throw a custom exception in the First class fnc method.
    """
    pass


class Parent(object):
    """
    A parent class the following classes derived from.

    There's nothing to do in this class. Let's just pass it.
    """
    pass


class First(Parent):
    """
    A subclass of a Parent class

    We could redefine constructor as follows:

    def __init__(self):
        super(Parent, self).__init__()

    But let's stick to a Python's concise and beautiful style and
    just pass the body of the derived class
    """
    pass


class Second(Parent):
    pass


class A(First):
    def __init__(self):
        self.i = 3
        self.isSecond = 0

    def __setattr__(self, name, value):
        # throw an exception if and only if
        # we try to assign 2 to isSecond attribute
        if name == 'isSecond' and value == 2:
            raise AttributeError()
        else:
            object.__setattr__(self, name, value)

    def fnc(self, val):
        if val == 7:
            raise MyError('Error text')
        else:
            # we could easily use 3 instead of self.i
            # because setting object's attribute i to another value
            # would break the test, but we don't since using `magic` numbers
            # considered a bad style of programming.
            return val * val * self.i

    def isFirst(self):
        """
        isFirst breaks PEP8 naming conventions (this is not Java!),
        but probably makes a good job tricking down an interviewee.

        The good name for this function could be isfirst (like isinstance),
        or is_first.
        """
        return 1

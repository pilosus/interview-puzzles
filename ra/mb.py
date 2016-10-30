# -*- coding: utf-8 -*-

from ma import Second

"""
mb is a module for Ramax International's interview test problem.

This module shows the use of class inheritance in Python, defining
class methods, and commenting.

The code below follows PEP8 style guide for Python code and
checked against pep8 tool.

Total coding time for ma and mb modules: 59 minutes.
Text editor: GNU/Emacs
"""

__author__ = 'Vitaly R. Samigullin'
__copyright__ = "Copyright 2016, Vitaly R. Samigullin"
__status__ = 'Production'

# Common sense and PEP8 require to use descriptive names for constants,
# variables, functions, etc. We do not want to have some magic coefficients
# in the fnc method. We don't now either what fnc exactly doing or should it
# rely on a object's attribute of some kind (as we supposed in ma module).
# So for the diversity sake let's assume this time, that fnc uses a constant.
# We still have no idea what it's for, but bear in mind it should be named
# properly!
NOT_A_MAGIC_CONSTANT = 5


class B(Second):
    def __init__(self, i):
        self.i = i
        self.isSecond = 1

    def fnc(self, val1, val2):
        return val1 * val2 * NOT_A_MAGIC_CONSTANT

    def isFirst(self):
        return 0

import random
import logging

"""
### Global and local variables. Scope ###

http://www.python-course.eu/python3_global_vs_local_variables.php
"""
def fun(x, l=[]):
    for i in range(x):
        l.append(i)
    return l

"""
### Function decorators ###

http://www.python-course.eu/python3_decorators.php
https://www.oreilly.com/ideas/5-reasons-you-need-to-learn-to-write-python-decorators
http://blog.thedigitalcatonline.com/blog/2015/04/23/python-decorators-metaprogramming-with-style/
"""

def test_argument_is_natural_number(func):
    def wrapper(x):
        if type(x) == int and x > 0:
            return func(x)
        else:
            raise ValueError("Argument is not a natural number")
    return wrapper


@test_argument_is_natural_number
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def make_non_negative(func):
    def wrapper(x):
        result = func(x)
        if result <= 0:
            return 0
        else:
            return result
    return wrapper

@make_non_negative
def negative_range(n):
    return random.randrange(-n, n)


# logging decorator
def log_it(func):
    def wrapper(*args, **kwargs):
        logging.warning('{0} function has been called.'.format(func.__name__))
        result = func(*args, **kwargs)
        logging.warning('Function returned: {0}.'.format(result))
        return result
    return wrapper

@log_it
def mult(a, b):
    return a * b



"""
### Multiple inheritance ###
"""


class A(object):
    def __init__(self):
        self.i = 10

    def go(self):
        print("A goes here")


class B(A):
    def __init__(self):
        self.i = 20

    def go(self):
        super(B, self).go()
        print("B goes here")


class C(A):
    def __init__(self):
        self.i = 30

    def go(self):
        super(C, self).go()
        print("C goes here")


class D(B, C):
    def __init(self):
        pass

    def go(self):
        super(D, self).go()
        print("D goes here")


"""
d.go() works as "deep-first left-to-right traversal + remove duplicates expect for the last one

D -> B -> A -> object -> C -> A -> object

Now, after removing all duplicates, except for the last one, we get:

D -> B -> C -> A -> object

That's why first A.go will be printed, then C.go, then B.go and then D.go

See discussion here:
https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
"""


"""
### Class method, Static Method ###

see http://stackoverflow.com/a/1669524/4241180

Class method:
  - can be called on class (no instance of the class is necessary)
  - get use of cls not self
  - one of the main uses of classmethod is to define "alternative constructors":
    http://stackoverflow.com/a/1950927/4241180

"""


class TestCls(object):
    def __init__(self, s):
        self.s = s

    @classmethod
    def alt_constr(cls, l):
        """
        An alternative constructor for TestCls

        >>> t1 = TestCls('hello')
        >>> t1
        TestCls('hello')
        >>> t2 = TestCls.alt_constr([1, 2, 3])
        >>> t2
        TestCls('1, 2, 3')
        :param l: a list
        :return: TestCls instance
        """
        # create instance using default constructor with an empty string
        c = cls('')
        # assign new value to self.s
        c.s = ', '.join(str(s) for s in l)
        # return the instance
        return c

    def __repr__(self):
        return "TestCls({0})".format(self.s)

    def foo(self, x):
        return "foo(%s, %s)" % (self, x)

    @classmethod
    def class_foo(cls, x):
        return "class_foo(%s, %s)" % (cls, x)

    @staticmethod
    def static_foo(x):
        return "static_foo(%s)" % x

# now let's inherit from TestCls

class NewTestCls(TestCls):
    """
    Alternative constructor using class method inherited from TestCls.
    """
    def __repr__(self):
        return "NewTestCls({0})".format(self.s.upper())

nt1 = NewTestCls.alt_constr(['hello', 'world'])

# yet another example of using class method for alternative constructor
# http://stackoverflow.com/a/12179752/4241180

class NewDate(object):
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        # parse args
        day, month, year = map(int, date_as_string.split('-'))
        # create an instance
        new_date = cls(day, month, year)
        return new_date

"""
### Metaclass ###

The most comprehensive practical tutorial on metaclass:
http://stackoverflow.com/a/6581949/4241180
"""

# first metaclass
class UpperAttrMetaclass(type):
    """
    Metaclass, sublassed from type metaclass.

    Makes sure all attributes are uppercased.
    """
    def __new__(cls, clsname, bases, dct):
        uppercase_attr = {}

        for name, value in dct.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = value
            else:
                uppercase_attr[name] = value

        return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr)


def useless_method(self):
    """
    Custom method for the metaclass
    :param self: instance of the class
    :return: 2-tuple of ints
    """
    return self.X, self.Y

MyClass = UpperAttrMetaclass('UpperAttrMetaclass', (),
                             {'x': 1, 'y': 2, 'useless_method': useless_method})

mc1 = MyClass()


# yet another metaclass

class DocStrMeta(type):
    """
    Metaclass subclassed from type metaclass.

    Makes sure all methods (except for private and non-callable ones) have docstring.
    """

    def __new__(cls, name, bases, attrs):
        no_docs = []

        for key, val in attrs.items():
            # skip if it's a special method or non-callable
            if key.startswith("__"):
                continue

            if not hasattr(val, "__call__"):
                continue

            # if method has no __doc__, then add it to the list,
            # raise exception, once all methods checked
            # and at least one method lacks
            try:
                result = getattr(val, '__doc__')
                if not result:
                    no_docs.append(key)
            except Exception as err:
                pass

        if no_docs:
            list_as_str = ', '.join(no_docs)
            raise TypeError("Methods: {0} have no docstring!".format(list_as_str))

        return super(DocStrMeta, cls).__new__(cls, name, bases, attrs)


class EnoughDocs(object):

    __metaclass__ = DocStrMeta

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


    def geta(self):
        """
        Get the a!

        Once removed this docstring, Python will throw a TypeError, because parent class requires docstrings!
        :return: int (constant)
        """
        return self.a

    def seta(self, newa):
        """
        Set the a!
        :param newa:
        :return:
        """
        self.a = newa


"""
__call__ method

See discussion here:
https://stackoverflow.com/questions/5824881/python-call-special-method-practical-example

See also Python's data model:
https://docs.python.org/3/reference/datamodel.html
"""


class Factorial:
    def __init__(self):
        self.cache = {}

    def __call__(self, n):
        if n not in self.cache:
            if n == 0:
                self.cache[n] = 1
            else:
                self.cache[n] = n * self.__call__(n - 1)
        return self.cache[n]


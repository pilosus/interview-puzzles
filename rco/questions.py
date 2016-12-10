import random
import logging
import urllib.request
from contextlib import ContextDecorator, contextmanager
from time import time


"""
### Global and local variables. Scope ###

http://www.python-course.eu/python3_global_vs_local_variables.php
"""
def fun(x, l=[]):
    for i in range(x):
        l.append(i)
    return l

"""
### Class-based decorators
"""


class CustomException(ValueError):
    pass


class DecoratorClass(object):
    def __init__(self, exception, *args, **kwargs):
        self.exception = exception
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        def wrap(*args, **kwargs):
            result = f(*args, **kwargs)
            if result < 0:
                raise self.exception
            return result
        return wrap



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
    def __init__(self, name, bases, attrs):
        nodocs = []
        for key, value in attrs.items():
            # skip special and private methods
            if key.startswith("__"): continue
            # skip any non-callable
            if not hasattr(value, "__call__"): continue
            # check for a doc string. a better way may be to store
            # all methods without a docstring then throw an error showing
            # all of them rather than stopping on first encounter
            if not getattr(value, '__doc__'):
                nodocs.append(key)
                #raise TypeError("%s must have a docstring" % key)

        if nodocs:
            methods_without_docstr = ", ".join(nodocs)
            raise TypeError("Methods {0} have no docstring!".format(methods_without_docstr))

        type.__init__(self, name, bases, attrs)


class EnoughDocs(object, metaclass=DocStrMeta):
    # __metaclass__ field used in Python 2.x. but disallowed in Python 3.x
    # use keyword argument metaclass for a class instead
    #__metaclass__ = DocStrMeta

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
class NotEnoughDocs(object, metaclass=DocStrMeta):
    # __metaclass__ field used in Python 2.x, but disallowed in Python 3
    # for Python 3 use keyword argument `metaclass`
    #__metaclass__ = DocStrMeta

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def geta(self):
        return self.a

    def seta(self, newa):
        self.a = newa

n = NotEnoughDocs(1, 2, 3)
"""

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

"""
### Context manager
See also:
https://jeffknupp.com/blog/2016/03/07/python-with-context-managers/
"""

class UrlRetriever():
    def __init__(self, url):
        self.url = url

    def __enter__(self):
        self.local_filename, self.headers = urllib.request.urlretrieve(self.url)
        self.response = open(self.local_filename)
        return self.response

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.close()

"""
### contextlib
See also
https://docs.python.org/3/library/contextlib.html
https://gist.github.com/bradmontgomery/4f4934893388f971c6c5
"""


@contextmanager
def opener(url='http://www.python.org'):
    print('Start')
    yield urllib.request.urlopen(url)
    print('Stop')


class TimeElapsed(ContextDecorator):
    def __enter__(self):
        self.start = time()
        print("Start time: {}".format(self.start))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = time()
        elapsed = self.stop - self.start
        print("Stop time: {0}".format(self.stop))
        print("Time elapsed: {0}".format(elapsed))


import unittest
import sys
from contextlib import contextmanager
from io import StringIO
from time import sleep

import questions as q
from models import *

# Helper functions
@contextmanager
def captured_output():
    """
    Use for testing functions with print statements:

    with captured_output() as (out, err):
      d.go()

    output = out.getvalue().strip()
    self.assertEqual(output, 'Expected output')

    See also: http://stackoverflow.com/a/17981937/4241180
    :return:
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


# Test cases
class InterviewTestCase(unittest.TestCase):
    def test_getsizeof(self):
        """
        Python docs:

        sys.getsizeof() returns the size of an object in bytes.
        The object can be any type of object. getsizeof() calls the object's
        __sizeof__ method and adds an additional garbage collector overhead
        if the object is managed by the garbage collector.

        https://docs.python.org/3/library/sys.html#sys.getsizeof
        :return:
        """
        self.assertEqual(sys.getsizeof(1), sys.getsizeof(2))

        # because type(int) or type(list) => <type 'type'>,
        # but type(int()) => <type 'int'> and type(list()) => <type 'list'>
        self.assertEqual(sys.getsizeof(int), sys.getsizeof(float))
        self.assertEqual(sys.getsizeof(list), sys.getsizeof(set))


        # sizes of objects for some built-in types
        # http://stackoverflow.com/a/30316760/4241180

        # list is an array; set is a kind of hash table;
        # hash table is more complex than an array, so it should have
        # bigger memory footprint.
        self.assertLess(sys.getsizeof(list()), sys.getsizeof(set()))

    def test_hash(self):
        """
        Python docs:

        Return the hash value of the object (if it has one). Hash values are integers.
        They are used to quickly compare dictionary keys during a dictionary lookup.
        Numeric values that compare equal have the same hash value (even if they are
        of different types, as is the case for 1 and 1.0).

        https://docs.python.org/3/library/functions.html#hash
        :return:
        """
        self.assertEqual(hash(1), hash(1.0))
        self.assertNotEqual(hash('a'), hash('b'))

        # http://stackoverflow.com/a/7648538/4241180
        # The hash value -1 signalizes an error to CPython. This is because C doesn't have exceptions,
        # so it needs to use the return value. When a Python object's __hash__ returns -1,
        # CPython will actually silently change it to -2.
        self.assertNotEqual(hash(-1), -1)
        self.assertTrue(hash(-1), -2)

    def test_fun_with_list(self):
        """

        Execution model (name binding and scopes)
        https://docs.python.org/3/reference/executionmodel.html

        Blocks: a module, a function body, and a class definition, a script file, str args to eval(), exec()
        The following constructs bind names: formal parameters to functions, import statements,
        class and function definitions, for loop header, or after as in a with statement or except clause.

        :return:
        """
        result1 = q.fun(3)
        self.assertEqual(result1, [0, 1, 2])

        result2 = q.fun(1, [1, 2, 3])
        self.assertEqual(result2, [1, 2, 3, 0])

        result3 = q.fun(5)
        self.assertEqual(result3, [0, 1, 2, 0, 1, 2, 3, 4])

    def test_id_is(self):
        """
        id() returns the identity of an object. This is an integer (or long integer) which is
        guaranteed to be unique and constant for this object during its lifetime.
        Two objects with non-overlapping lifetimes may have the same id() value.

        CPython implementation detail: This is the address of the object in memory.

        id() (or its equivalent) is used in the "is" operator.
        see:
        https://stackoverflow.com/questions/15667189/what-does-id-function-used-for
        :return:
        """
        result1 = [1, 2, 3, 4]
        result2 = [1, 2, 3, 4]
        result3 = result1

        self.assertNotEqual(id(result1), id(result2))
        self.assertNotEqual(id(result1[0]), id(result1[1]))
        self.assertEqual(id(result1), id(result3))

        foo = 1
        bar = foo
        baz = bar
        err = 1

        self.assertEqual(foo, bar)
        self.assertEqual(baz, foo)
        self.assertEqual(err, foo)

        self.assertTrue(foo is 1)
        self.assertTrue(bar is foo)
        self.assertTrue(baz is bar)
        self.assertTrue(err is foo)

    def test_multiple_inheritance(self):
        """
        See discussion in question.py
        """
        d = q.D()
        d_order = (q.D, q.B, q.C, q.A, object)

        self.assertEqual(q.D.__mro__, d_order)

        with captured_output() as (out, err):
            d.go()

        output = out.getvalue().strip()
        self.assertEqual(output, 'A goes here\nC goes here\nB goes here\nD goes here')

    def test_classmethod_staticmethod(self):
        """
        See discussion in question.py
        """
        t1 = q.TestCls("hello")
        t2 = q.TestCls.alt_constr([1, 2, 3, 4, 5])
        nt1 = q.NewTestCls.alt_constr(['hello', 'world'])

        self.assertEqual(t1.foo(1), "foo(TestCls(hello), 1)")
        self.assertEqual(t1.class_foo(1), "class_foo(<class 'questions.TestCls'>, 1)")
        self.assertEqual(t1.static_foo(1), "static_foo(1)")
        self.assertEqual(q.TestCls.class_foo(1), t1.class_foo(1))
        self.assertEqual(q.TestCls.static_foo(1), t1.static_foo(1))
        self.assertEqual(str(t2), "TestCls(1, 2, 3, 4, 5)")
        self.assertEqual(str(nt1), "NewTestCls(HELLO, WORLD)")

        date1 = q.NewDate(11, 10, 2016)
        date2 = q.NewDate.from_string('11-10-2016')

        self.assertEqual(date1.day, date2.day)
        self.assertEqual(date1.month, date2.month)
        self.assertEqual(date1.year, date2.year)

    def test_metaclass(self):
        """
        See discussion in question.py
        """
        self.assertTrue(hasattr(q.mc1, 'X'))
        self.assertFalse(hasattr(q.mc1, 'x'))
        self.assertTrue(hasattr(q.mc1, 'Y'))
        self.assertFalse(hasattr(q.mc1, 'y'))
        self.assertTrue(hasattr(q.mc1, 'USELESS_METHOD'))
        self.assertFalse(hasattr(q.mc1, 'useless_method'))
        self.assertEqual(q.mc1.X, 1)
        self.assertEqual(q.mc1.Y, 2)
        self.assertEqual(q.mc1.USELESS_METHOD(), (1, 2))

        with self.assertRaises(TypeError):
            class NotEnoughDocs(object, metaclass=q.DocStrMeta):
                def __init__(self, make, model, color):
                    self.make = make
                    self.model = model
                    self.color = color

                def change_gear(self):
                    print("Changing gear")

                def start_engine(self):
                    print("Changing engine")

        class EnoughDocs(object, metaclass=q.DocStrMeta):
            pass

        enough = EnoughDocs()

        self.assertEqual(enough.__class__.__class__.__name__, "DocStrMeta")
        # we are no intended to unit-test Python itself here! Use as a reminder
        self.assertEqual(enough.__class__.__class__, q.DocStrMeta)


    def test_function_decorators(self):
        @q.make_non_negative
        def identity(x):
            return x

        self.assertEqual(identity(10), 10)
        self.assertEqual(identity(-10), 0)

    def test_class_decorator(self):
        pass

    def test_call_method(self):
        fact = q.Factorial()
        self.assertEqual(fact(5), 120)

    def test_db_query(self):
        u1 = User(name="Vitaly")
        session.add(u1)
        u2 = User(name="Anna")
        session.add(u2)
        u3 = User(name="Olga")
        session.add(u3)
        session.commit()

        d1 = Dialogue(receiver_id=u1.id, sender_id=u2.id)
        session.add(d1)
        d2 = Dialogue(receiver_id=u2.id, sender_id=u3.id)
        session.add(d2)
        d3 = Dialogue(receiver_id=u3.id, sender_id=u1.id)
        session.add(d3)
        session.commit()

        # find all Dialogues where u1 is either receiver or sender
        q1 = session.query(Dialogue).filter((Dialogue.sender == u1) | (Dialogue.receiver == u1)).all()

        self.assertIn(d1, q1)
        self.assertIn(d3, q1)
        self.assertNotIn(d2, q1)

        # find all dialogues between u1 and u3
        q2 = session.query(Dialogue).filter(((Dialogue.sender == u1) | (Dialogue.receiver == u1)) &
                                            ((Dialogue.sender == u3) | (Dialogue.receiver == u3))).all()

        self.assertIn(d3, q2)
        self.assertNotIn(d1, q2)
        self.assertNotIn(d2, q2)

    def test_class_based_decorators(self):
        @q.DecoratorClass(q.CustomException)
        def mult(a, b):
            return a * b

        with self.assertRaises(q.CustomException):
            mult(-10, 5)

        self.assertEqual(mult(2, 3), 6)

    def test_context_manager(self):
        with q.UrlRetriever('http://python.org/') as html:
            self.assertIn('Welcome to Python.org', html.read())

    def test_contextlib(self):
        with q.opener('http://www.python.org') as page:
            self.assertIn(b'Welcome to Python.org', page.read())
        # capture output first
        with captured_output() as (out, err):
            # now use ContextManager
            with q.TimeElapsed():
                sleep(1)
                print("...")
                sleep(1)

        output = out.getvalue().strip()
        self.assertIn("Start time", output)
        self.assertIn("Stop time", output)
        self.assertIn("Time elapsed", output)



        #self.fail('Finish the tests!')


if __name__ == '__main__':
    unittest.main()

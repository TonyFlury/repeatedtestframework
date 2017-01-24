===================================
Why use the repeated Test Framework
===================================

The repeated Test Framework is designed to reduce the amount of repetitive code required to
test some function/method with a lot of different data sets, while keep the benefits of using the
`unittest`_ module :

------------------
Summary comparison
------------------

The following table shows a side-by-side comparison of using :ref:`multiple-test`, using a :ref:`single-test`, and using the :ref:`framework`. It can be seen that the Framework retains the advantages of the explicit single test methods while also keeping the small code footprint that can normally only be acheieved by having a loop within a single test method.

**Advantages**

    +-----------------------+------------------------+--------------------+--------------------+
    |                       | :ref:`multiple-test`   | :ref:`single-test` | :ref:`framework`   |
    |                       |                        |                    |                    |
    +=======================+========================+====================+====================+
    | Unique test methods   |       Yes              |      No            |    Yes             |
    +-----------------------+------------------------+--------------------+--------------------+
    | Unique doc strings    |       Yes              |      No            |    Yes             |
    | with input data       |                        |                    |                    |
    +-----------------------+------------------------+--------------------+--------------------+
    | Testing continues     |       Yes              |      No            |    Yes             |
    | after failure         |                        |                    |                    |
    +-----------------------+------------------------+--------------------+--------------------+
    | Decorate test cases   |       Yes              |      No            |    Yes             |
    | (skip etc)            |                        |                    |                    |
    +-----------------------+------------------------+--------------------+--------------------+
    | Test data in one      |       No               |      Yes           |    Yes             |
    | place in source       |                        |                    |                    |
    +-----------------------+------------------------+--------------------+--------------------+

**Disadvantages**

    +-----------------------+------------------------+--------------------+--------------------+
    |                       | :ref:`multiple-test`   | :ref:`single-test` | :ref:`framework`   |
    |                       |                        |                    |                    |
    +=======================+========================+====================+====================+
    | Repititive code       |       Yes              |      No            |    No              |
    +-----------------------+------------------------+--------------------+--------------------+


The remainder of this page explores in detail the methodologies compared in the above table; giving an example of the same tests (and the same deliberate error) in each methodology, and describing the advantages and disadvantages which the table outlines.

-----

.. _multiple-test:

-----------------------------
Multiple Expilicit Test cases
-----------------------------

The 'standard' way to use the `unittest`_ module is to write multiple test methods, with each method testing single input data point. As an illustration, :ref:`Example1` shows an trivial example of this methodology where a single item of functionality (in this case integer multiplication) is being tested against
with multiple input values.

.. _`Example1`:

Example 1 - Multiple explicit Test cases
----------------------------------------

.. code-block:: python

    class TestCases(unittest.TestCase):

        def test_test1(self):
            """Confirm that 1*2 == 2"""
            self.assertEqual(1*2, 2)

        def test_test2(self):
            """Confirm that 2*2 == 2"""
            self.assertEqual(2*2, 4)

        def test_test3(self):
            """Confirm that 3*2 == 6"""
            self.assertEqual(3*2, 6)

        def test_test3(self):
            """Confirm that 3*4 == 11"""
             self.assertEqual(3*2, 11)

This testing methodology has a number of distinct and important advantages:

    Unique Test cases
        Each test case can be executed from the command line (or from another script) as required - maybe to help diagnose a bug, or confirm a bug fix.

    Unique documentation strings.
        Unique documentation strings means that testing output can include a descripton of the functionality being tested, and the input data being used (as well as the expected result). This can be very useful in documenting what has been tested and what input data is being used.

    Test Separation
        Any test failure will not stop the execution of the remaining test cases.

However this methodogy has a distinct disadvantage in the case being discussed where the same functionality is being tested with mutiple different input data points: there is considerable repetition of very similar code, with the essential the difference between each test method being the data point being tested.

-----

.. _`single-test`:

---------------------------------------
Using a loop witin a single test method
---------------------------------------

The most obvious way to remove the repititive code in :ref:`Example1` would be to refactor the tests into a single test method with a loop (after all a competent developer would never write 10 lines of code when that code could be written as a 4 line loop). :ref:`Example2` shows the same tests being executed using a single test method with a loop, and a list defining the test data.

.. _`Example2`:

Example 2 - Single Test method with a loop
------------------------------------------

.. code-block:: python

    class TestCases(unittest.TestCase):

        def test_testAll(self):
            """Confirm that all test cases work"""
            test_input = [(1,2,2),(2,2,4),(3,2,6), (3,4,11)]
            for in1, in2, result in test_input:
                self.assertEqual(in1*in2, result)

Example 2 clearly has far less code for any reasonable number of test cases, but despite the reduction of repition compared to  :ref:`Example1`, but this also brings some distinct advantages when testing.

    Non Unique testcases
        We only have one test method, so we can't use the command line to isolate and execute a single test case - (e.g. just test with an input of 3 & 4 - which fails in the above example). We also can't easily isolate and skip some input data (unless we edit the list).

    Non Unique Documentation Strings
        With only one test case, and one documentation string to describe all of your test case, you will have limited logging as to what has been tested (depending on the verbosity level being used, the documentation strings will appear in your test output).

    No Test Separation
        The loop system also has the disadvantage that any single failure will stop all further test execution in the list. The use of the `subtest`_ context manager can be used to ensure that testing continues after a failure in this example - it does not solve the other issues listed above.

-----

.. _`framework`:

Repeated Test Framework
-----------------------

The Repeated Test Framework provides a solution to all of these identified above by:

    1. You write one generic method to execute the function/method which is under test.
    #. You specify the actual test data as a list (in a similar to :ref:`Example2`).
    #. Creating (behind the scenes) a unique test method for input data point
    #. Allowing for customisation of both the names and documentation strings of those test methods.

.. _`Example3`:

Example 3 - Using the Repeated Test Framework
---------------------------------------------

.. code-block:: python

    from RepeatedTestFramework import RepeatedTestFramework

    def test_method_wrapper(index, input, expected_result):
        a, b = input[0], input[1]
        def test_method(self):
            """The actual test method which gets replicated"""
            self.assertEqual( a * b, expected_result)
        return test_method_wrapper

    @RepeatedTestFramework(
        test_name = 'test_multiplication',
        test_method = test_method_wrapper,
        test_input = [
                {'input':(1,2), 'expected_result':2 },
                {'input':(2,2), 'expected_result':4 },
                {'input':(3,2), 'expected_result':6 },
                {'input':(3,4), 'expected_result':11 },]
            )
    class TestCases(unittest.TestCase):
        pass

By default the test method names and documentation strings both contain the input data - allowing you to easily differentiate between the test methods both on the command line and in test result output. The test method names and documentation strings are completely customisable and can be edited to contain any data item which is part of your test input data.

As well as providing a simple method of generating many test cases, the Framework also provides methods for addong the normal unitest decorators to the generated methods, meaning that all of the unittest functionality is still available.

In the above example the Framework will create the following test methods :

+-------------------------------+----------------------------------+-----+-----+-------------------+
| Test method name              | Documentation string             | *a* | *b* | *expected_result* |
+===============================+==================================+=====+=====+===================+
| test_001_test_multiplication  | test_multiplication 001 (1,2) 2  |  1  |  2  |        2          |
+-------------------------------+----------------------------------+-----+-----+-------------------+
| test_002_test_multiplication  | test_multiplication 002 (2,2) 4  |  2  |  2  |        2          |
+-------------------------------+----------------------------------+-----+-----+-------------------+
| test_003_test_multiplication  | test_multiplication 003 (3,2) 6  |  3  |  2  |        4          |
+-------------------------------+----------------------------------+-----+-----+-------------------+
| test_004_test_multiplication  | test_multiplication 004 (3,4) 11 |  3  |  4  |        6          |
+-------------------------------+----------------------------------+-----+-----+-------------------+

From the above table it can be seen that by default the test method name includes an automatically generated index number, and the ``test_name`` attribute that is passed to the ``RepeatedTestFramework`` decorator. The documentation string by default includes the ``test_name`` attribute, the generated index, as well as both the ``input`` and ``expected_result`` values from the relevant item in the ``test_input`` list attribute. The generated index, and each item from the list is passed to the ``test_method`` function as a set of keywords attributes, which can be used by the ``test_method`` function in anyway required.

For full of how to use the framework including how to customise test names, how to decorate individual test cases, and some useful usage suggestions see :doc:`using`.


.. _unittest: https://docs.python.org/3.5/library/unittest.html
.. _subtest: https://docs.python.org/3.5/library/unittest.html#distinguishing-test-iterations-using-subtests
.. _usage: <usage>

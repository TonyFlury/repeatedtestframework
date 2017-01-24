=======================
Repeated Test Framework
=======================


.. image:: https://img.shields.io/pypi/v/repeatedtestframework.svg
    :target: https://pypi.python.org/pypi/repeatedtestframework

.. image:: https://travis-ci.org/TonyFlury/repeatedtestframework.png?branch=master
    :target: https://travis-ci.org/TonyFlury/repeatedtestframework/

.. image:: https://codecov.io/github/TonyFlury/repeatedtestframework/coverage.svg?branch=master
        :target: https://codecov.io/github/TonyFlury/repeatedtestframework?branch=master

.. image:: https://readthedocs.org/projects/repeatedtestframework/badge/?version=latest
        :target: https://readthedocs.org/projects/repeatedtestframework/?badge=latest

------------
Introduction
------------
The repeated Test Framework is designed to be used with the ``unittest`` standard library module (`unittest for Python 2.7`_, `unittest for Python 3.5`_), to
make to generate multiple test cases against the same functionality
where the difference between the test cases is different test input and
differing expected results.

Features
--------

The Framework provides the following features :

 - Supports Python 2 and Python 3
 - Easy to use

   - Uses a list of dictionaries (or any Iterable of mappings) to define the data for the test cases.
   - Requires only a single generic test function which takes the test case data and executes the test of the functionality.
   - Can decorate a entirely empty ``unittest.TestCase`` class - no boiler plate coded neede within the class.
   - Using the default settings, ensures a unique and predictable set of test method names, and useful documentation strings for each test case.
   - The automatically generated test methods work correctly with ``unitest`` module default test detection, loaders, execution and reporting functionality.
   - Supports the use of the normal commandline usage of the ``unittest`` module, including execution of specific test cases.

 - Behind the scenes

   - Automatically generates a test method on a ``unittest.TestCase``, one for each entry the test data list/Iterable.
   - By generating unique documentation strings and test names, ensures useful test result reporting from the ``unittest`` module.
   - By generating multiple test methods, ensures test separation so that testing continues after a test failure.

 - Also

   - Allows for customisation of the name and the documentation strings of the generated test method, using any of the data from the relevant test_case.
   - Provides additional decorators allowing the application of ``unittest`` test method decorators (``skip``, ``skipIf`` etc) to one or more of the automatically generated test cases. Can also apply your own arbritary test method decorators to the generated test case methods.
   - Can combine Automatically generated test methods and explicitly provided test method on the same ``unittest.TestCase`` class.

See :doc:`Using the Framework <using>` for full details of how to use the Framework, including how to customise the Framework, and how to apply decorators to the generated test methods.

See :doc:`Why Use the Framework <WhyUse>` for a more detailed comparison of the Framework against other traditional ways of using the unittest module to acheive the same multiple test cases for the same functionality item with different data.

------------
Installation
------------

Installation is very simple :

.. code-block:: bash

    $ pip install repeatedtestframework

To upgrade an existing installation use

.. code-block:: bash

    $ pip install --upgrade repeatedtestframework

---------------
Getting Started
---------------

The following code snippet will illustrate the simplest use of the Framework to excute a small number of test case
against the multiplication operation - a trivial example which is still illustrative of the key points.

.. code-block:: python

    from RepeatedTestFramework import RepeatedTestFramework

    def test_method_wrapper(index, a, b, result):
        def test_method(self):
            """The actual test method which gets replicated"""
            self.assertEqual( a * b, result)
        return test_method_wrapper

    @RepeatedTestFramework(
        test_name = 'test_multiplication',
        test_method = test_method_wrapper,
        test_input = [  {'a':1, 'b';2, 'result':2 },
                        {'a':2, 'b':2, 'result':4 },
                        {'a':3, 'b':2, 'result':6 },
                        {'a':3, 'b':4, 'result':11 } ] )
    class TestCases(unittest.TestCase):
        pass

Although the exaample above is trivial, it does illustrate the key features of the framework as noted.

 - The data to be used is provided as a list of dictionaries;  the ``input_data`` attribute on the RepeatdTestFramework decorator.
 - A ``test_name`` attrribute is provided - which is a human readable string which is included verbatim into the test method name - as such it can only include alphabetic, numeric and underscaore (`_`) characters.
 - Regardless of the number of test data items the decorator only needs a a single test execution method (``test_method`` in the example) is required. The Framework replicates this method into the multiple test methods on the decorated class.
 - The framework does require the test function to be wrapped in method which accepts the attributes from the ``input_data`` iterator - in the example below this wrapping function is ``test_method_wrapper``. As shown in the example, the wrapper function it does not need to do anything at all other than wrap the test function, and accept the test data as a set of argumnents which can then be used by the wrapped test function.
 - The ``unittest.TestCase`` class being decorated by the Framework can be entirely empty (as in the example), or it can include set Up and clear down methods as required by the test cases, or it could even include one or more `hand-written` test case methods (so long as the method names do not clash).


-------------------
Further Information
-------------------

- `Full Documentation`_
- `On PyPi (Python Package Index)`_
- `Source code on GitHub`_

----------------------
Troubleshooting & Bugs
----------------------

.. note::
  Every care is taken to try to ensure that this code comes to you bug free.
  If you do find an error - please report the problem on :

    - `GitHub Issues`_
    - By email to : `Tony Flury`_

-------
License
-------

This software is covered by the provisions of `Apache Software License 2.0`_ License.



.. _Github Issues: http://github.com/TonyFlury/repeatedtestframework/issues/new
.. _Tony Flury: mailto:anthony.flury@btinternet.com?Subject=repeatedtestframework%20Error

.. _Full Documentation: http://repeatedtestframework.readthedocs.org/en/latest/
.. _On PyPi (Python Package Index): https://pypi.python.org/pypi/repeatedtestframework
.. _Source code on GitHub: http://github.com/TonyFlury/repeatedtestframework
.. _Apache Software License 2.0: http://repeatedtestframework.readthedocs.org/en/latest/LICENSE.rst
.. _unittest for Python 2.7: https://docs.python.org/2.7/
.. _unittest for Python 3.5: https://docs.python.org/3.5/


.. _`top`:

=================================
Using the Repeated Test Framework
=================================


The Framework is very easy to use; see the following sections for a full guide:

    * :ref:`SimpleUsage`
    * :ref:`Customisation`
    * :ref:`Decorators`


A :doc:`full-spec`  is available.


.. _`SimpleUsage`:

------------
Simple Usage
------------


This first example illustrates using the Framework with default settings.

.. code-block:: python
    :linenos:
    :caption: Example simple usage
    :name: UsingExample1

    from GenerateTestMethods import GenerateTestMethods

    def test_method_wrapper(index, a, b, result):
        """Wrapper for the test_method"""
        def test_method(self):
            """The actual test method which gets replicated"""
            self.assertEqual( a * b, result)
        return test_method_wrapper

    @GenerateTestMethods(
        test_name = 'test_multiplication',
        test_method = test_method_wrapper,
        test_cases = [
                {'a':1,'b':2, 'result':2 },
                {'a':2,'b':2, 'result':4 },
                {'a':3,'b':2, 'result':6 },
                {'a':3,'b':4, 'result':11 },]
            )
    class TestCases(unittest.TestCase):
        pass

A few things to note about this simple example :

    1. The actual functionality under test is defined by the ``test_method`` function on lines 5-7. It is wrapped by the ``test_method_wrapper`` (lines 3-8); this wrap is neccessary as since the ``test method`` can only accept the self paramter, so the outer layer is required to give definition to the ``input`` and ``expected_results`` names which ``test_method`` needs.
    #. The ``test_cases`` (lines 14 to 17) which defines the data for each separate test case is here is a list of dictionaries, but it could be any python Iterator which conatins a mapping per entry (for instance a generator which creates ordered dicts).
    #. The TestCases class must be a sub class of `unittest.TestCase`_, as per normal `unittest module`_ usage, but there are no other restrictions. The class could potentially contain other test methods (take care to ensure that method names don't clash), or the class could contain the normal test ``setUp``, ``setUpClass``, ``tearDown`` & ``tearDownClass`` methods to establish or destory the test Fixtures.

The example above is complete and will automatically generate test methods
based on the input data - this is equivalent to the following code
(including the deliberate error) :

.. _`UsingExample1a`:

.. code-block:: python
    :linenos:

    class TestCases(unittest.TestCase):
        def test_000_test_multiplication(self):
            """test_multiplication 000 {'a':1,'b':2,'result':2}"""
            self.assertEqual(1*2, 2)

        def test_001_test_multiplication(self):
            """test_multiplication 001 {'a':2,'b':2,'result':4}"""
            self.assertEqual(2*2, 2)

        def test_002_test_multiplication(self):
            """test_multiplication 002 {'a':3,'b':2,'result':6}"""
            self.assertEqual(2*2, 6)

        def test_003_test_multiplication(self):
            """test_multiplication 003 {'a':3,'b':4,'result':11}"""
            self.assertEqual(3*4, 1)

See :doc:`full-spec` for full details on the paramters and their usage

Return :ref:`to the top<top>`

------

.. _`Customisation`:

-------------
Customisation
-------------

The Framework has a number of options for customisation :

 - :ref:`Method name & Documentation strings`:
 - :ref:`Test Case Attributes`:

.. _`Method name & Documentation strings`:

Method names & Documentation strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each test method is provided with a generated method name, and documentation string. The method names and documentation string are central to documenting your test suites and test results. Both the method name and documentation strings are generated in a predicatble fashion. The predictable method names means that individual test methods can be selected from the command line to be executed.

The format of the method name is controlled by the ``method_name_template`` attribute, and the format of this documentation string is controlled by using the ``method_doc_template`` string; both of these attributes are python format string (i.e. using the ``format`` method - see `Format specification`_ for full details).

The defaults for these attributes are :

    - ``method_name_template`` : "test_{index:03d}_{test_name}"
    - ``method_doc_template`` : "{test_name} {index:03d}: {test_data}"


Both the ``method_name_template`` and ``method_doc_template`` can contain the following keys :

    - ``test_name`` : the value is the string passed into `test_name`` attrribute.
    - ``index`` : the value is the start from zero index of the appropriate entry in the `test_case` iterator for this test case
    - ``test_data`` : the value is the appropriate entry within the test_cases iterator for this test case.

Within the format strings the individual keys from the ``test_data`` dictionary can be accessed using the normal subscript notation (eg. :

.. code-block:: pycon

    >>> "_{test_data[a]:03d}_".format(test_data={'a':1, 'b':2})
    "_001_

.. warning::

   Unless you are using a custom dictionary and with an alternative ``__str__`` method, the ``test_data`` key **must not** be used within the ``method_name_template`` format string.  During the formatting process, ``test_data`` value is converted to the string repesentation of a dictionary, and therefore by default it will contain characters which are not legal characters within a method name. It is possible to extract the individual data items within the ``test_data`` value using the format string subscript feature (illustrated above), but care still needs to be taken to ensure that any data extracted is valid for inclusion in a method name (e.g. only alphanumeric characters, or the underscore character `_`.

.. _`Test Case Attributes`:

Test Case Attributes
^^^^^^^^^^^^^^^^^^^^
As mentioned above the ``test_cases`` attribute is an iterator of mappings (in :ref:`UsingExample1` it is a list of dictionaries). The key/value pairs within those dictionaries are as a minimum the input and expected results, but they could be anything you would find useful, and the key's could be any string value which is a legal identifier (i.e. starts with a alphabetic character, and only contains alphabetic, numeric or underscores `_` characters). Examples of extra uses for these key/value sets might be :

    - To customise the error messages from the aseert calls within your test method; include in each dictionary an extra data item which is your customised message.
    - To add a version of the test_data which can be used within your method name; include the usable form as an extra data item, and include a reference to that key within the ``method_name_template``
    - The ability to include arbitary key,value pairs within the data dictionary could be useful when using the :ref:`Decorators`


See :doc:`full-spec` for full details on the paramters and their usage


Return :ref:`to the top<top>`

------

.. _`Decorators`:

-------------------------
Decoratoring test methods
-------------------------

The `unittest module`_ includes a number of decorators that can be used to change the standard behaviour. These are :

    - `unittest.skip`_
    - `unittest.skipIf`_
    - `unittest.skipUnless`_
    - `unittest.expectedFailure`_

These decorators can still be used to decorate the entire TestCase class (either before or after the GenerateTestMethods is used). However since the test methods are automatically generated, it is not possible to use the `unittest module`_ decorators listed above.

The GenerateTestMethods has provided it's own equivalents which allow the selection of the test methods to be selected by using the test data itself :

    - skip : skip the identified test method or methods
            *@repeatedtestframework*.skip( reason, criteria = lambda test_data : True )
    - skipIf : skip the identified test method or methods if the condition is True
            *@repeatedtestframework*.skip( reason, condition, criteria = lambda test_data : True )
    - skipUnless : skip the identified test method or methods if the condition is False
            *@repeatedtestframework*.skip( reason, condition, criteria = lambda test_data : True )
    - expectedFailure : mark the identified test method or methods as expecting to fail.
            *@repeatedtestframework*.skip( criteria = lambda test_data : True )

The ``skip`` decorator is shown in the example below - all of the other decorators listed above work in the same way.

.. code-block:: python
    :linenos:
    :caption: Decorator Example Usage
    :name: DecoratorExample

    from GenerateTestMethods import GenerateTestMethods
    from GenerateTestMethods import skip

    def test_method_wrapper(index, a, b, result):
        """Wrapper for the test_method"""
        def test_method(self):
            """The actual test method which gets replicated"""
            self.assertEqual( a * b, result)
        return test_method_wrapper

    @skip("This is a very boring test",
        criteria = lambda test_data : test_data['a'] == 1)
    @GenerateTestMethods(
        test_name = 'test_multiplication',
        test_method = test_method_wrapper,
        test_cases = [
                {'a':1,'b':2, 'result':2 },
                {'a':2,'b':2, 'result':4 },
                {'a':3,'b':2, 'result':6 },
                {'a':3,'b':4, 'result':11 },]
            )
    class TestCases(unittest.TestCase):
        pass

In the example above lines 11-13 demonstrate the use of the skip decorator from the framework - comparing it to the `unittest.skip` decorator the call above has the extra ``criteria`` paramter. The ``criteria`` parameter is a callable, which is invoked once for each generated test_method and is passed as a dictionary all of relevant test data for that test method, and also the test method index as an extra key. If the callable returns True for a particular test method (which it will do for the test method created for the first row of the ``test_cases`` parameter) then the `unittest.skip`_ decorator will be applied to that specific test method.

The following invocation of the skip decorator would be equivalent in the :ref:`DecoratorExample` above;

.. code-block:: python

    @skip("This is a very boring test",
        criteria = lambda test_data : test_data['index'] == 0)

The default for the ``criteria`` paramater for all 4 decorators is a simple callable that returns True in all cases. Therefore as a default the decorator applies to all the generated test methods.

As mentioned above :ref:`Customisation`, the test data can include arbitrary keys, which may not have any direct use in the test execution itself, but as shown above since the ``criteria`` callable is passed the full test data dictionary for each test method, a key could be included in the dictionary which is used to solely control the application of the decorator

.. code-block:: python
    :linenos:
    :caption: Key use by Decorator
    :name: DecoratorAndDataKeyExample

    from GenerateTestMethods import GenerateTestMethods
    from GenerateTestMethods import skip

    def test_method_wrapper(index, a, b, result):
        """Wrapper for the test_method"""
        def test_method(self):
            """The actual test method which gets replicated"""
            self.assertEqual( a * b, result)
        return test_method_wrapper

    @skip("This is a very boring test",
        criteria = lambda test_data : test_data.get('skip', False))
    @GenerateTestMethods(
        test_name = 'test_multiplication',
        test_method = test_method_wrapper,
        test_cases = [
                {'a':1,'b':2, 'result':2 },
                {'skip':True, 'a':2,'b':2, 'result':4 },
                {'a':3,'b':2, 'result':6 },
                {'a':3,'b':4, 'result':11 },]
            )
    class TestCases(unittest.TestCase):
        pass

In this example only the 2nd test case (a = 2, b = 2, result = 4) will have the `unittest.skip`_ decorator applied to as only that test case has a test case key of 'skip'. All of the other test cases will not have the decorator applied, as in those dictionaries, the 'skip' key is missing, and the criteria test uses a default of False in the case of a missing 'skip' key (line 12)

The framework also provides a method for applying any decorator method to the automatically generated test methods

.. code-block:: python

    *@repeatedtestframework*DecorateTestMethod(
                       criteria=lambda test_data: True, decorator_method=None,
                       decorator_args=None, decorator_kwargs=None)


 - ``criteria`` : as above a callable which is called for each test method, and is passed the test data dictionary appropriate to that method with the index added. The criteria should return True for all test_method to which the decorator should be applied, and False in all other cases.
 - ``decorator_method`` : A callable which is the actual method with which the test method should be generated
 - ``decorator_args``: A tuple for the positional arguments for the decorator_method
 - ``decorator_kwargs``: A dictionary for the kwargs argument for the decorator_method


The example below shows using the DecorateTestMethod call as an alternative to the `skip` method as shown in :ref:`DecoratorExample`

.. code-block:: python
    :linenos:
    :caption: Example of the DecorateTestMethod
    :name: DecorateTestMethodExample

    import unittest

    from GenerateTestMethods import GenerateTestMethods
    from GenerateTestMethods import DecorateTestMethod

    def test_method_wrapper(index, a, b, result):
        """Wrapper for the test_method"""
        def test_method(self):
            """The actual test method which gets replicated"""
            self.assertEqual( a * b, result)
        return test_method_wrapper


    @DecorateTestMethod( decorator_method = unittest.skip,
                         decorator_kwargs = {'reason': "This is a very boring test"},
                         criteria = lambda test_data : test_data.get('skip', False) )
    @GenerateTestMethods(
        test_name = 'test_multiplication',
        test_method = test_method_wrapper,
        test_cases = [
                {'a':1,'b':2, 'result':2 },
                {'skip':True, 'a':2,'b':2, 'result':4 },
                {'a':3,'b':2, 'result':6 },
                {'a':3,'b':4, 'result':11 },]
            )
    class TestCases(unittest.TestCase):
        pass

The two examples :ref:`DecorateTestMethodExample` and ref:`DecoratorExample` are functionally equivalent, but the former version (using the `skip` decorator is recommended for readability).

.. note::

    Since the `DecorateTestMethod` can only access the test methods once they have been created, it must be invoked **after** the `GenerateTestMethods` decorator (i.e. it must appear before ``GenerateTestMethods`` in the decorator chain reading from the top).

.. note::

    Using the decorators supplied by the framework will only apply the relevant `unittest module`_ decorator to the relevant test methods generated by the framework - any other test case which have been explicitly written in the  `unittest.TestCase`_ class will be ignored by the decorators discussed above. Of course the usual `unittest module`_ decorators can be applied explicitly to those explicitly written test cases.


See :doc:`full-spec` for full details on the paramters and their usage

Return :ref:`to the top<top>`

.. _Format specification: https://docs.python.org/3.5/library/string.html#formatspec
.. _unittest module: https://docs.python.org/3.5/library/unittest.html
.. _unittest.TestCase: https://docs.python.org/3.5/library/unittest.html#test-cases
.. _unittest.skip: https://docs.python.org/3.5/library/unittest.html#unittest.skip
.. _unittest.skipIf: https://docs.python.org/3.5/library/unittest.html#unittest.skipIf
.. _unittest.skipUnless: https://docs.python.org/3.5/library/unittest.html#unittest.skipUnless
.. _unittest.expectedFailure: https://docs.python.org/3.5/library/unittest.html#unittest.expectedFailure
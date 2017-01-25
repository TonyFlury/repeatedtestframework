#!/usr/bin/env python
# coding=utf-8
"""
# repeatedtestframework : Functionality to support the creation of multiple
                          test cases with the Unittest framwork

Summary :
    Helper functionality to reduce the amount of boiler plate or repeated
    code which is implemented when the same functionality is tested multiple
    times with the different data.

Use Case :
    As a user I want to reduce the amount of boiler plate and repeated code
    so as to reduce errors.

Testable Statements :
    ...
"""
import six as _six
import unittest

from .version import __version__ as __version__

__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '17 Jan 2017'

# Python 3 introduced the collections.abc module
if _six.PY2:
    from collections import Iterable, Mapping
else:
    from collections.abc import Iterable, Mapping


class RepeatedTestFramework(object):
    """A decorator to construct repeated test methods """

    def __init__(self, test_name='',
                 test_method=None,
                 test_cases=None,
                 method_name_template="test_{index:03d}_{test_name}",
                 method_doc_template="{test_name} {index:03d}: "
                                     "{input} {expected_result}"
                 ):
        """A decorator to construct repeated test methods
            :param test_name : A valid paython identifier for these tests
            :param test_method : The actual test method to execute
            :param test_cases : A list of tuples defining the actual test cases
        """
        if not self._isidentifier(test_name):
            raise ValueError(
                'test_name value not able to be used in a method name')
        else:
            self._test_name = test_name

        if not (callable(test_method)):
            raise TypeError('test_method is not callable')
        else:
            self._method = test_method

        if not (isinstance(test_cases, Iterable)):
            raise TypeError('test_cases is not a valid Iterator')
        else:
            self._test_cases = test_cases

        self._method_name_template = method_name_template
        self._method_doc_template = method_doc_template

    @staticmethod
    def _isidentifier(name):
        """returns True only if strng can be included into a method name"""
        if not name:
            return False
        else:
            return all(
                True if (c.isalnum() or c == "_") else False for c in name)

    def __call__(self, cls):

        if not issubclass(cls, unittest.TestCase):
            raise TypeError(
                'Invalid type: Decorator target is not '
                'unittest.TestCase subclass')

        cls._RTF_DECORATED = True
        cls._RTF_METHODS = {}

        for index, case in enumerate(self._test_cases):
            if not isinstance(case, Mapping):
                raise TypeError(
                    "test_cases item {} is not a Mapping".format(index))

            test_data = {'index': index}
            test_data.update(case)

            test_method = self._method(**test_data)

            test_method.__name__ = self._method_name_template.format(
                test_name=self._test_name, **test_data)
            test_method.__doc__ = self._method_doc_template.format(
                test_name=self._test_name, **test_data)
            setattr(cls, test_method.__name__, test_method)
            cls._RTF_METHODS[test_method.__name__] = test_data
        return cls


# noinspection PyPep8Naming
def DecorateTestMethod(criteria=None, decorator_method=None,
                       decorator_args=None, decorator_kwargs=None):
    """Allow for conditional decoration of any generated test method

      :param criteria: A callable which will return boolean. The callable is
                        passed a relevant item from test_input list
                        (from the ``RepeatedTestFramework``) call. The
                        ``criteria`` should return a boolean value which
                        determines if the test method which will be generated
                        for this test_input item should be deoctorated or not.
      :param decorator_method: A decorator called which will be used to
                               decorate the test_method.
      :param decorator_args :  A typle of the positional arguments passed to
                               the ``decorator_method`` callable.
      :param decorator_kwargs : A dictionary of keyword arguments passed to
                                the ``decorator_method`` callable.
    """
    # Double check the attribute validity
    if not (callable(criteria)):
        raise TypeError('criteria is not callable')

    if not (callable(decorator_method)):
        raise TypeError('decorator_method is not callable')

    if decorator_args is None:
        decorator_args = ()

    if decorator_kwargs is None:
        decorator_kwargs = {}

    def class_wrapper(cls):
        """ Function returned by the decorator to wrap the class
            :param cls: An instance of the RepeatedTestFramework class
        """

        # noinspection PyProtectedMember
        def _generated_methods(cls_):
            for method_name, test_data in cls_._RTF_METHODS.items():
                yield method_name, test_data, getattr(cls_, method_name)

        # Check the validity of the call arguments
        if not hasattr(cls, '_RTF_DECORATED'):
            raise TypeError(
                'Incorrect usage; DecorateTestMethod can only be used to '
                'decorate a TestCase class which is already decorated '
                'by RepeatedTestFramework')

        for name, data, method in _generated_methods(cls):
            if criteria(data):
                if decorator_args or decorator_kwargs:
                    new_method = decorator_method(
                        *decorator_args,
                        **decorator_kwargs)(method)
                else:
                    new_method = decorator_method(method)

                new_method.__name__ = name
                new_method.__doc__ = method.__doc__
                setattr(cls, name, new_method)
        return cls

    return class_wrapper


# --------------------------------------------------------------------------
# A set of shortcuts for common test method decorators
#
# skip - skip decorator of methods based on test data
# skipIf - skipIf decorator of methods based on test data
# skipUnless - skipUnless decorator of methods based on test data
# expectedFailure  - expectedFailure decorator of methods based on test data
#

def skip(reason, criteria=lambda x: True):
    """Shortcut Decorator to allow skip decorator of methods based on test data
        :param reason - the reason string to be pasded to the decorator
        :param criteria - A callable which will return True if a given method
                        should be decorated. This is the same as the criteria
                        attribute to the DecorateTestMethod
                        By default all methods will be skipped
    """
    return DecorateTestMethod(criteria=criteria,
                              decorator_method=unittest.skip,
                              decorator_kwargs={'reason': reason})


# noinspection PyPep8Naming
def skipIf(condition, reason, criteria=lambda x: True):
    """Shortcut Decorator to allow skipIf decorator of methods based on test data
        :param condition - Skip the decorated test if condition is true
        :param reason - the reason string to be passed to the decorator
        :param criteria - A callable which will return True if a given method
                        should be decorated. This is the same as the criteria
                        attribute to the DecorateTestMethod
                        By default all methods will be skipped
    """
    if condition:
        return DecorateTestMethod(criteria=criteria,
                                  decorator_method=unittest.skipIf,
                                  decorator_kwargs={'condition': condition,
                                                    'reason': reason})
    else:
        return lambda x: x


# noinspection PyPep8Naming
def skipUnless(condition, reason, criteria=lambda x: True):
    """Shortcut Decorator to allow skipunless decoration based on test data
        :param condition - Skip the decorated test unless the condition is true
        :param reason - the reason string to be passed to the decorator
        :param criteria - A callable which will return True if a given method
                        should be decorated. This is the same as the criteria
                        atrribute to the DecorateTestMethod. By default all
                        methods will be decorated
    """
    if not condition:
        return DecorateTestMethod(criteria=criteria,
                                  decorator_method=unittest.skipUnless,
                                  decorator_kwargs={'condition': condition,
                                                    'reason': reason})
    else:
        return lambda x: x


# noinspection PyPep8Naming
def expectedFailure(criteria=lambda x: True):
    """Shortcut allow expectedFailure to decorate methods based on test data
        :param criteria - A callable which will return True if a given method
                        should be decorated. This is the same as the criteria
                        atrribute to the DecorateTestMethod
                        By default all methods will be skipped
    """
    return DecorateTestMethod(criteria=criteria,
                              decorator_method=unittest.expectedFailure)

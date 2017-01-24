#!/usr/bin/env python
# coding=utf-8
"""
# Repeated Test Framework : Test Suite for test_repeatedtestframework.py

Summary : 
    <summary of module/class being tested>
Use Case : 
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I <Boolean statement>
    ....
"""

import unittest
import six
from repeatedtestframework import RepeatedTestFramework
from repeatedtestframework import expectedFailure as RTFExpectedFailure
from repeatedtestframework import __version__ as RTFversion

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '19 Jan 2017'

def test_method_wrapper(index, a, b, result):
    def test_method(self):
        self.assertEqual( a*b, result)
    return test_method


#@DecorateTestMethod(
#        criteria=lambda item: item['a'] == 1,
#        decorator_method=unittest.skip,
#        decorator_kwargs={'reason':'Skipping all tests with a == 1'}
#)
#@RTFExpectedFailure( criteria=lambda item: (item['a'] == 3) and (item['b'] == 4),
#                )
#@RepeatedTestFramework(
#        test_name = 'Integer_multiplication',
#        test_method= test_method_wrapper,
#        test_cases=[
#            {'a':1, 'b':2, 'result':2},
#            {'a': 2, 'b': 2, 'result': 4},
#            {'a': 3, 'b': 2, 'result': 6},
#            {'a': 3, 'b': 4, 'result': 11},
#            ],
#        method_doc_template="{test_name} {index}: {a}*{b} = {result}"
#)
#class TestCaseClass(unittest.TestCase):
#    pass


class TestErrorChecking(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_010_InvalidTestNameEmpty(self):
        """Test that an empty test_name attribute is rejected"""
        with six.assertRaisesRegex( self, AttributeError, r'.*test_name.*'):
            # Provide dummy values for test_method & test_cases
            dec = RepeatedTestFramework(
                test_name='',
                test_method=lambda x:x,
                test_cases=[{'dummy':None}] )

    def test_011_InvalidTestNameBadCharacters(self):
        """Test that an invalid test_name attribute is rejected"""
        with six.assertRaisesRegex( self, AttributeError, r'.*test_name.*'):
            dec = RepeatedTestFramework(
                test_name='this is an invalid name,#&',
                test_method = lambda x: x,
                test_cases = [{'dummy': None}] )

    def test_019_ValidTestName(self):
        """Test that an valid test_name attribute is accepted"""
        dec = RepeatedTestFramework(
            test_name='this_is_a_valid_name',
            test_method = lambda x: x,
            test_cases = [{'dummy': None}] )

    def test_020_InvalidTestMethodNotCallable(self):
        """Confirm that an invalid test_method is rejected"""
        with six.assertRaisesRegex( self, AttributeError, r'.*test_method.*'):
            dec = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method = None,
                test_cases = [{'dummy': None}] )

    def test_025_ValidTestMethod(self):
        """Confirm that an valid test_method is accepted"""
        dec = RepeatedTestFramework(
            test_name='this_is_a_valid_name',
            test_method = lambda x:x,
            test_cases = [{'dummy': None}] )

    def test_030_InValidTestCasesNone(self):
        """Confirm that an valid test_method is accepted"""
        with six.assertRaisesRegex( self, AttributeError, r'.*test_cases.*'):
            dec = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method = lambda x:x,
                test_cases = None )

    def test_031_InValidTestCasesInt(self):
        """Confirm that an valid test_method is accepted"""
        with six.assertRaisesRegex( self, AttributeError, r'.*test_cases.*'):
            dec = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method = lambda x:x,
                test_cases = 1 )

    def test_035_InValidTestCasesNoMapping(self):
        """Confirm that an valid test_method is accepted"""
        with six.assertRaisesRegex( self, AttributeError, r'.*test_cases.*'):
            dec = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method = lambda x:x,
                test_cases = 1 )


def load_tests(loader, tests=None, pattern=None):
    classes = [TestErrorChecking]
    suite = unittest.TestSuite()
    for test_class in classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    ldr = unittest.TestLoader()

    test_suite = load_tests(ldr)

    unittest.TextTestRunner(verbosity=2).run(test_suite)

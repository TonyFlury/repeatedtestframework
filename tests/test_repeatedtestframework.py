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
import inspect

from repeatedtestframework import RepeatedTestFramework
from repeatedtestframework import DecorateTestMethod
from repeatedtestframework import skip
from repeatedtestframework import skipIf
from repeatedtestframework import skipUnless
from repeatedtestframework import expectedFailure

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '19 Jan 2017'


class TestErrorChecking(unittest.TestCase):
    def setUp(self):
        # Empty class that can be decorated
        class EmptyClass(unittest.TestCase):
            pass

        self.cls_ = EmptyClass

    # noinspection PyUnusedLocal
    def test_010_InvalidTestNameEmpty(self):
        """Test that an empty test_name attribute is rejected"""
        with six.assertRaisesRegex(self, ValueError, r'.*test_name.*'):
            # Provide dummy values for test_method & test_cases
            dec = RepeatedTestFramework(
                test_name='',
                test_method=lambda x: x,
                test_cases=[{'dummy': None}])

    # noinspection PyUnusedLocal
    def test_011_InvalidTestNameBadCharacters(self):
        """Test that an invalid test_name attribute is rejected"""
        with six.assertRaisesRegex(self, ValueError, r'.*test_name.*'):
            dec = RepeatedTestFramework(
                test_name='this is an invalid name,#&',
                test_method=lambda x: x,
                test_cases=[{'dummy': None}])

    # noinspection PyUnusedLocal
    def test_019_ValidTestName(self):
        """Test that an valid test_name attribute is accepted"""
        dec = RepeatedTestFramework(
            test_name='this_is_a_valid_name',
            test_method=lambda x: x,
            test_cases=[{'dummy': None}])

    # noinspection PyUnusedLocal
    def test_020_InvalidTestMethodNotCallable(self):
        """Confirm that an invalid test_method is rejected"""
        with six.assertRaisesRegex(self, TypeError, r'.*test_method.*'):
            dec = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method=None,
                test_cases=[{'dummy': None}])

    # noinspection PyUnusedLocal
    def test_025_ValidTestMethod(self):
        """Confirm that an valid test_method is accepted"""
        dec = RepeatedTestFramework(
            test_name='this_is_a_valid_name',
            test_method=lambda x: x,
            test_cases=[{'dummy': None}])

    # noinspection PyUnusedLocal
    def test_030_InValidTestCasesNone(self):
        """Confirm that an in valid test_case attribute is rejected"""
        with six.assertRaisesRegex(self, TypeError, r'.*test_cases.*'):
            dec = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method=lambda x: x,
                test_cases=None)

    # noinspection PyUnusedLocal
    def test_031_InValidTestCasesInt(self):
        """Confirm that an in valid test_case attribute is rejected"""
        with six.assertRaisesRegex(self, TypeError, r'.*test_cases.*'):
            dec = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method=lambda x: x,
                test_cases=1)

    # noinspection PyUnusedLocal
    def test_035_InValidTestCasesNoMapping(self):
        """Confirm that an in valid test_case item is rejected"""
        with six.assertRaisesRegex(self, TypeError, r'.*test_cases.*'):
            case_class = RepeatedTestFramework(
                test_name='this_is_a_valid_name',
                test_method=lambda x: x,
                test_cases=[(1, 1)])(self.cls_)


class TestMethodGeneration(unittest.TestCase):
    def setUp(self):

        # noinspection PyShadowingBuiltins,PyUnusedLocal
        def wrapper(index, input, expected_result):
            # noinspection PyShadowingNames
            def test_method(self):
                self.assertEqual(input + 1, expected_result)

            return test_method

        self.cls_ = type('EmptyClass', (unittest.TestCase, object,), {})
        self.test_method_ = wrapper

    @staticmethod
    def _generate_test_method_name(test_name, num_test_cases):
        for i in range(0, num_test_cases):
            yield "test_{index:03d}_{test_name}".format(index=i,
                                                        test_name=test_name)

    @staticmethod
    def _generate_test_data(num_test_cases):
        for i in range(0, num_test_cases):
            yield {'input': i, 'expected_result': i + 1}

    def test_010_MethodGenerationTestNames(self):
        """Test that test_method with the correct names have been generated"""
        test_name = "MethodGeneration"
        num_test_cases = 3
        case_cls_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=self._generate_test_data(num_test_cases)
        )(self.cls_)

        # Loop around the generated names
        for index, test_method_name in enumerate(
                self._generate_test_method_name(
                    test_name,
                    num_test_cases)):
            # Grab the actual method object from the class
            method = getattr(case_cls_, test_method_name, None)

            # Make sure it isn't None
            self.assertIsNotNone(method,
                                 msg='Failed to generate the test_method'
                                     ' name ({name}) for index {i}'.format(
                                                name=test_method_name,
                                                i=index))

            # Make sure the method object is actually a method
            self.assertTrue(inspect.ismethod(method) or
                            inspect.isfunction(method),
                            "Item ({name}) is not a function".format(
                                name=test_method_name))

    # noinspection PyTypeChecker
    def test_020_MethodGenerationDocStrings(self):
        """Test that test_method have the correct documentation strings"""
        test_name = "MethodGeneration"
        num_test_cases = 3
        # Wrap the class with the decorator
        case_cls_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=self._generate_test_data(num_test_cases)
        )(self.cls_)
        # loop around test names, and associated data
        for index, test_info in enumerate(zip(
                self._generate_test_method_name(test_name, num_test_cases),
                self._generate_test_data(num_test_cases))):

            # Extract associated name and data - and get the method object
            test_method_name, test_data = test_info[0], test_info[1]
            method = getattr(case_cls_, test_method_name, None)

            self.assertEqual(method.__doc__,
                             "{test_name} {index:03d}: {input} "
                             "{expected_result}".format(
                                 test_name=test_name,
                                 index=index,
                                 input=test_data['input'],
                                 expected_result=test_data['expected_result']))


class TestMethodExecution(unittest.TestCase):
    def setUp(self):

        # noinspection PyUnusedLocal
        def wrapper(index, a, b):
            # noinspection PyShadowingNames
            def test_method(self):
                self.assertEqual(a + 1, b)

            return test_method

        self.cls_ = type('EmptyClass', (unittest.TestCase, object), {})
        self.test_method_ = wrapper

    @staticmethod
    def _run_tests(test_class):
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_class)
        result = unittest.result.TestResult()
        suite.run(result=result)
        summary = result.testsRun, len(result.errors), len(
            result.failures), len(result.skipped), len(
            result.expectedFailures), len(result.unexpectedSuccesses)

        return summary, result

    def test_001_MethodExecution(self):
        """Test that test_method will execute correctly"""
        test_name = "MethodExecution"
        num_test_cases = 3
        # Wrap the class with the decorator
        case_cls_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="{test_name} {index:03d}: {a} {b}")(
            self.cls_)

        summary, result = self._run_tests(case_cls_)

        self.assertEqual((num_test_cases, 0, 0, 0, 0, 0), summary)

    def test_010_MethodExecutionOneFail(self):
        """Confirm that a test failure does fail correctly"""
        test_name = 'MethodExecution'
        num_test_cases = 3
        # Wrap the class with the decorator - force one error from 3
        case_cls_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 3}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")(
            self.cls_)

        summary, result = self._run_tests(case_cls_)

        self.assertEqual((num_test_cases, 0, 1, 0, 0, 0), summary)

        self.assertEqual(result.failures[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_002_MethodExecution'
                         )

    def test_015_MethodExecutionTwoFail(self):
        """Confirm that more than one test failure does fail correctly"""
        test_name = 'MethodExecution'
        num_test_cases = 3
        # Wrap the class with the decorator - force one error from 3
        case_cls_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 4},
                        {'a': 3, 'b': 3}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")(
            self.cls_)

        summary, result = self._run_tests(case_cls_)

        self.assertEqual((num_test_cases, 0, 2, 0, 0, 0), summary)

        self.assertEqual(result.failures[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_001_MethodExecution'
                         )
        self.assertEqual(result.failures[1][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_002_MethodExecution'
                         )

    # noinspection PyUnusedLocal
    def test_100_DecoratorsErrorsInvalidCriteria(self):
        """Confirm that the criteria attribute is checked to be a callable"""
        with six.assertRaisesRegex(self, TypeError,
                                   r'.*criteria.*not callable.*'):
            skip_dec = DecorateTestMethod(
                criteria=None,
                decorator_method=unittest.skip,
                decorator_kwargs={'reason': 'Skipped because a == 1'})

    # noinspection PyUnusedLocal
    def test_101_DecoratorsErrorsInvalidDecoratorMethod(self):
        """Confirm that the decorator_method attribute is callable"""
        with six.assertRaisesRegex(self, TypeError,
                                   r'.*decorator_method.*not callable.*'):
            skip_dec = DecorateTestMethod(
                criteria=lambda x: x,
                decorator_method=None,
                decorator_kwargs={'reason': 'Skipped because a == 1'})

    # noinspection PyUnusedLocal
    def test_110_DecoratorsOrderErrors(self):
        """Confirm error is generated when decorator used in wrong order"""
        skip_dec = DecorateTestMethod(
            criteria=lambda data: data['a'] == 1,
            decorator_method=unittest.skip,
            decorator_kwargs={'reason': 'Skipped because a == 1'})

        with six.assertRaisesRegex(self, TypeError,
                                   r'Incorrect usage; DecorateTestMethod.*'):
            case_cls_ = skip_dec(self.cls_)

    def test_120_SkipTest(self):
        """Confirm that the DecorateTestMethod can make a method be skipped"""
        test_name = 'MethodExecution'
        skip_dec = DecorateTestMethod(
            criteria=lambda data: data['a'] == 1,
            decorator_method=unittest.skip,
            decorator_kwargs={'reason': 'Skipped because a == 1'})

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = skip_dec(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped a=1, index = 0..
        self.assertEqual((3, 0, 0, 1, 0, 0), summary)
        self.assertEqual(result.skipped[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_000_MethodExecution'
                         )

    def test_130_ChainingDecorators(self):
        """Confirm that the DecorateTestMethod can be chained"""
        test_name = 'MethodExecution'
        expected_fail = DecorateTestMethod(
            criteria=lambda data: data['a'] == 3,
            decorator_method=unittest.expectedFailure,
        )

        skip_dec = DecorateTestMethod(
            criteria=lambda data: data['a'] == 1,
            decorator_method=unittest.skip,
            decorator_kwargs={'reason': 'Skipped because a == 1'})

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 5}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = expected_fail(skip_dec(case_dec_(self.cls_)))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped a=1, index = 0..
        self.assertEqual((3, 0, 0, 1, 1, 0), summary)
        self.assertEqual(result.skipped[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_000_MethodExecution'
                         )
        self.assertEqual(result.expectedFailures[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_002_MethodExecution'
                         )

    def test_140_SkipShortcutTest(self):
        """Confirm that the skip shortcut decorator works as expected"""
        test_name = 'MethodExecution'
        skip_dec = skip(
            criteria=lambda data: data['a'] == 1,
            reason='Skipped because a == 1')

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = skip_dec(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped a=1, index = 0..
        self.assertEqual((3, 0, 0, 1, 0, 0), summary)
        self.assertEqual(result.skipped[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_000_MethodExecution'
                         )

    def test_150_SkipIfShortcutTestConditionTrue(self):
        """Confirm that the skipIf shortcut decorator when condition == True"""
        test_name = 'MethodExecution'
        test_value = 3
        skip_dec = skipIf(
            condition=(test_value >= 2),
            criteria=lambda data: data['a'] == 1,
            reason='Skipped because a == 1')

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = skip_dec(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped a=1, index = 0..
        self.assertEqual((3, 0, 0, 1, 0, 0), summary)
        self.assertEqual(result.skipped[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_000_MethodExecution'
                         )

    def test_155_SkipIfShortcutTestConditionFalse(self):
        """Confirm that skipIf shortcut decorator when condition == False"""
        test_name = 'MethodExecution'
        test_value = 3
        skip_dec = skipIf(
            condition=(test_value > 4),
            criteria=lambda data: data['a'] == 1,
            reason='Skipped because a == 1')

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = skip_dec(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped
        self.assertEqual((3, 0, 0, 0, 0, 0), summary)

    def test_160_SkipUnlessShortcutTestConditionTrue(self):
        """Confirm skipIf shortcut decorator works when condition == True"""
        test_name = 'MethodExecution'
        test_value = 3
        skip_dec = skipUnless(
            condition=(test_value >= 4),
            criteria=lambda data: data['a'] == 1,
            reason='Skipped because a == 1')

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = skip_dec(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped a=1, index = 0..
        self.assertEqual((3, 0, 0, 1, 0, 0), summary)
        self.assertEqual(result.skipped[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_000_MethodExecution'
                         )

    def test_165_SkipUnlessShortcutTestConditionFalse(self):
        """Confirm the SkipUnless decorator works when condition == False"""
        test_name = 'MethodExecution'
        test_value = 3
        skip_dec = skipUnless(
            condition=(test_value >= 2),
            criteria=lambda data: data['a'] == 1,
            reason='Skipped because a == 1')

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = skip_dec(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped
        self.assertEqual((3, 0, 0, 0, 0, 0), summary)

    def test_170_ExpectedFailureShortcutTest(self):
        """Confirm the ExpectedFailure shortcut decorator works as expected"""
        test_name = 'MethodExecution'
        expected_fail = expectedFailure(
            criteria=lambda data: data['a'] == 1)

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 1},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = expected_fail(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped
        self.assertEqual((3, 0, 0, 0, 1, 0), summary)
        self.assertEqual(result.expectedFailures[0][0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_000_MethodExecution'
                         )

    def test_170_ExpectedFailureShortcutTestUnexpecteSuccess(self):
        """Confirm the ExpectedFailure decorator works when the test works"""
        test_name = 'MethodExecution'
        expected_fail = expectedFailure(
            criteria=lambda data: data['a'] == 1)

        case_dec_ = RepeatedTestFramework(
            test_name=test_name,
            test_method=self.test_method_,
            test_cases=[{'a': 1, 'b': 2},
                        {'a': 2, 'b': 3},
                        {'a': 3, 'b': 4}, ],
            method_doc_template="""{test_name} {index:03d}: {a} {b}""")

        case_cls_ = expected_fail(case_dec_(self.cls_))
        summary, result = self._run_tests(case_cls_)

        # Check that the right method has been skipped
        self.assertEqual((3, 0, 0, 0, 0, 1), summary)
        self.assertEqual(result.unexpectedSuccesses[0].id(),
                         'tests.test_repeatedtestframework.'
                         'EmptyClass.test_000_MethodExecution'
                         )


# noinspection PyUnusedLocal
def load_tests(loader, tests=None, pattern=None):
    classes = [TestErrorChecking, TestMethodGeneration, TestMethodExecution]
    suite = unittest.TestSuite()
    for test_class in classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    ldr = unittest.TestLoader()

    test_suite = load_tests(ldr)

    unittest.TextTestRunner(verbosity=2).run(test_suite)

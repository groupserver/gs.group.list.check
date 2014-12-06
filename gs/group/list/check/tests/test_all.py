# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import TestSuite, main as unittest_main
#from gs.group.list.check.tests.validmessagerules import TestXMailerRule
testCases = (TestXMailerRule, )


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for testClass in testCases:
        tests = loader.loadTestsFromTestCase(testClass)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest_main()

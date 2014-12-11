# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import TestSuite, main as unittest_main
from gs.group.list.check.tests.automatic_email_rule import \
    TestAutomaticEmailRule
from gs.group.list.check.tests.blocked_address_rule import \
    TestBlockedAddressRule
from gs.group.list.check.tests.tight_loop_rule import TestTightLoopRule
from gs.group.list.check.tests.x_mailer_rule import TestXMailerRule
testCases = (
    TestAutomaticEmailRule,
    TestBlockedAddressRule,
    TestTightLoopRule,
    TestXMailerRule, )


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for testClass in testCases:
        tests = loader.loadTestsFromTestCase(testClass)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest_main()

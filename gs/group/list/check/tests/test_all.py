# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 E-Democracy.org and contributors
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from unittest import TestSuite, main as unittest_main
from gs.group.list.check.tests.automatic_email_rule import \
    TestAutomaticEmailRule
from gs.group.list.check.tests.blocked_address_rule import \
    TestBlockedAddressRule
from gs.group.list.check.tests.tight_loop_rule import TestTightLoopRule
from gs.group.list.check.tests.x_mailer_rule import TestXMailerRule
from gs.group.list.check.tests.forbidden_rule import TestForbiddenTextRule
from gs.group.list.check.tests.validmessage import TestIsValidMessage
testCases = (
    TestAutomaticEmailRule,
    TestBlockedAddressRule,
    TestTightLoopRule,
    TestXMailerRule,
    TestForbiddenTextRule,
    TestIsValidMessage, )


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for testClass in testCases:
        tests = loader.loadTestsFromTestCase(testClass)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest_main()

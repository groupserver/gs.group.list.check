# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
#from mock import patch
from unittest import TestCase
from zope.component import getGlobalSiteManager
from gs.group.list.check.interfaces import IGSValidMessageRule
from gs.group.list.check.validmessage import (IsValidMessage)
from Products.XWFMailingListManager.emailmessage import IEmailMessage
from .faux import (email, FauxGroup, FauxRuleInvalid, IFauxGroup,
                   FauxRuleValid)


class TestIsValidMessage(TestCase):
    def setUp(self):
        self.fauxGroup = FauxGroup()
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(FauxRuleValid, (IFauxGroup, IEmailMessage),
                            IGSValidMessageRule, 'valid')

    def test_vaid_only(self):
        ivm = IsValidMessage(self.fauxGroup, email)
        self.assertEqual(1, len(ivm.rules))
        r = ivm.validMessage
        self.assertTrue(r)
        r = ivm.statusNum
        self.assertEqual(0, r)

    def test_invalid(self):
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(FauxRuleInvalid, (IFauxGroup, IEmailMessage),
                            IGSValidMessageRule, 'invalid')

        ivm = IsValidMessage(self.fauxGroup, email)
        self.assertEqual(2, len(ivm.rules))
        self.assertEqual([10, 20], [r.weight for r in ivm.rules])

        r = ivm.validMessage
        self.assertFalse(r)

        r = ivm.statusNum
        self.assertEqual(1, r)

        gsm.unregisterAdapter(FauxRuleInvalid, (IFauxGroup, IEmailMessage),
                              IGSValidMessageRule, 'invalid')

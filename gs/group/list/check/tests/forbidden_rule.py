# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and contributors
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
from mock import patch, create_autospec
from unittest import TestCase
from Products.GSGroup import GSGroupInfo
from Products.XWFMailingListManager.emailmessage import EmailMessage
from gs.group.list.check.rules import ForbiddenTextRule


class TestForbiddenTextRule(TestCase):
    'Test the forbidden-text rule'

    def setUp(self):
        self.groupInfo = create_autospec(GSGroupInfo, instance=True)

    def assert_valid_message(self, rule):
        m = 'Invalid message: {0}'
        failMsg = m.format(rule.s['status'])
        self.assertTrue(rule.s['validMessage'], failMsg)

    def assert_invalid_message(self, rule):
        failMsg = 'Valid message: {0}'.format(rule.s['status'])
        self.assertFalse(rule.s['validMessage'], failMsg)

    @patch.object(ForbiddenTextRule, 'mailingList')
    def test_no_forbidden_text(self, ml):
        ml.getValueFor.return_value = ['.*transgress the unwritten rule.*']

        m = EmailMessage("""From: member@example.com
To: group@groups.example.com
Subject: The unwritten rule

This does not contain any forbidden text""")

        rule = ForbiddenTextRule(self.groupInfo, m)
        rule.check()
        self.assert_valid_message(rule)

    @patch.object(ForbiddenTextRule, 'mailingList')
    def test_forbidden_text(self, ml):
        ml.getValueFor.return_value = ['.*transgress the unwritten rule.*']

        m = EmailMessage("""From: member@example.com
To: group@groups.example.com
Subject: The unwritten rule

This message does transgress the unwritten rule.""")

        rule = ForbiddenTextRule(self.groupInfo, m)
        rule.check()
        self.assert_invalid_message(rule)

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
from mock import patch, create_autospec
from unittest import TestCase
from Products.GSGroup import GSGroupInfo
from gs.group.list.check.rules import AutomaticEmailRule


class TestAutomaticEmailRule(TestCase):
    'Test the automatic email rule'

    def setUp(self):
        group = create_autospec(GSGroupInfo, instance=True)
        self.group = group

    def assert_valid_message(self, message):
        failMsg = (
            'Invalid message: {0}, return-path {1} equals {2}').format(
                message.s['status'],
                message.message.get('return-path'),
                '')
        self.assertTrue(message.s['validMessage'], failMsg)

    def assert_invalid_message(self, message):
        failMsg = 'Valid message: {0}'.format(message.s['status'])
        self.assertFalse(message.s['validMessage'], failMsg)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    def test_non_automatic_message_is_valid(self, MockEmailMessage):
        m = MockEmailMessage.return_value
        m.get.return_value = 'realperson@example.com'

        message = AutomaticEmailRule(self.group, m)
        message.check()
        self.assert_valid_message(message)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    def test_automatic_message_is_invalid(self, MockEmailMessage):
        m = MockEmailMessage.return_value
        m.get.return_value = '<>'

        message = AutomaticEmailRule(self.group, m)
        message.check()

        self.assert_invalid_message(message)

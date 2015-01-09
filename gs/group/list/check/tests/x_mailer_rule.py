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
from Products.XWFMailingListManager.emailmessage import EmailMessage
from gs.group.list.check.rules import XMailerRule


class TestXMailerRule(TestCase):
    'Test the x-mailer header rule'

    valid_xheader = 'Mailboxer'

    def setUp(self):
        group = create_autospec(GSGroupInfo, instance=True)
        self.group = group

    def assert_valid_message(self, message):
        m = 'Invalid message: {0}, expected: {1}; received: {2}'
        failMsg = m.format(
            message.s['status'],
            message.mailingList.getValueFor('xmailer'),
            message.message.get('x-mailer'))
        self.assertTrue(message.s['validMessage'], failMsg)

    def assert_invalid_message(self, message):
        failMsg = 'Valid message: {0}'.format(message.s['status'])
        self.assertFalse(message.s['validMessage'], failMsg)

    @patch.object(XMailerRule, 'mailingList')
    def test_message_with_good_xmailer_header_is_valid(self, ml):
        # Mock a valid X-Header for this test
        ml.getValueFor.return_value = TestXMailerRule.valid_xheader

        m = EmailMessage("")
        m.message.add_header('x-mailer', self.valid_xheader)

        message = XMailerRule(self.group, m)
        message.check()
        self.assert_valid_message(message)

    @patch.object(XMailerRule, 'mailingList')
    def test_message_with_bad_xmailer_header_is_invalid(self, ml):
        # Mock a valid X-Header for this test
        ml.getValueFor.return_value = TestXMailerRule.valid_xheader

        m = EmailMessage("")
        m.message.add_header('x-mailer', 'weezlewozzle')

        message = XMailerRule(self.group, m)
        message.check()

        self.assert_invalid_message(message)

    @patch.object(XMailerRule, 'mailingList')
    def test_message_with_no_xmailer_header_is_invalid(self, ml):
        # Mock a valid X-Header for this test
        ml.getValueFor.return_value = TestXMailerRule.valid_xheader

        m = EmailMessage("")

        message = XMailerRule(self.group, m)
        message.check()

        self.assert_invalid_message(message)

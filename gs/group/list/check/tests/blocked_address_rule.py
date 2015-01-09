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
from gs.group.list.check.rules import BlockedAddressRule


class TestBlockedAddressRule(TestCase):
    'Test the blocked address rule'

    blocked_addresses = [
        'spammer@example.com',
        'criminal@example.com',
        'bill.bushey@e-democracy.org'
    ]

    def setUp(self):
        group = create_autospec(GSGroupInfo, instance=True)
        self.group = group

    def assert_valid_message(self, message):
        m = 'Invalid message: {0}, {1} is in blocked addresses: {2}'
        failMsg = m.format(message.s['status'], message.message.sender,
                           message.mailingList.getValueFor('disabled'))
        self.assertTrue(message.s['validMessage'], failMsg)

    def assert_invalid_message(self, message):
        failMsg = 'Valid message: {0}'.format(message.s['status'])
        self.assertFalse(message.s['validMessage'], failMsg)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    @patch.object(BlockedAddressRule, 'mailingList')
    def test_message_from_unblocked_address_is_valid(self, ml,
                                                     MockEmailMessage):
        # Mock the blocked addresses of the mailing list
        ml.getValueFor.return_value = TestBlockedAddressRule.blocked_addresses

        m = MockEmailMessage.return_value
        m.sender = 'goodperson@example.com'

        message = BlockedAddressRule(self.group, m)
        message.check()
        self.assert_valid_message(message)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    @patch.object(BlockedAddressRule, 'mailingList')
    def test_message_from_blocked_address_is_invalid(self, ml,
                                                     MockEmailMessage):
        # Mock the blocked addresses of the mailing list
        ml.getValueFor.return_value = TestBlockedAddressRule.blocked_addresses

        m = MockEmailMessage.return_value
        m.sender = 'spammer@example.com'

        message = BlockedAddressRule(self.group, m)
        message.check()

        self.assert_invalid_message(message)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    @patch.object(BlockedAddressRule, 'mailingList')
    def test_message_to_list_with_no_blocked_addresses_is_valid(
            self,
            ml,
            MockEmailMessage):
        # Explicitely setting empty disabled address list
        ml.getValueFor.return_value = []

        m = MockEmailMessage.return_value
        m.sender = 'spammer@example.com'

        message = BlockedAddressRule(self.group, m)
        message.check()

        self.assert_valid_message(message)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    @patch.object(BlockedAddressRule, 'mailingList')
    def test_message_to_list_with_none_blocked_addresses_list_is_valid(
            self,
            ml,
            MockEmailMessage):
        # Explicitely setting blocked addresses list to None
        ml.getValueFor.return_value = None

        m = MockEmailMessage.return_value
        m.sender = 'spammer@example.com'

        message = BlockedAddressRule(self.group, m)
        message.check()

        self.assert_valid_message(message)

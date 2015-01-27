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

    @patch('gs.group.list.base.EmailMessage')
    @patch.object(BlockedAddressRule, 'query')
    def test_message_from_unblocked_address_is_valid(self, query,
                                                     MockEmailMessage):
        query.address_is_blacklisted.return_value = False
        m = MockEmailMessage.return_value
        m.sender = 'goodperson@example.com'

        rule = BlockedAddressRule(self.group, m)
        rule.check()
        self.assertTrue(rule.s['validMessage'])

    @patch('gs.group.list.base.EmailMessage')
    @patch.object(BlockedAddressRule, 'query')
    def test_message_from_blocked_address_is_invalid(self, query,
                                                     MockEmailMessage):
        query.address_is_blacklisted.return_value = True
        m = MockEmailMessage.return_value
        m.sender = 'spammer@example.com'

        rule = BlockedAddressRule(self.group, m)
        rule.check()
        self.assertFalse(rule.s['validMessage'])

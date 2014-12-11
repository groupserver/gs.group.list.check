# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from mock import patch, create_autospec
from unittest import TestCase
from Products.GSGroup import GSGroupInfo
from gs.group.list.check.rules import TightLoopRule


class TestTightLoopRule(TestCase):
    'Test the tight loop rule'

    last_email_checksum = 'hash_of_foo'

    def setUp(self):
        group = create_autospec(GSGroupInfo, instance=True)
        self.group = group

    def assert_valid_message(self, message):
        failMsg = (
            'Invalid message: {0}, {1} is the same checksum as: {2}').format(
                message.s['status'],
                message.message.post_id,
                message.mailingList._v_last_email_checksum)
        self.assertTrue(message.s['validMessage'], failMsg)

    def assert_invalid_message(self, message):
        failMsg = 'Valid message: {0}'.format(message.s['status'])
        self.assertFalse(message.s['validMessage'], failMsg)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    @patch.object(TightLoopRule, 'mailingList')
    def test_unique_message_is_valid(self, ml, MockEmailMessage):
        # Mock the last_email_checksum of the mailing list
        ml._v_last_email_checksum = TestTightLoopRule.last_email_checksum

        m = MockEmailMessage.return_value
        m.post_id = 'hash_of_unique'

        message = TightLoopRule(self.group, m)
        message.check()
        self.assert_valid_message(message)

    @patch('Products.XWFMailingListManager.emailmessage.EmailMessage')
    @patch.object(TightLoopRule, 'mailingList')
    def test_duplicate_message_is_invalid(self, ml, MockEmailMessage):
        # Mock the last_email_checksum of the mailing list
        ml._v_last_email_checksum = TestTightLoopRule.last_email_checksum

        m = MockEmailMessage.return_value
        m.post_id = TestTightLoopRule.last_email_checksum

        message = TightLoopRule(self.group, m)
        message.check()

        self.assert_invalid_message(message)

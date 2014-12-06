# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from mock import MagicMock, patch 
from unittest import TestCase
from Products.XWFMailingListManager.emailmessage import EmailMessage
from gs.group.list.check.rules import XMailerRule


class TestXMailerRule(TestCase):
    'Test the x-mailer header rule'

    valid_xheader = 'Mailboxer'

    def setUp(self):
        group = MagicMock()
        # --=mpj17=-- I am not proud of this next line
        gv = group.mailingList.getValueFor
        gv.return_value = TestXMailerRule.valid_xheader
        self.group = group

    def assert_valid_message(self, message):
        failMsg = 'Invalid message: {0}, expected: {1}; received: {2}'.format(
                message.s['status'],
                message.mailingList.getValueFor('xmailer'), 
                message.message.get('x-mailer') )
        import code
        code.interact(local=locals())
        self.assertTrue(message.s['validMessage'], failMsg)

    def assert_invalid_message(self, message):
        failMsg = 'Valid message: {0}'.format(message.s['status'])
        self.assertFalse(message.s['validMessage'], failMsg)

    @patch.object(XMailerRule, 'groupInfo')
    def test_message_with_good_xmailer_header_is_valid(self, gi):
        m = EmailMessage("")
        m.message.add_header('x-mailer', self.valid_xheader)

        g = self.group

        message = XMailerRule(g, m)
        message.check()

        self.assert_valid_message(message)

    def text_message_with_bad_xmailer_header_is_invalid(self):
        m = MagicMock(EmailMessage(""))
        m.message.add_header('x-mailer', 'weezlewozzle')

        g = self.group

        message = XMailerRule(g, m)
        message.check()

        self.assert_invalid_message(message)

    def text_message_with_no_xmailer_header_is_invalid(self):
        m = MagicMock(EmailMessage(""))

        g = self.group

        message = XMailerRule(g, m)
        message.check()

        self.assert_invalid_message(message)

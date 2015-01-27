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
from __future__ import unicode_literals, absolute_import
from re import search
from zope.cachedescriptors.property import Lazy
from .baserule import BaseRule, check_asserts
from .queries import MemberQuery


class XMailerRule(BaseRule):
    'Valid messages include an x-mailer header that was set by GroupServer'
    weight = 10

    def check(self):
        if not self.s['checked']:
            gs_xmailer = self.mailingList.getValueFor('xmailer')
            msg_xmailer = self.message.get('x-mailer')
            if msg_xmailer != gs_xmailer:
                self.s['validMessage'] = False
                self.s['status'] = 'does not contain a valid x-mailer '\
                                   'header'
                self.s['statusNum'] = self.weight
            else:
                self.s['validMessage'] = True
                self.s['status'] = 'contains valid x-mailer header'
                self.s['statusNum'] = 0
            self.s['checked'] = True

        check_asserts(self)


class BlockedAddressRule(BaseRule):
    '''Valid messages can not come from a blocked email address'''
    weight = 20

    @Lazy
    def query(self):
        retval = MemberQuery()
        return retval

    def check(self):
        if not self.s['checked']:
            sender = self.message.sender
            if self.query.address_is_blacklisted(sender):
                self.s['validMessage'] = False
                self.s['status'] = ' is from a blocked email address'
                self.s['statusNum'] = self.weight
            else:
                self.s['validMessage'] = True
                self.s['status'] = ' is from a non-blocked email address'
                self.s['statusNum'] = 0
        self.s['checked'] = True

        check_asserts(self)


class AutomaticEmailRule(BaseRule):
    '''Valid messages can not be automatically generated emails'''
    weight = 30

    def check(self):
        if not self.s['checked']:
            return_path = self.message.get('return-path')
            if return_path == '<>':
                self.s['validMessage'] = False
                self.s['status'] = ' is an automatically generated email'
                self.s['statusNum'] = self.weight
            else:
                self.s['validMessage'] = True
                self.s['status'] = ' is not an automatic email'
                self.s['statusNum'] = 0
        self.s['checked'] = True

        check_asserts(self)


class TightLoopRule(BaseRule):
    '''Valid messages can not have recently been sent from the group'''
    weight = 40

    def check(self):
        if not self.s['checked']:
            assert hasattr(self.mailingList, '_v_last_email_checksum'), \
                "no _v_last_email_checksum"

            last_email_checksum = self.mailingList._v_last_email_checksum
            current_email_checksum = self.message.post_id
            if last_email_checksum and (last_email_checksum ==
                                        current_email_checksum):
                self.s['validMessage'] = False
                self.s['status'] = ' is a duplicate, tight loop message'
                self.s['statusNum'] = self.weight
            else:
                self.s['validMessage'] = True
                self.s['status'] = ' is a unique message'
                self.s['statusNum'] = 0
        self.s['checked'] = True

        check_asserts(self)


class ForbiddenTextRule(BaseRule):
    'Ensure a forbidden text is absent from the message'
    weight = 50

    def check(self):
        if not self.s['checked']:
            mailString = self.message.message.as_string()
            self.s['validMessage'] = True  # Uncharacteristic optimism
            self.s['status'] = ' is free from forbidden text'
            self.s['statusNum'] = 0

            for regexp in self.mailingList.getValueFor('spamlist'):
                if regexp and search(regexp, mailString):
                    self.s['validMessage'] = False
                    m = ' matches forbidden text "{0}"'
                    self.s['status'] = m.format(regexp)
                    self.s['statusNum'] = self.weight
                    break
        self.s['checked'] = True
        check_asserts(self)

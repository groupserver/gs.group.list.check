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
from abc import ABCMeta, abstractmethod
import sys
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo
STRING = basestring if (sys.version_info < (3, )) else str


def check_asserts(rule):
    assert isinstance(rule, BaseRule)

    assert rule.s['checked']
    assert type(rule.s['validMessage']) == bool
    assert isinstance(rule.s['status'], STRING)
    assert type(rule.s['statusNum']) == int


class BaseRule(object):
    '''The rule abstract base class

:param group: The group.
:param message: The email message.'''
    __metaclass__ = ABCMeta
    weight = None

    def __init__(self, group, message):
        self.group = group
        self.message = message

        #: The state of the rule. Set once for efficency.
        self.s = {'checked': False,
                  'validMessage': False,
                  'status': 'not implemented',
                  'statusNum': -1}

    @abstractmethod
    def check(self):
        '''Check the message

:Side effects:
  Sets the :attr:`self.s` dictionary'''

    @Lazy
    def groupInfo(self):
        return IGSGroupInfo(self.group)

    @Lazy
    def siteInfo(self):
        return createObject('groupserver.SiteInfo', self.group)

    @Lazy
    def mailingList(self):
        site_root = self.group.site_root()
        mailingListManager = site_root.ListManager
        retval = mailingListManager.get_list(self.groupInfo.id)
        return retval

    @Lazy
    def validMessage(self):
        self.check()
        retval = self.s['status']
        assert isinstance(retval, STRING)
        return retval

    @Lazy
    def statusNum(self):
        self.check()
        retval = self.s['statusNum']
        assert retval in (-1, 0, self.weight), \
            'self.statusNum is "%s", not in range: -1, 0, %s' % \
            (retval, self.weight)
        assert (retval in (-1, self.weight) and (not self.validMessage))\
            or ((retval == 0) and self.validMessage), 'Mismatch between '\
            'self.satusNum "%s" and self.canPost "%s"' %\
            (retval, self.validMessage)


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

    def check(self):
        if not self.s['checked']:
            disabled = self.mailingList.getValueFor('disabled')
            if disabled is None:
                disabled = []
            sender = self.message.sender
            if sender in disabled:
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

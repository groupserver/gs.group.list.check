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


def check_type(expected, val):
    m = 'Expected {0}, got {1}'
    if not(type(val) == expected):
        raise TypeError(m.format(expected, type(val)))


def check_instance(expected, val):
    m = 'Expected {0}, got {1}'
    if not(isinstance(val, expected)):
        raise TypeError(m.format(expected, type(val)))


def check_asserts(rule):
    check_instance(BaseRule, rule)
    check_type(bool, rule.s['checked'])
    check_type(bool, rule.s['validMessage'])
    check_instance(STRING, rule.s['status'])
    check_type(int, rule.s['statusNum'])


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
        retval = self.s['validMessage']
        if not isinstance(retval, bool):
            raise TypeError('{0} is not a Boolean'.format(retval))
        return retval

    @Lazy
    def status(self):
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
        return retval

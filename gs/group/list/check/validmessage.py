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
from functools import reduce
from operator import and_
from zope.cachedescriptors.property import Lazy
from zope.component import getGlobalSiteManager
from .interfaces import IGSValidMessageRule


class IsValidMessage(object):
    def __init__(self, group, message):
        self.group = group
        self.message = message

    @Lazy
    def adaptors(self):
        gsm = getGlobalSiteManager()
        retval = [a for a in gsm.getAdapters((self.group, self.message),
                                             IGSValidMessageRule)]
        retval.sort(key=lambda r: r[1].weight)
        return retval

    @Lazy
    def rules(self):
        retval = [instance for name, instance in self.adaptors]
        return retval

    @Lazy
    def validMessage(self):
        return reduce(and_, [rule.validMessage for rule in self.rules],
                      True)

    @Lazy
    def statusNum(self):
        statusNums = [rule.statusNum for rule in self.rules
                      if rule.statusNum != 0]
        retval = (statusNums and min(statusNums)) or 0
        assert retval >= 0
        return retval

    @Lazy
    def status(self):
        retval = [rule.status for rule in self.rules
                  if rule.statusNum == self.statusNum][0]
        return retval

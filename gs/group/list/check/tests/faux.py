# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from email.parser import Parser
from zope.interface import Interface, implementer, directlyProvides
from gs.group.list.base.interfaces import IEmailMessage
from gs.group.list.check.interfaces import IGSValidMessageRule


class IFauxGroup(Interface):
    'This is not a group'


@implementer(IFauxGroup)
class FauxGroup(object):
    'This is not a group'


@implementer(IGSValidMessageRule)
class FauxRuleValid(object):
    def __init__(self, message, group):
        self.validMessage = True
        self.weight = 10
        self.statusNum = 0


@implementer(IGSValidMessageRule)
class FauxRuleInvalid(object):
    def __init__(self, message, group):
        self.validMessage = False
        self.weight = 20
        self.statusNum = 1


email = Parser().parsestr(
    'From: <member@example.com>\n'
    'To: <group@example.com>\n'
    'Subject: This is a message\n'
    '\n'
    'Body would go here\n')
directlyProvides(email, IEmailMessage)

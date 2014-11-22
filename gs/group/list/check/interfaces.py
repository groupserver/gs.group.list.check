# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope.interface.interface import Interface
from zope.schema import Bool, Int, Text


class IValidMessage(Interface):
    validMessage = Bool(
        title=u'Valid Message',
        description=u'Is the message valid for posting to the list?',
        required=True)

    statusNum = Int(
        title=u'Status Number',
        description=u'The reason the message is not valid, as a number. 0 if '
                    u'the message is valid for posting.',
        required=True)

    status = Text(
        title=u'Status',
        description=u'The reason the message is not valid for posting as '
                    u'a textual description.',)


class IGSValidMessageRule(IValidMessage):
    weight = Int(
        title=u'Weight',
        description=u'The weight of this rule, used for sorting the rules.',
        default=0)


class IGSValidMessage(IValidMessage):
    pass

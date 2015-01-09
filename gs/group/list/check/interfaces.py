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
from __future__ import unicode_literals
from zope.interface.interface import Interface
from zope.schema import Bool, Int, Text


class IValidMessage(Interface):
    validMessage = Bool(
        title='Valid Message',
        description='Is the message valid for posting to the list?',
        required=True)

    statusNum = Int(
        title='Status Number',
        description='The reason the message is not valid, as a number. 0 '
                    'if the message is valid for posting.',
        required=True)

    status = Text(
        title='Status',
        description='The reason the message is not valid for posting as '
                    'a textual description.',)


class IGSValidMessageRule(IValidMessage):
    weight = Int(
        title='Weight',
        description='The weight of this rule, used for sorting the rules.',
        default=0)


class IGSValidMessage(IValidMessage):
    pass

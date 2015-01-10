# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
#from mock import patch
from unittest import TestCase
from zope.component import getGlobalSiteManager
#from gs.group.list.check.validmessage import (IsValidMessage)
from gs.group.list.check.interfaces import IGSValidMessageRule
from .faux import FauxGroup, FauxRuleInvalid, IFauxGroup


class TestIsValidMessage(TestCase):
    def setUp(self):
        self.fauxGroup = FauxGroup()

    def test_vaid_only(self):
        self.assertTrue(True)

    def test_invalid(self):
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(FauxRuleInvalid, (IFauxGroup,),
                            IGSValidMessageRule, 'invalid')
        self.assertTrue(True)
        gsm.unregisterAdapter(FauxRuleInvalid, (IFauxGroup,),
                            IGSValidMessageRule, 'invalid')

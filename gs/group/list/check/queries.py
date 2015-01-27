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
from __future__ import unicode_literals
from gs.database import getTable, getSession


class MemberQuery(object):

    def __init__(self):
        self.emailBlacklist = getTable('email_blacklist')

    def address_is_blacklisted(self, emailAddress):
        s = self.emailBlacklist.select()
        ilike = self.emailBlacklist.c.email.op('ILIKE')
        s.append_whereclause(ilike(emailAddress))

        session = getSession()
        r = session.execute(s)

        retval = (r.rowcount > 0)
        assert type(retval) == bool
        return retval

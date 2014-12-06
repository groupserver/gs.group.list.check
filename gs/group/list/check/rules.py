# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo


class BaseRule(object):
    weight = None

    def __init__(self, group, message):
        self.group = group
        self.message = message
        self.s = {'checked': False,
                  'validMessage': False,
                  'status': 'not implemented',
                  'statusNum': -1}

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

    def check(self):
        m = 'Sub-classes must implement the check method.'
        raise NotImplementedError(m)

    @Lazy
    def validMessage(self):
        self.check()
        retval = self.s['status']
        assert type(retval) == unicode
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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo


def check_asserts(rule):
    assert isinstance(rule, BaseRule)

    assert rule.s['checked']
    assert type(rule.s['validMessage']) == bool
    assert type(rule.s['status']) == unicode
    assert type(rule.s['statusNum']) == int


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


class XMailerRule(BaseRule):
    '''Valid messages include an x-mailer header that was set by GroupServer'''
    weight = 10

    def check(self):
        if not self.s['checked']:
            ml = self.mailingList
            msg = self.message
            gs_xmailer = ml.getValueFor('xmailer')
            if msg.get('x-mailer') != gs_xmailer:
                self.s['validMessage'] = False
                self.s['status'] = 'does not contain a valid x-mailer header'
                self.s['statusNum'] = self.weight
            else:
                self.s['validMessage'] = True
                self.s['status'] = 'contains valid x-mailer header'
                self.s['statusNum'] = 0
            self.s['checked'] = True

        check_asserts(self)

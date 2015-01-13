=======================
``gs.group.list.check``
=======================
~~~~~~~~~~~~~~~~~~~~~~~~~~
Check if an email is valid
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Bill Bushey`_
:Contact: Bill Bushey <bill.bushey@e-democracy.org>
:Date: 2014-11-21
:Organization: `E-Democracy`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 License`_
  by `E-Democracy`_.

Introduction
============

Several things about a message must be verified before it can be
posted to a mailing list. In GroupServer_ this verification is
performed by two products:

- ``gs.group.member.canpost`` [#canpost]_ verifies that the
  sender of a message has *permission* to post a message to a
  given group.

- ``gs.group.list.check`` (this product) verifies that the
  message meets a set of fundamental rules_. The actual checking
  is done by a validator_.

Rules
=====

There are four rules. Each rule is a named adaptor. Each takes a
group and a message, and conforms to the ``IGSValidMessageRule``
interface. There are four rules provided by default:

#. Not an automatic_ message,
#. No `tight loop`_,
#. No blocked_ email addresses. and
#. No `forbidden text`_ in the message.

Automatic
---------

An automatic message is one whose ``Return-path`` header is
``<>``. Automatic messages are dropped.

:See also: `Forbidden text`_.
:Adaptor name: ``gs-group-list-check-automatic``

Tight loop
----------

A *tight loop* is a message that has been posted twice to the
group. GroupServer detects tight-loops by storing the identifier
(which is also a check-sum) of the last-seen post in the
``_v_last_email_checksum`` property of the mailing-list
object. If the post-identifier of the current message matches the
checksum of the last-seen post then the message is dropped.

:Adaptor name: ``gs-group-list-check-tightloop``


Blocked
-------

Some people are so horrid that they are blocked from posting
(*blacklisted*). The list of blocked email addresses is stored in
the ``email_blacklist`` table of the database. We never tell
sender the message has been dropped.

:Adaptor name: ``gs-group-list-check-blocked``

Forbidden text
--------------

The forbidden text check is used to drop *out of office*
messages. It looks up the ``spamlist`` property of the mailing
list (or mailing list manager). This is a list of regular
expressions. The rule compares each expression against the
**entire** message, including the headers. If there is a match
the message is dropped.

The list of regular expressions is normally some variations on::

  Subject.*Out of office.*

:Adaptor name: ``gs-group-list-check-forbidden``


Validator
=========

The validator is an adaptor that takes a group and a message, and
confirms to the ``IValidMessage`` interface. The validator sorts
the rules_ by weight and checks if the message if valid. 

If one of these checks fails then the message is dropped. The
poster is never notified, because in all circumstances there is
either no point, or it would make a bad situation worse (such as
the out-of-office messages).

:Note: If the user should be notified when a rule is violated
       then the rule should be implemented as part of the group
       member posting system [#canpost]_.

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.list.check 
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _E-Democracy: http://e-democracy.org/
.. _Bill Bushey: http://groupserver.org/p/wbushey
.. _Creative Commons Attribution-Share Alike 3.0 License:
   http://creativecommons.org/licenses/by-sa/3.0/
.. [#canpost] The group member posting system checks for more
              user-specific problems, such as exceeding the
              posting limit. If these checks fail the user is
              sent a notification.  See the
              ``gs.group.member.canpost`` product
              <https://github.com/groupserver/gs.group.member.canpost>

..  LocalWords:  Validator validator

==============================
``gs.group.list.check``
==============================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This product performs checks on whether a provided email message is valid and can be posted to a group.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Bill Bushey`_
:Contact: Bill Bushey <bill.bushey@e-democracy.org>
:Date: 2014-11-21
:Organization: `E-Democracy`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 License`_
  by `E-Democracy`_.

Introduction
===========

Several things about a message must be verified before it can be posted to a 
mailing list. In `GroupServer`_ this verification is performed by two products:

- `gs.group.member.canpost`_ verifies that the sender of a message has 
  *permission* to post a message to a given group.
- gs.group.list.checks (this product) verifies that the message meets a set of
  additional criteria, such as having required headers and not being auto-
  generated responses.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.list.check 
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _E-Democracy: http://e-democracy.org/
.. _Bill Bushey: http://groupserver.org/p/wbushey
.. _Creative Commons Attribution-Share Alike 3.0 License:
   http://creativecommons.org/licenses/by-sa/3.0/
.. _gs.group.member.canpost: 
   https://source.iopen.net/groupserver/gs.group.member.canpost

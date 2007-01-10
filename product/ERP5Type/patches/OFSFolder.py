##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from OFS.Folder import Folder

"""
  This patch modifies OFS.Folder._setOb to update portal_skins cache when
  needed.
"""

Folder_original__setOb = Folder._setOb

def Folder_setOb(self, id, object):
  """
    Update portal_skins cache with the new files.

    Checks must be done from the quickest to the slowest to avoid wasting
    time when no cache must be updated.

    Update must only be triggered if we (folder) are right below the skin
    tool, not any deeper.
  """
  Folder_original__setOb(self, id, object)
  aq_chain = getattr(self, 'aq_chain', None)
  if aq_chain is None: # Not in acquisition context
    return
  if len(aq_chain) < 2: # Acquisition context is not deep enough for context to possibly be below portal skins.
    return
  portal_skins = aq_chain[-2]
  if getattr(portal_skins, 'meta_type', '') != 'CMF Skins Tool' : # It is not a skin tool we're below.
    return
  _updateCacheEntry = getattr(portal_skins.aq_base, '_updateCacheEntry', None)
  if _updateCacheEntry is None:
    return
  _updateCacheEntry(self.id, id)

Folder._setOb = Folder_setOb

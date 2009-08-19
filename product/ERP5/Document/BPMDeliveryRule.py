# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2002-2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#                    Romain Courteaud <romain@nexedi.com>
#                    Łukasz Nowak <luke@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5.Document.BPMRule import BPMRule

class BPMDeliveryRule(BPMRule):
  """
    DISCLAIMER: Refer to BPMRule docstring disclaimer.

    This is BPM enabled Delivery Rule.
  """

  # CMF Type Definition
  meta_type = 'ERP5 BPM Delivery Rule'
  portal_type = 'BPM Delivery Rule'

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  def _getInputMovementList(self, applied_rule):
    """Return list of movements from delivery"""
    delivery = applied_rule.getDefaultCausalityValue()
    if delivery is not None:
      return delivery.getMovementList(
                     portal_type=delivery.getPortalDeliveryMovementTypeList())
    return []

  def _getExpandablePropertyUpdateDict(self, applied_rule, movement,
      business_path, current_property_dict):
    """Delivery specific update dict"""
    return {
      'order_list': [movement.getRelativeUrl()],
      'delivery_list': [movement.getRelativeUrl()],
      'deliverable': 1,
    }

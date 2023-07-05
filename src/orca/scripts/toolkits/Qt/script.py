# Orca
#
# Copyright (C) 2013-2019 Igalia, S.L.
#
# Author: Joanmarie Diggs <jdiggs@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2013-2019 Igalia, S.L."
__license__   = "LGPL"

import gi
gi.require_version("Atspi", "2.0")
from gi.repository import Atspi

import orca.debug as debug
import orca.orca as orca
import orca.scripts.default as default
from orca.ax_object import AXObject


class Script(default.Script):

    def __init__(self, app):
        super().__init__(app)

    def onCaretMoved(self, event):
        """Callback for object:text-caret-moved accessibility events."""

        if AXObject.get_role(event.source) == Atspi.Role.ACCELERATOR_LABEL:
            msg = "QT: Ignoring event due to role."
            debug.println(debug.LEVEL_INFO, msg, True)
            return

        super().onCaretMoved(event)

    def onFocusedChanged(self, event):
        """Callback for object:state-changed:focused accessibility events."""

        if not event.detail1:
            return

        if AXObject.get_role(event.source) == Atspi.Role.ACCELERATOR_LABEL:
            msg = "QT: Ignoring event due to role."
            debug.println(debug.LEVEL_INFO, msg, True)
            return

        frame = self.utilities.topLevelObject(event.source, useFallbackSearch=True)
        if not frame:
            msg = "QT: Ignoring event because we couldn't find an ancestor window."
            debug.println(debug.LEVEL_INFO, msg, True)
            return

        isActive = AXObject.has_state(frame, Atspi.StateType.ACTIVE)
        if not isActive:
            msg = "QT: Event came from inactive top-level object %s" % frame
            debug.println(debug.LEVEL_INFO, msg, True)

            AXObject.clear_cache(frame)
            isActive = AXObject.has_state(frame, Atspi.StateType.ACTIVE)
            msg = "QT: Cleared cache of %s. Frame is now active: %s" % (frame, isActive)
            debug.println(debug.LEVEL_INFO, msg, True)

        state = AXObject.get_state_set(event.source)
        if state.contains(Atspi.StateType.FOCUSED) and state.contains(Atspi.StateType.FOCUSABLE):
            super().onFocusedChanged(event)
            return

        msg = "QT: WARNING - source states lack focused and/or focusable"
        debug.println(debug.LEVEL_INFO, msg, True)
        orca.setLocusOfFocus(event, event.source)

# Orca
#
# Copyright 2016 Igalia, S.L.
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
__copyright__ = "Copyright (c) 2016 Igalia, S.L."
__license__   = "LGPL"

from orca import debug
from orca import focus_manager
from orca.scripts import default
from orca.ax_text import AXText

from .braille_generator import BrailleGenerator
from .speech_generator import SpeechGenerator
from .script_utilities import Utilities


class Script(default.Script):

    def __init__(self, app):
        super().__init__(app)
        self.present_if_inactive = False

    def deactivate(self):
        """Called when this script is deactivated."""

        self.utilities.clearCache()
        super().deactivate()

    def get_braille_generator(self):
        """Returns the braille generator for this script."""

        return BrailleGenerator(self)

    def get_speech_generator(self):
        """Returns the speech generator for this script."""

        return SpeechGenerator(self)

    def get_utilities(self):
        """Returns the utilities for this script."""

        return Utilities(self)

    def on_focus(self, event):
        """Callback for focus: accessibility events."""

        # https://bugzilla.gnome.org/show_bug.cgi?id=748311
        focus_manager.get_manager().set_locus_of_focus(event, event.source)

    def on_text_deleted(self, event):
        """Callback for object:text-changed:delete accessibility events."""

        if self.utilities.treatEventAsNoise(event):
            msg = "TERMINAL: Deletion is believed to be noise"
            debug.printMessage(debug.LEVEL_INFO, msg, True)
            return

        super().on_text_deleted(event)

    def on_text_inserted(self, event):
        """Callback for object:text-changed:insert accessibility events."""

        if not self.utilities.treatEventAsCommand(event):
            msg = "TERMINAL: Passing along event to default script."
            debug.printMessage(debug.LEVEL_INFO, msg, True)
            super().on_text_inserted(event)
            return

        msg = "TERMINAL: Insertion is believed to be due to terminal command"
        debug.printMessage(debug.LEVEL_INFO, msg, True)

        self.updateBraille(event.source)

        newString = self.utilities.insertedText(event)
        if len(newString) == 1:
            self.speakCharacter(newString)
        else:
            voice = self.speech_generator.voice(obj=event.source, string=newString)
            self.speakMessage(newString, voice=voice)

        if self.get_flat_review_presenter().is_active():
            msg = "TERMINAL: Flat review presenter is active. Ignoring insertion"
            debug.printMessage(debug.LEVEL_INFO, msg, True)
            return

        offset = AXText.get_caret_offset(event.source)
        self._saveLastCursorPosition(event.source, offset)
        self.utilities.updateCachedTextSelection(event.source)

    def presentKeyboardEvent(self, event):
        if not event.isPrintableKey():
            return super().presentKeyboardEvent(event)

        if event.isPressedKey():
            return False

        self._sayAllIsInterrupted = False
        self.utilities.clearCachedCommandState()
        if not event.shouldEcho() or event.isOrcaModified() or event.isCharacterEchoable():
            return False

        # We have no reliable way of knowing a password is being entered into
        # a terminal -- other than the fact that the text typed isn't there.
        char, start = AXText.get_character_at_offset(event.getObject())[0:2]
        prevChar = AXText.get_character_at_offset(event.getObject(), start - 1)[0]
        string = event.event_string
        if string not in [prevChar, "space", char]:
            return False

        tokens = ["TERMINAL: Presenting keyboard event", string]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)
        self.speakKeyEvent(event)
        return True

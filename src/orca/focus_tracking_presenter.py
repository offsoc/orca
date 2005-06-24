# Orca
#
# Copyright 2004-2005 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""Provides the focus tracking presentation manager for Orca.  The main
entry points into this module are for the presentation manager contract:

    processKeyEvent     - handles all keyboard events
    processBrailleEvent - handles all Braille input events
    activate            - called when this manager is enabled
    deactivate          - called when this manager is disabled

This module uses the script module to maintain a set of scripts for all
running applications, and also keeps the notion of an activeScript.  All
object events are passed to the associated script for that application,
regardless if the application has keyboard focus or not.  All keyboard events
are passed to the active script only if it has indicated interest in the
event.
"""

import sys

import a11y
import core
import debug
#import mag - [[[TODO: WDW - disable until I can figure out how
#             to resolve the GNOME reference in mag.py.]]]
import orca
import script
import speech

from orca_i18n import _ # for gettext support

# The currently active script - this script will get all keyboard
# and Braille events.
#
_activeScript = None


########################################################################
#                                                                      #
# METHODS FOR PRE-PROCESSING AND MASSAGING AT-SPI OBJECT EVENTS        #
#                                                                      #
# AT-SPI events are receieved here and converted into a Python object  #
# for processing by the rest of Orca.                                  #
#                                                                      #
########################################################################

# Dictionary that keeps count of event listeners by type.  This is a bit
# convoluted for now, but what happens is that scripts tell the
# focus_tracking_presenter to listen for object events based on what they
# want, and the focus_tracking_presenter then eventually passes them to the
# script.  Because both the focus_tracking_presenter and scripts are
# interested in object events, and the focus_tracking_presenter is what delves
# them out, we keep at most one listener to avoid receiving the same event
# twice in a row.
#
_listenerCounts = {}

def registerEventListener(eventType):
    """Tells this module to listen for the given event type.

    Arguments:
    - eventType: the event type.
    """

    global _listenerCounts
    
    if _listenerCounts.has_key(eventType):
        _listenerCounts[eventType] = _listenerCounts[eventType] + 1
    else:
        core.registerEventListener(processObjectEvent, eventType)
        _listenerCounts[eventType] = 1

            
def unregisterEventListener(eventType):
    """Tells this module to stop listening for the given event type.

    Arguments:
    - eventType: the event type.
    """

    global _listenerCounts
    
    _listenerCounts[eventType] = _listenerCounts[eventType] - 1
    if _listenerCounts[eventType] == 0:
        core.unregisterEventListener(processObjectEvent, eventType)
        del _listenerCounts[eventType]


class Event:
   """Dummy class for converting the source of an event to an
   Accessible object.  We need this since the core.event object we
   get from the core is read-only.  So, we create this dummy event
   object to contain a copy of all the event members with the source
   converted to an Accessible.  It is perfectly OK for event handlers
   to annotate this object with their own attributes.
   """
   pass


def processObjectEvent(e):
    """Handles all events destined for scripts.

    Arguments:
    - e: an at-spi event.
    """
    
    global _activeScript
    
    # We ignore defunct objects and let the a11y module take care of them
    # for us.
    #
    if e.type == "object:state-changed:defunct":
        return

    # Convert the AT-SPI event into a Python Event that we can annotate.
    # Copy relevant details from the event.
    #
    event = Event()
    event.type = e.type
    event.detail1 = e.detail1
    event.detail2 = e.detail2
    event.any_data = e.any_data
    event.source = a11y.makeAccessible(e.source)

    print event.source
    
    debug.printObjectEvent(debug.LEVEL_FINEST,
                           event,
                           a11y.accessibleToString("                ",
                                                   event.source))

    if event.source is None:
        sys.stderr.write("ERROR: received an event with no source.\n")
        return

    # [[[TODO: WDW - might want to consider re-introducing the reload
    # feature of scripts somewhere around here.  I pulled it out as
    # part of the big refactor to make scripts object-oriented.]]]
    #
    if event.type == "window:activate":
        speech.stop("default")
        _activeScript = script.getScript(event.source.app)
        debug.println(debug.LEVEL_FINE, "ACTIVATED SCRIPT: " \
                      + _activeScript.name)
    elif event.type == "object:children-changed:remove":
        # [[[TODO: WDW - something is severely broken.  We are not deleting
        # scripts here.
        #
        if e.source == core.desktop:
            try:
                script.deleteScript(event.source.app)
                return
            except:
                debug.printException(debug.LEVEL_SEVERE)
                return

    if event.source.app is None:
        set = event.source.state
        try:
            if event.source.state.count(core.Accessibility.STATE_DEFUNCT) > 0:
                return
        except:
            return
        
    s = script.getScript(event.source.app)

    try:
        s.processObjectEvent(event)
    except:
        debug.printException(debug.LEVEL_SEVERE)


def processKeyEvent(keystring):
    """Processes the given keyboard event based on the keybinding from the
    currently active script. This method is called synchronously from the
    at-spi registry and should be performant.  In addition, it must return
    True if it has consumed the event (and False if not).
    
    Arguments:
    - keystring: a keyboard event string

    Returns True if the event should be consumed.
    """

    global _activeScript
    
    if _activeScript:
        try:
            return _activeScript.processKeyEvent(keystring)
        except:
            debug.printException(debug.LEVEL_SEVERE)
            
    return False


def processBrailleEvent(command):
    """Called whenever a cursor key is pressed on the Braille display.
    
    Arguments:
    - command: the BrlAPI command for the key that was pressed.

    Returns True if the command was consumed; otherwise False
    """

    if _activeScript:
        try:
            return _activeScript.processBrailleEvent(command)
        except:
            pass

    return False
        

def activate():
    """Called when this presentation manager is activated."""

    speech.say("default", _("Switching to focus tracking mode."))

    registerEventListener("window:activate")
    registerEventListener("object:children-changed:remove")

    win = orca.findActiveWindow()
    if win:
        # Generate a fake window activation event so the application
        # can tell the user about itself.
        #
        e = Event()
        e.source = win.acc
        e.type = "window:activate"
        e.detail1 = 0
        e.detail2 = 0
        e.any_data = None    

        processObjectEvent(e)


def deactivate():
    """Called when this presentation manager is deactivated."""

    for key in _listenerCounts.keys():
        core.unregisterEventListener(processObjectEvent, key)
    _listenerCounts = {}

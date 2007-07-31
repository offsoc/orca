#!/usr/bin/python

"""Test of toggle button output using the gtk-demo Expander button demo.
"""

from macaroon.playback.keypress_mimic import *

sequence = MacroSequence()

########################################################################
# We wait for the demo to come up and for focus to be on the tree table
#
sequence.append(WaitForWindowActivate("GTK+ Code Demos"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TREE_TABLE))

########################################################################
# Once gtk-demo is running, invoke the Expander demo
#
sequence.append(KeyComboAction("<Control>f"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TEXT))
sequence.append(TypeAction("Expander"))
sequence.append(KeyComboAction("Return", 500))

########################################################################
# Once the demo is up, toggle the toggle button a few times and then
# close the dialog.
#
#sequence.append(WaitForWindowActivate("GtkExpander",None))
sequence.append(WaitForFocus("Details", acc_role=pyatspi.ROLE_TOGGLE_BUTTON))
sequence.append(KeyComboAction("Return"))

sequence.append(WaitAction("object:state-changed:expanded",
                           "Details",
                           None,
                           pyatspi.ROLE_TOGGLE_BUTTON,
                           5000))
sequence.append(KeyComboAction("Return", 500))

sequence.append(WaitAction("object:state-changed:expanded",
                           "Details",
                           None,
                           pyatspi.ROLE_TOGGLE_BUTTON,
                           5000))
sequence.append(KeyComboAction("Return", 500))

sequence.append(WaitAction("object:state-changed:expanded",
                           "Details",
                           None,
                           pyatspi.ROLE_TOGGLE_BUTTON,
                           5000))
sequence.append(KeyComboAction("Return", 500))

sequence.append(WaitAction("object:state-changed:expanded",
                           "Details",
                           None,
                           pyatspi.ROLE_TOGGLE_BUTTON,
                           5000))
sequence.append(KeyComboAction("Tab"))

sequence.append(WaitForFocus("Close", acc_role=pyatspi.ROLE_PUSH_BUTTON))
sequence.append(KeyComboAction("Return", 500))

########################################################################
# Go back to the main gtk-demo window and reselect the
# "Application main window" menu.  Let the harness kill the app.
#
#sequence.append(WaitForWindowActivate("GTK+ Code Demos",None))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TREE_TABLE))
sequence.append(KeyComboAction("Home"))

sequence.append(WaitAction("object:active-descendant-changed",
                           None,
                           None,
                           pyatspi.ROLE_TREE_TABLE,
                           5000))

sequence.start()

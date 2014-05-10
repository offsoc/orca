#!/usr/bin/python

"""Test flat review on menubar."""

from macaroon.playback import *
import utils

sequence = MacroSequence()
sequence.append(KeyComboAction("F6"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_8"))
sequence.append(utils.AssertPresentationAction(
    "1. Review current line.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "SPEECH OUTPUT: 'File Edit View Insert Format Table Tools Window Help'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_5"))
sequence.append(utils.AssertPresentationAction(
    "2. Review current word.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "SPEECH OUTPUT: 'File'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "3. Review next word.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=6",
     "SPEECH OUTPUT: 'Edit'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "4. Review next word.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=11",
     "SPEECH OUTPUT: 'View'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_4"))
sequence.append(utils.AssertPresentationAction(
    "5. Review previous word.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=6",
     "SPEECH OUTPUT: 'Edit'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_4"))
sequence.append(utils.AssertPresentationAction(
    "6. Review previous word.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "SPEECH OUTPUT: 'File'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_2"))
sequence.append(utils.AssertPresentationAction(
    "7. Review current char.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "SPEECH OUTPUT: 'F'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_2"))
sequence.append(KeyComboAction("KP_2"))
sequence.append(utils.AssertPresentationAction(
    "8. Spell current char.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "SPEECH OUTPUT: 'F'",
     "SPEECH OUTPUT: 'foxtrot' voice=uppercase"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_2"))
sequence.append(KeyComboAction("KP_2"))
sequence.append(KeyComboAction("KP_2"))
sequence.append(utils.AssertPresentationAction(
    "9. Unicode for current char.",
    ["BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "BRAILLE LINE:  'File Edit View Insert Format Table Tools Window Help $l'",
     "     VISIBLE:  'File Edit View Insert Format Tab', cursor=1",
     "SPEECH OUTPUT: 'F'",
     "SPEECH OUTPUT: 'foxtrot' voice=uppercase",
     "SPEECH OUTPUT: 'Unicode 0046'"]))

sequence.append(utils.AssertionSummaryAction())
sequence.start()

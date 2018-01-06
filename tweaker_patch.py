#!/usr/bin/env python3
#
# test_midiout.py
#

"""Show how to open an output port and send MIDI events."""

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON
from rtmidi.midiutil import open_midiinput

from tweaker_macro import *

### set midi ports ###

port_tweaker = sys.argv[1] if len(sys.argv) > 1 else None
port_hammond = sys.argv[2] if len(sys.argv) > 2 else None

try:
    print("Connecting LED output")
    midiout_led, port_name = open_midioutput(port=port_tweaker, client_name="tweaker", port_name="output_led")
    print("Connecting Notes output")
    midiout_notes, port_name = open_midioutput(port=port_hammond, client_name="tweaker", port_name="output_notes")
    print("Connecting LED input")
    midiin, port_name = open_midiinput(port=port_tweaker, client_name="tweaker", port_name="input")

except (EOFError, KeyboardInterrupt):
    sys.exit()

### Init start ###

rgbButtons = {}
pots = {}

rgbButtonsQueue = []

NOTE_BASE_G = 7
NOTE_STRING_DIFF = 5
OCTAVE = 5
STR_MOD = 0
TONE_MOD = 0
updateButtonState = False

def colorNotesBackground():
    # passive coloring
    for key in rgbButtons:
        button = rgbButtons[key]
        button.note.setState(False)
        # color black tones
        if (button.getRow() in range(0, 4)):
            if (button.note.getMidi() % 12 in [1, 3, 5, 8, 10]):
                button.color.setColorGreen()
            else:
                button.color.setColorWhite()
        # color tone c
        if (button.getRow() in range(0, 4)):
            if (button.note.getMidi() % 12 == 0):
                button.color.setColorRed()

def colorNotesForeground():
    # active coloring
    for key in rgbButtons:
        button = rgbButtons[key]
        if (button.getRow() in range(0, 4)):
            if (button.isState()):
                button.color.setColorBlue()

def setMidiNotes():
    for key in rgbButtons:
        button = rgbButtons[key]
        # set notes based on bass
        if (button.getRow() in range(0, 4)):
            formula = (NOTE_BASE_G + TONE_MOD) + (OCTAVE * 12) - (NOTE_STRING_DIFF * (button.getRow() + STR_MOD)) + button.getCol()
            button.note.setMidi(formula)

for midi in SOFT_TOUCH_BUTTONS:
    rgbButtons[midi] = RgbButton(midi)

for midi in POTENTIOMETERS:
    pots[midi] = Pot(midi)

for key in rgbButtons:
    button = rgbButtons[key]
    button.color.setColorOff()
    setMidiNotes()

def setUpdateButton(state):
    global updateButtonState
    updateButtonState = state

def isUpdateButton():
    global updateButtonState
    return(updateButtonState)

def updateButton(key):
    button = rgbButtons[key]
    # handle buttonPress
    if (button.isUpdate()):
        if (button.isState()):
            button.color.setColorBlue()
            button.note.setState(True)
        else:
            button.color.setColorOff()
            colorNotesBackground()
            button.note.setState(False)
        button.setUpdate(False)
    # handle buttonNote
    if (button.note.isUpdate()):
        if (button.note.isState()):
            midiout_notes.send_message([NOTE_ON, button.note.getMidi(), 127])
        else:
            midiout_notes.send_message([NOTE_ON, button.note.getMidi(), 0])
        button.note.setUpdate(False)
    # handle buttonColor
    if (button.color.isUpdate()):
        midiout_led.send_message([NOTE_ON, button.getMidi(), button.color.getColor()])
        button.color.setUpdate(False)

def updatePot():
    global STR_MOD
    global TONE_MOD
    for key in pots:
         pot = pots[key]
         if (pot.isUpdate()):
            if (pot.getMidi() == POTENTIOMETERS[1]):
                str_mod = int(pot.getValue() / 16) - 4
                STR_MOD = str_mod
                setMidiNotes()
                colorNotesBackground()
                for key in rgbButtons:
                    updateButton(key)
            elif (pot.getMidi() == POTENTIOMETERS[2]):
#                tone_mod = (int(pot.getValue() / 16) - 4) * -1
#                TONE_MOD = tone_mod
#                setMidiNotes()
#                colorNotesBackground()
#                for key in rgbButtons:
#                    updateButton(key)
                #print(pot.getValue())
                midiout_notes.send_message([176, pot.getMidi(), pot.getValue()])
            else:
                #print(pot.getValue())
                midiout_notes.send_message([176, pot.getMidi(), pot.getValue()])
            pot.setUpdate(False)

def processMidi(message):
    if message[1] in SOFT_TOUCH_BUTTONS:
        button = rgbButtons[message[1]]
        if (message[2] == 127):
            button.setState(True)
            rgbButtonsQueue.insert(0, message[1])
        elif (message[2] == 0):
            button.setState(False)
            rgbButtonsQueue.insert(0, message[1])
    elif message[1] in POTENTIOMETERS and message[0] == 176:
        pot = pots[message[1]]
        pot.setValue(message[2])

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()
    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        #print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        processMidi(message)

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    while True:
        if rgbButtonsQueue:
            updateButton(rgbButtonsQueue.pop())
        updatePot()
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
    del midiout_led
    del midiout_notes

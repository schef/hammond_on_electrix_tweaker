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


#log = logging.getLogger('midiout_led')
#logging.basicConfig(level=logging.DEBUG)

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

NOTE_BASE_G = 7
NOTE_STRING_DIFF = 5
OCTAVE = 5
STR_MOD = 0
TONE_MOD = 0

def colorNotes():
    for key in rgbButtons:
        button = rgbButtons[key]
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
    colorNotes()


def updateButtons():
    for key in rgbButtons:
        button = rgbButtons[key]
        # notes
        if (button.isUpdate()):
            if (button.getState()):
                midiout_notes.send_message([NOTE_ON, button.note.getMidi(), 127])
                #button.color.setColorRandom()
            else:
                midiout_notes.send_message([NOTE_ON, button.note.getMidi(), 0])
                #button.color.setColorOff()
            button.unsetUpdate()
        # color
        if (button.color.isUpdate()):
            midiout_led.send_message([NOTE_ON, button.getMidi(), button.color.getColor()])
            button.color.unsetUpdate()

def updatePot():
    global STR_MOD
    global TONE_MOD
    for key in pots:
         pot = pots[key]
         if (pot.isUpdate()):
            if (pot.getMidi() == POTENTIOMETERS[0]):
                str_mod = int(pot.getValue() / 16) - 4
                STR_MOD = str_mod
                setMidiNotes()
                colorNotes()
            elif (pot.getMidi() == POTENTIOMETERS[2]):
                tone_mod = (int(pot.getValue() / 16) - 4) * -1
                TONE_MOD = tone_mod
                setMidiNotes()
                colorNotes()
            else:
                print(pot.getValue())
            pot.unsetUpdate()

def processMidi(message):
    if message[1] in SOFT_TOUCH_BUTTONS:
        button = rgbButtons[message[1]]
        if (message[2] == 127):
            button.setState(True)
        elif (message[2] == 0):
            button.setState(False)
    elif message[1] in POTENTIOMETERS and message[0] == 176:
        pot = pots[message[1]]
        pot.setValue(message[2])

### Init end ###

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()
    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        processMidi(message)

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        #time.sleep(1)
        updateButtons()
        updatePot()
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
    del midiout_led
    del midiout_notes

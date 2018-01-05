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

for midi in SOFT_TOUCH_BUTTONS:
    rgbButtons[midi] = RgbButton(midi)

for midi in POTENTIOMETERS:
    pots[midi] = Pot(midi)

for key in rgbButtons:
    button = rgbButtons[key]
    button.color.setColorOff()

def updateButtons():
    for key in rgbButtons:
        button = rgbButtons[key]
        # notes
        if (button.isUpdate()):
            if (button.getState()):
                midiout_notes.send_message([NOTE_ON, button.getMidi(), 127])
                button.color.setColorRandom()
            else:
                midiout_notes.send_message([NOTE_ON, button.getMidi(), 0])
                button.color.setColorOff()
            button.unsetUpdate()
        # color
        if (button.color.isUpdate()):
            midiout_led.send_message([NOTE_ON, button.getMidi(), button.color.getColor()])
            button.color.unsetUpdate()

def updatePot():
    for key in pots:
         pot = pots[key]
         if (pot.isUpdate()):
           print(pot.getValue())
           pot.unsetUpdate()

def processMidi(message):
    if message[1] in SOFT_TOUCH_BUTTONS:
        button = rgbButtons[message[1]]
        if (message[2] == 127):
            button.setState(True)
        elif (message[2] == 0):
            button.setState(False)
    elif message[1] in POTENTIOMETERS:
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

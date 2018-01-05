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


log = logging.getLogger('midiout_led')
logging.basicConfig(level=logging.DEBUG)

port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiout_led, port_name = open_midioutput(port=port, client_name="tweaker", port_name="output_led")
    midiout_notes, port_name = open_midioutput(port=None, client_name="tweaker", port_name="output_notes")
    midiin, port_name = open_midiinput(port=port, client_name="tweaker", port_name="input")

except (EOFError, KeyboardInterrupt):
    sys.exit()

### Init start ###

rgbButtons = {}

for midi in SOFT_TOUCH_BUTTONS:
    rgbButtons[midi] = RgbButton(midi)

for key in rgbButtons:
    button = rgbButtons[key]
    button.color.setColorOff()
    if (button.color.isUpdate()):
        print(button.color.getColor())
        midiout_led.send_message([NOTE_ON, button.getMidi(), button.color.getColor()])
        button.color.unsetUpdate()

def processMidi(message):
    button = rgbButtons[message[1]]
    if (message[2] > 38):
        return
    if (message[2] == 127):
        button.color.setColorGreen()
    elif (message[2] == 0):
        button.color.setColorOff()
    if (button.color.isUpdate()):
        print(button.color.getColor())
        midiout_led.send_message([NOTE_ON, button.getMidi(), button.color.getColor()])
        button.color.unsetUpdate()

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
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
    del midiout_led
    del midiout_notes

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
from rtmidi.midiconstants import NOTE_ON
from rtmidi.midiutil import open_midiinput

from tweaker_macro import *

from enum import Enum

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
START_OCTAVE = 5


# def colorNotesBackground():
#     # passive coloring
#     for key in rgbButtons:
#         button = rgbButtons[key]
#         button.note.setState(False)
#         # color black tones
#         if (button.getRow() in range(0, 4)):
#             if (button.note.getMidi() % 12 in [1, 3, 5, 8, 10]):
#                 button.color.setColorGreen()
#             else:
#                 button.color.setColorWhite()
#         # color tone c
#         if (button.getRow() in range(0, 4)):
#             if (button.note.getMidi() % 12 == 0):
#                 button.color.setColorRed()
#
#
# def colorNotesForeground():
#     # active coloring
#     for key in rgbButtons:
#         button = rgbButtons[key]
#         if (button.getRow() in range(0, 4)):
#             if (button.isState()):
#                 button.color.setColorBlue()
#
#
# def setMidiNotes():
#     for key in rgbButtons:
#         button = rgbButtons[key]
#         # set notes based on bass
#         if (button.getRow() in range(0, 4)):
#             formula = (NOTE_BASE_G + TONE_MOD) + (OCTAVE * 12) - (
#                         NOTE_STRING_DIFF * (button.getRow() + STR_MOD)) + button.getCol()
#             button.note.setMidi(formula)
#
#
# for midi in SOFT_TOUCH_BUTTONS:
#     rgbButtons[midi] = RgbButton(midi)
#
# for midi in POTENTIOMETERS:
#     pots[midi] = Pot(midi)
#
# for key in rgbButtons:
#     button = rgbButtons[key]
#     button.color.setColorOff()
#     setMidiNotes()
#
#
# def setUpdateButton(state):
#     global updateButtonState
#     updateButtonState = state
#
#
# def isUpdateButton():
#     global updateButtonState
#     return (updateButtonState)
#
#
# def updateButton(key):
#     button = rgbButtons[key]
#     # handle buttonPress
#     if (button.isUpdate()):
#         if (button.isState()):
#             button.color.setColorBlue()
#             button.note.setState(True)
#         else:
#             button.color.setColorOff()
#             colorNotesBackground()
#             button.note.setState(False)
#         button.setUpdate(False)
#     # handle buttonNote
#     if (button.note.isUpdate()):
#         if (button.note.isState()):
#             midiout_notes.send_message([NOTE_ON, button.note.getMidi(), 127])
#         else:
#             midiout_notes.send_message([NOTE_ON, button.note.getMidi(), 0])
#         button.note.setUpdate(False)
#     # handle buttonColor
#     if (button.color.isUpdate()):
#         midiout_led.send_message([NOTE_ON, button.getMidi(), button.color.getColor()])
#         button.color.setUpdate(False)
#
#
# def updatePot():
#     global STR_MOD
#     global TONE_MOD
#     for key in pots:
#         pot = pots[key]
#         if (pot.isUpdate()):
#             if (pot.getMidi() == POTENTIOMETERS[1]):
#                 str_mod = int(pot.getValue() / 16) - 4
#                 STR_MOD = str_mod
#                 setMidiNotes()
#                 colorNotesBackground()
#                 for key in rgbButtons:
#                     updateButton(key)
#             elif (pot.getMidi() == POTENTIOMETERS[2]):
#                 #tone_mod = (int(pot.getValue() / 16) - 4) * -1
#                 #TONE_MOD = tone_mod
#                 #setMidiNotes()
#                 #colorNotesBackground()
#                 #for key in rgbButtons:
#                 #
#                 #updateButton(key)
#                 #print(pot.getValue())
#                 #midiout_notes.send_message([176, pot.getMidi(), pot.getValue()])
#                 midiout_notes.send_message([176, 11, pot.getValue()])
#             else:
#                 # print(pot.getValue())
#                 # midiout_notes.send_message([176, pot.getMidi(), pot.getValue()])
#                 midiout_notes.send_message([176, 1, pot.getValue()])
#             pot.setUpdate(False)
#
#
# def processMidi(message):
#     if message[1] in SOFT_TOUCH_BUTTONS:
#         button = rgbButtons[message[1]]
#         if (message[2] == 127):
#             button.setState(True)
#             rgbButtonsQueue.insert(0, message[1])
#         elif (message[2] == 0):
#             button.setState(False)
#             rgbButtonsQueue.insert(0, message[1])
#     elif message[1] in POTENTIOMETERS and message[0] == 176:
#         pot = pots[message[1]]
#         pot.setValue(message[2])


class TweakerNoteOnEnum(Enum):
    BUTTON_ROW1_COL1 = 1
    BUTTON_ROW1_COL2 = 2
    BUTTON_ROW1_COL3 = 3
    BUTTON_ROW1_COL4 = 4
    BUTTON_ROW1_COL5 = 5
    BUTTON_ROW1_COL6 = 6
    BUTTON_ROW1_COL7 = 7
    BUTTON_ROW1_COL8 = 8
    BUTTON_ROW2_COL1 = 9
    BUTTON_ROW2_COL2 = 10
    BUTTON_ROW2_COL3 = 11
    BUTTON_ROW2_COL4 = 12
    BUTTON_ROW2_COL5 = 13
    BUTTON_ROW2_COL6 = 14
    BUTTON_ROW2_COL7 = 15
    BUTTON_ROW2_COL8 = 16
    BUTTON_ROW3_COL1 = 17
    BUTTON_ROW3_COL2 = 18
    BUTTON_ROW3_COL3 = 19
    BUTTON_ROW3_COL4 = 20
    BUTTON_ROW3_COL5 = 21
    BUTTON_ROW3_COL6 = 22
    BUTTON_ROW3_COL7 = 23
    BUTTON_ROW3_COL8 = 24
    BUTTON_ROW4_COL1 = 25
    BUTTON_ROW4_COL2 = 26
    BUTTON_ROW4_COL3 = 27
    BUTTON_ROW4_COL4 = 28
    BUTTON_ROW4_COL5 = 29
    BUTTON_ROW4_COL6 = 30
    BUTTON_ROW4_COL7 = 31
    BUTTON_ROW4_COL8 = 32
    BUTTON_GRID_NAVIGATION_UP = 39
    BUTTON_GRID_NAVIGATION_DOWN = 41
    BUTTON_GRID_NAVIGATION_LEFT = 42
    BUTTON_GRID_NAVIGATION_RIGHT = 43
    BUTTON_GRID_NAVIGATION_CENTER = 40
    BUTTON_AB_ASSIGN_LEFT = 35
    BUTTON_AB_ASSIGN_RIGHT = 38
    BUTTON_SOLO_LEFT = 33
    BUTTON_SOLO_RIGHT = 36
    BUTTON_RECORD_ARM_LEFT = 34
    BUTTON_RECORD_ARM_RIGHT = 37
    PAD_ROW1_COL1 = 63
    PAD_ROW1_COL2 = 64
    PAD_ROW1_COL3 = 65
    PAD_ROW1_COL4 = 66
    PAD_ROW2_COL1 = 67
    PAD_ROW2_COL2 = 68
    PAD_ROW2_COL3 = 69
    PAD_ROW2_COL4 = 70
    SLIDER_LEFT = 53
    SLIDER_RIGHT = 54
    ENCODER_HIGH_LEFT = 45
    ENCODER_MID_LEFT = 46
    ENCODER_LOW_LEFT = 47
    ENCODER_HIGH_RIGHT = 48
    ENCODER_MID_RIGHT = 49
    ENCODER_LOW_RIGHT = 50
    POT_LEFT = 51
    POT_RIGHT = 52
    TRACK_SELECT = 44


class TweakerControlChangeEnum(Enum):
    PAD_ROW1_COL1 = 71
    PAD_ROW1_COL2 = 72
    PAD_ROW1_COL3 = 73
    PAD_ROW1_COL4 = 74
    PAD_ROW2_COL1 = 75
    PAD_ROW2_COL2 = 76
    PAD_ROW2_COL3 = 77
    PAD_ROW2_COL4 = 78
    SLIDER_LEFT = 53
    SLIDER_RIGHT = 54
    SLIDER_CENTER = 55
    ENCODER_HIGH_LEFT = 57
    ENCODER_MID_LEFT = 58
    ENCODER_LOW_LEFT = 59
    ENCODER_HIGH_RIGHT = 60
    ENCODER_MID_RIGHT = 61
    ENCODER_LOW_RIGHT = 62
    POT_LEFT = 51
    POT_RIGHT = 52
    TRACK_SELECT = 56


class TweakerCommandNameEnum(Enum):
    NOTE_ON = 144
    CONTROL_CHANGE = 176


class Button:
    def __init__(self, midi):
        self.midi = midi
        self.state = False

    def is_state(self):
        return(self.state)

    def set_state(self, state):
        self.state = state
        self.execute()

    def execute(self):
        print(self.midi, self.state)
        midiout_notes.send_message([TweakerCommandNameEnum.NOTE_ON.value, self.midi, self.state])


class Slider:
    def __init__(self, midi):
        self.midi = midi
        self.state = 0

    def is_state(self):
        return(self.state)

    def set_state(self, state):
        self.state = state
        self.execute()

    def execute(self):
        print(self.midi, self.state)
        midiout_notes.send_message([TweakerCommandNameEnum.CONTROL_CHANGE.value, self.midi, self.state])


buttonsDict = dict()
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL1] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL2] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL3] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL4] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL5] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL6] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL7] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL8] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 8)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL1] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL2] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL3] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL4] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL5] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL6] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL7] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL8] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 8)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL1] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL2] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL3] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL4] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL5] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL6] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL7] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL8] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 8)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL1] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL2] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL3] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL4] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL5] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL6] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL7] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL8] = Button(NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 8)


sliderDict = dict()
sliderDict[TweakerControlChangeEnum.SLIDER_LEFT] = Slider(11)
sliderDict[TweakerControlChangeEnum.SLIDER_RIGHT] = Slider(1)
sliderDict[TweakerControlChangeEnum.SLIDER_CENTER] = Slider(2)


def processBotnu(message):
    command = TweakerCommandNameEnum(message[0])
    note = TweakerNoteOnEnum(message[1])
    control = TweakerControlChangeEnum(message[1])
    state = message[2]
    if command == TweakerCommandNameEnum.NOTE_ON:
        if note not in buttonsDict: pass
        buttonsDict[note].set_state(state)
    elif command == TweakerCommandNameEnum.CONTROL_CHANGE:
        if control not in sliderDict: pass
        sliderDict[control].set_state(state)

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        processBotnu(message)
        # processMidi(message)


print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    while True:
        pass
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
    del midiout_led
    del midiout_notes

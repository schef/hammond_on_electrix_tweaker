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
    print("ToTweaker")
    midiout_led, port_name = open_midioutput(port=port_tweaker, client_name="tweaker", port_name="ToTweaker")
    print("Output")
    midiout_notes, port_name = open_midioutput(port=port_hammond, client_name="tweaker", port_name="Output")
    print("FromTweaker")
    midiin, port_name = open_midiinput(port=port_tweaker, client_name="tweaker", port_name="FromTweaker")

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


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class InternalData(metaclass=Singleton):
    velocity = 100
    midiOffsetHorizontal = 0
    midiOffsetVertical = 0
    colors = {
    "OFF"     : 0,
    "GREEN"   : 1,
    "RED"     : 4,
    "YELLOW"  : 8,
    "BLUE"    : 16,
    "CYAN"    : 32,
    "MAGENTA" : 64,
    "WHITE"   : 127
    }

    def __init__(self):
        pass

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        print("set_velocity: ", self.velocity)

    def get_midi_offset(self):
        return self.midiOffsetVertical + self.midiOffsetHorizontal

    def set_midi_offset_vertical(self, value):
        self.midiOffsetVertical += value
        print("midiOffset: ", self.get_midi_offset())
        self.set_colors()

    def set_midi_offset_horizontal(self, value):
        self.midiOffsetHorizontal += value
        print("midiOffset: ", self.get_midi_offset())
        self.set_colors()

    def reset_midi_offset(self):
        self.midiOffsetVertical = 0
        self.midiOffsetHorizontal = 0
        print("midiOffset: ", self.get_midi_offset())
        self.set_colors()

    def set_colors_for_music_tones(self):
        for button in buttonsDict:
            if buttonsDict[button].get_play_midi() == 60:
                midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, buttonsDict[button].get_manuf_midi(), self.colors["RED"]])
            elif buttonsDict[button].get_play_midi() == 60 + 12:
                midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, buttonsDict[button].get_manuf_midi(), self.colors["MAGENTA"]])
            elif buttonsDict[button].get_play_midi() == 60 + 12 + 12:
                midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, buttonsDict[button].get_manuf_midi(), self.colors["YELLOW"]])
            elif buttonsDict[button].get_play_midi() == 60 - 12:
                midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, buttonsDict[button].get_manuf_midi(), self.colors["GREEN"]])
            elif buttonsDict[button].get_play_midi() == 60 - 12 - 12:
                midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, buttonsDict[button].get_manuf_midi(), self.colors["BLUE"]])
            elif buttonsDict[button].get_play_midi() > 127 or buttonsDict[button].get_play_midi() < 0:
                midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, buttonsDict[button].get_manuf_midi(), self.colors["CYAN"]])
            else:
                midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, buttonsDict[button].get_manuf_midi(), self.colors["OFF"]])

    def set_colors_for_midi_offset(self):
        if self.get_midi_offset():
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_CENTER.value, self.colors["OFF"]])
        else:
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_CENTER.value, self.colors["WHITE"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_UP.value, self.colors["OFF"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_DOWN.value, self.colors["OFF"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_LEFT.value, self.colors["OFF"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_RIGHT.value, self.colors["OFF"]])
        if self.midiOffsetVertical > 0:
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_UP.value, self.colors["OFF"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_DOWN.value, self.colors["WHITE"]])
        elif self.midiOffsetVertical < 0:
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_UP.value, self.colors["WHITE"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_DOWN.value, self.colors["OFF"]])
        if self.midiOffsetHorizontal > 0:
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_LEFT.value, self.colors["WHITE"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_RIGHT.value, self.colors["OFF"]])
        elif self.midiOffsetHorizontal < 0:
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_LEFT.value, self.colors["OFF"]])
            midiout_led.send_message([TweakerStatusByteEnum.NOTE_ON.value, TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_RIGHT.value, self.colors["WHITE"]])

    def set_colors(self):
        self.set_colors_for_music_tones()
        self.set_colors_for_midi_offset()



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


class TweakerStatusByteEnum(Enum):
    NOTE_ON = 144
    CONTROL_CHANGE = 176


class EmptyDevice:
    init_midi = 0
    velocity = 0
    manuf_midi = 0

    def get_velocity(self):
        if self.velocity:
            return InternalData().get_velocity()
        else:
            return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        self.execute()

    def get_play_midi(self):
        return self.init_midi + InternalData().get_midi_offset()

    def get_manuf_midi(self):
        return self.manuf_midi

    def execute(self):
        pass


class Button(EmptyDevice):

    def __init__(self, manuf_midi, init_midi):
        self.manuf_midi = manuf_midi
        self.init_midi = init_midi

    def execute(self):
        print(self.get_play_midi(), self.get_velocity())
        midiout_notes.send_message([TweakerStatusByteEnum.NOTE_ON.value, self.get_play_midi(), self.get_velocity()])


class Slider(EmptyDevice):
    def __init__(self, init_midi):
        self.init_midi = init_midi

    def execute(self):
        print(self.init_midi, self.velocity)
        midiout_notes.send_message([TweakerStatusByteEnum.CONTROL_CHANGE.value, self.init_midi, self.velocity])


class InternalVelocity(EmptyDevice):
    def execute(self):
        InternalData().set_velocity(self.velocity)


class InternalMidiOffset(EmptyDevice):

    def __init__(self, manuf_midi):
        self.manuf_midi = manuf_midi

    def execute(self):
        if self.velocity:
            if self.manuf_midi == TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_UP.value:
                InternalData().set_midi_offset_vertical(-5)
            elif self.manuf_midi == TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_DOWN.value:
                InternalData().set_midi_offset_vertical(+5)
            elif self.manuf_midi == TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_LEFT.value:
                InternalData().set_midi_offset_horizontal(+1)
            elif self.manuf_midi == TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_RIGHT.value:
                InternalData().set_midi_offset_horizontal(-1)
            elif self.manuf_midi == TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_CENTER.value:
                InternalData().reset_midi_offset()


##### REGITER DEVICES #####

buttonsDict = dict()
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL1.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL1.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL2.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL2.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL3.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL3.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL4.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL4.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL5.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL5.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL6.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL6.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL7.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL7.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW1_COL8.name] = Button(TweakerNoteOnEnum.BUTTON_ROW1_COL8.value, NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 8)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL1.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL1.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL2.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL2.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL3.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL3.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL4.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL4.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL5.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL5.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL6.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL6.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL7.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL7.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW2_COL8.name] = Button(TweakerNoteOnEnum.BUTTON_ROW2_COL8.value, NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 8)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL1.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL1.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL2.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL2.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL3.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL3.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL4.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL4.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL5.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL5.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL6.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL6.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL7.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL7.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW3_COL8.name] = Button(TweakerNoteOnEnum.BUTTON_ROW3_COL8.value, NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 8)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL1.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL1.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 1)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL2.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL2.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 2)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL3.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL3.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 3)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL4.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL4.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 4)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL5.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL5.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 5)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL6.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL6.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 6)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL7.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL7.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 7)
buttonsDict[TweakerNoteOnEnum.BUTTON_ROW4_COL8.name] = Button(TweakerNoteOnEnum.BUTTON_ROW4_COL8.value, NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 8)

midiOffsetDict = dict()
midiOffsetDict[TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_UP.name] = InternalMidiOffset(TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_UP.value)
midiOffsetDict[TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_DOWN.name] = InternalMidiOffset(TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_DOWN.value)
midiOffsetDict[TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_LEFT.name] = InternalMidiOffset(TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_LEFT.value)
midiOffsetDict[TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_RIGHT.name] = InternalMidiOffset(TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_RIGHT.value)
midiOffsetDict[TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_CENTER.name] = InternalMidiOffset(TweakerNoteOnEnum.BUTTON_GRID_NAVIGATION_CENTER.value)

sliderDict = dict()
sliderDict[TweakerControlChangeEnum.SLIDER_LEFT.name] = Slider(11)
sliderDict[TweakerControlChangeEnum.PAD_ROW2_COL1.name] = Slider(1)
sliderDict[TweakerControlChangeEnum.SLIDER_CENTER.name] = Slider(1)
sliderDict[TweakerControlChangeEnum.ENCODER_LOW_LEFT.name] = InternalVelocity()



def item_exists(my_object, item):
    try:
        my_object(item)
    except ValueError:
        return False
    return True


def processBotnu(message):
    status = message[0]
    status_byte_1 = message[1]
    status_byte_2 = message[2]

    if item_exists(TweakerStatusByteEnum, status):
        command = TweakerStatusByteEnum(status).name
    else:
        return

    if command == TweakerStatusByteEnum.NOTE_ON.name:
        if item_exists(TweakerNoteOnEnum, status_byte_1):
            note = TweakerNoteOnEnum(status_byte_1).name
        else:
            return
    elif command == TweakerStatusByteEnum.CONTROL_CHANGE.name:
        if item_exists(TweakerControlChangeEnum, status_byte_1):
            control = TweakerControlChangeEnum(status_byte_1).name
        else:
            return
    else:
        return

    state = status_byte_2

    if command == TweakerStatusByteEnum.NOTE_ON.name:
        if note in buttonsDict:
            buttonsDict[note].set_velocity(state)
        elif note in midiOffsetDict:
            midiOffsetDict[note].set_velocity(state)
    elif command == TweakerStatusByteEnum.CONTROL_CHANGE.name:
        if control not in sliderDict: return
        sliderDict[control].set_velocity(state)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        processBotnu(message)


print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    InternalData().set_colors()
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

#!/usr/bin/env python3

import random

SOFT_TOUCH_BUTTONS = [i for i in range (1, 38 + 1)]
POTENTIOMETERS = [53, 54, 55]

class RgbLedColor:
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
        self.update = False
        self.setColorOff()
    def isUpdate(self):
        return(self.update)
    def setUpdate(self, state):
        self.update = True
    def getColor(self):
        return(self.color)
    def setColor(self, color):
        self.color = color
        self.setUpdate(True)
    def setColorOff(self):
        self.setColor(self.colors["OFF"])
    def setColorGreen(self):
        self.setColor(self.colors["GREEN"])
    def setColorRed(self):
        self.setColor(self.colors["RED"])
    def setColorYellow(self):
        self.setColor(self.colors["YELLOW"])
    def setColorBlue(self):
        self.setColor(self.colors["BLUE"])
    def setColorCyan(self):
        self.setColor(self.colors["CYAN"])
    def setColorMagenta(self):
        self.setColor(self.colors["MAGENTA"])
    def setColorWhite(self):
        self.setColor(self.colors["WHITE"])
    def setColorRandom(self):
        colorList = list(self.colors.values())
        colorList.remove(self.colors['OFF'])
        color = random.choice(colorList)
        print(color)
        self.setColor(color)

class RgbButtonNote:
    def __init__(self, midi):
        self.midi = midi
        self.state = False
        self.update = False
    def getMidi(self):
        return(self.midi)
    def setMidi(self, midi):
        self.midi = midi
    def isState(self):
        return(self.state)
    def setState(self, state):
        self.state = state
        self.setUpdate(True)
    def isUpdate(self):
        return(self.update)
    def setUpdate(self, state):
        self.update = state
    #def changeOctave(self, multiplier):
    #    self.midi += multiplier * 12

class RgbButton:
    def __init__(self, midi):
        self.midi = midi
        self.state = False
        self.update = False
        self.color = RgbLedColor()
        self.note = RgbButtonNote(midi)
        self.row = int((midi - 1) / 8)
        self.col = (midi - 1) % 8
    def getMidi(self):
        return(self.midi)
    def isState(self):
        return(self.state)
    def setState(self, state):
        self.state = state
        self.setUpdate(True)
    def isUpdate(self):
        return(self.update)
    def setUpdate(self, state):
        self.update = state
    def getRow(self):
        return(self.row)
    def getCol(self):
        return(self.col)

class Pot:
    def __init__(self, midi):
        self.midi = midi
        self.value = 0
        self.update = False
    def getMidi(self):
        return(self.midi)
    def getValue(self):
        return(self.value)
    def setValue(self, value):
        self.value = value
        self.setUpdate(True)
    def isUpdate(self):
        return(self.update)
    def setUpdate(self, state):
        self.update = state

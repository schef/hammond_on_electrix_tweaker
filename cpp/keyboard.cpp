#include <stdio.h>

#include "keyboard.hpp"
#include "midi_parser.hpp"
#include "midi_player.hpp"

#define FILE_NAME "keyboard: "

Keyboard *Keyboard::_instance = nullptr;

Keyboard *Keyboard::getInstance() {
  if (_instance == nullptr) {
    _instance = new Keyboard();
  }
  return _instance;
}

Keyboard::Keyboard() { printf(FILE_NAME "constructor\n"); }

uint8_t Keyboard::getVelocity() { return _velocity; }

void Keyboard::setVelocity(uint8_t velocity) {
  printf(FILE_NAME "setVelocity: %d\n", _velocity);
  _velocity = velocity;
}

int Keyboard::getMidiOffset() {
  return _midiOffsetVertical + _midiOffsetHorizontal;
}

void Keyboard::setMidiOffsetVertical(int value) {
  _midiOffsetVertical += value;
  printf(FILE_NAME "midiOffset: %d\n", getMidiOffset());
  setColors();
}

void Keyboard::setMidiOffsetHorizontal(int value) {
  _midiOffsetHorizontal += value;
  printf(FILE_NAME "midiOffset: %d\n", getMidiOffset());
  setColors();
}

void Keyboard::resetMidiOffset() {
  _midiOffsetVertical = 0;
  _midiOffsetHorizontal = 0;
  printf(FILE_NAME "midiOffset: %d\n", getMidiOffset());
  setColors();
}

void Keyboard::setColorsForMusicTones() {
  for (uint8_t i = 0; i < sizeof(midiStateHolder) / sizeof(MidiStateHolder);
       i++) {
    if (midiStateHolder[i].wantedMidi + getMidiOffset() == 60) {
      std::vector<unsigned char> note = {
          MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::RED};
      MidiPlayer::getInstance()->sendMessageOutTweaker(&note);
    } else if (midiStateHolder[i].wantedMidi + getMidiOffset() == 60 + 12) {
      std::vector<unsigned char> note = {MidiParser::NOTE_ON,
                                         midiStateHolder[i].originalMidi,
                                         Colors::MAGENTA};
      MidiPlayer::getInstance()->sendMessageOutTweaker(&note);
    } else if (midiStateHolder[i].wantedMidi + getMidiOffset() ==
               60 + 12 + 12) {
      std::vector<unsigned char> note = {
          MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::YELLOW};
      MidiPlayer::getInstance()->sendMessageOutTweaker(&note);
    } else if (midiStateHolder[i].wantedMidi + getMidiOffset() == 60 - 12) {
      std::vector<unsigned char> note = {
          MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::GREEN};
      MidiPlayer::getInstance()->sendMessageOutTweaker(&note);
    } else if (midiStateHolder[i].wantedMidi + getMidiOffset() ==
               60 - 12 - 12) {
      std::vector<unsigned char> note = {
          MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::BLUE};
      MidiPlayer::getInstance()->sendMessageOutTweaker(&note);
    } else if (midiStateHolder[i].wantedMidi + getMidiOffset() > 127 or
               midiStateHolder[i].wantedMidi + getMidiOffset() < 0) {
      std::vector<unsigned char> note = {
          MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::CYAN};
      MidiPlayer::getInstance()->sendMessageOutTweaker(&note);
    } else {
      std::vector<unsigned char> note = {
          MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::OFF};
      MidiPlayer::getInstance()->sendMessageOutTweaker(&note);
    }
  }
}

void Keyboard::setColorsForMidiOffset() {
  if (getMidiOffset()) {
    std::vector<unsigned char> note0 = {
        MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_CENTER,
        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note0);

  } else {
    std::vector<unsigned char> note1 = {
        MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_CENTER,
        Colors::WHITE};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note1);

    std::vector<unsigned char> note2 = {MidiParser::NOTE_ON,
                                        MidiParser::BUTTON_GRID_NAVIGATION_UP,
                                        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note2);

    std::vector<unsigned char> note3 = {MidiParser::NOTE_ON,
                                        MidiParser::BUTTON_GRID_NAVIGATION_DOWN,
                                        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note3);

    std::vector<unsigned char> note4 = {MidiParser::NOTE_ON,
                                        MidiParser::BUTTON_GRID_NAVIGATION_LEFT,
                                        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note4);

    std::vector<unsigned char> note5 = {
        MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_RIGHT,
        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note5);
  }

  if (_midiOffsetVertical > 0) {
    std::vector<unsigned char> note6 = {MidiParser::NOTE_ON,
                                        MidiParser::BUTTON_GRID_NAVIGATION_UP,
                                        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note6);

    std::vector<unsigned char> note7 = {MidiParser::NOTE_ON,
                                        MidiParser::BUTTON_GRID_NAVIGATION_DOWN,
                                        Colors::WHITE};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note7);

  } else if (_midiOffsetVertical < 0) {
    std::vector<unsigned char> note8 = {MidiParser::NOTE_ON,
                                        MidiParser::BUTTON_GRID_NAVIGATION_UP,
                                        Colors::WHITE};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note8);

    std::vector<unsigned char> note9 = {MidiParser::NOTE_ON,
                                        MidiParser::BUTTON_GRID_NAVIGATION_DOWN,
                                        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note9);
  }

  if (_midiOffsetHorizontal > 0) {
    std::vector<unsigned char> note10 = {
        MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_LEFT,
        Colors::WHITE};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note10);

    std::vector<unsigned char> note11 = {
        MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_RIGHT,
        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note11);

  } else if (_midiOffsetHorizontal < 0) {
    std::vector<unsigned char> note12 = {
        MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_LEFT,
        Colors::OFF};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note12);

    std::vector<unsigned char> note13 = {
        MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_RIGHT,
        Colors::WHITE};
    MidiPlayer::getInstance()->sendMessageOutTweaker(&note13);
  }
}

void Keyboard::setColors() {
  setColorsForMusicTones();
  setColorsForMidiOffset();
}

void Keyboard::setMidiState(uint8_t midiNote, bool state) {
  uint8_t midiNoteWithOffset;
  for (uint8_t i = 0; i < sizeof(midiStateHolder) / sizeof(MidiStateHolder);
       i++) {
    if (midiStateHolder[i].originalMidi == midiNote) {
      midiNoteWithOffset = midiStateHolder[i].wantedMidi + getMidiOffset();
      break;
    }
  }
  std::vector<unsigned char> note = {MidiParser::NOTE_ON, midiNoteWithOffset,
                                     _velocity};
  if (!state) {
    note.at(2) = 0;
  }
  MidiPlayer::getInstance()->sendMessageOut(&note);
}
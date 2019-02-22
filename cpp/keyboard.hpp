#ifndef __KEYBOARD_HPP__
#define __KEYBOARD_HPP__

#include <stdint.h>

#include "midi_parser.hpp"

#define NOTE_BASE_G 7
#define NOTE_STRING_DIFF 5
#define START_OCTAVE 5

class Keyboard {
private:
  struct MidiStateHolder {
    uint8_t originalMidi;
    uint8_t wantedMidi;
    uint8_t originalVelocity;
  };
  MidiStateHolder midiStateHolder[4 * 8] = {
      {MidiParser::BUTTON_ROW1_COL1,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 1, 0},
      {MidiParser::BUTTON_ROW1_COL2,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 2, 0},
      {MidiParser::BUTTON_ROW1_COL3,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 3, 0},
      {MidiParser::BUTTON_ROW1_COL4,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 4, 0},
      {MidiParser::BUTTON_ROW1_COL5,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 5, 0},
      {MidiParser::BUTTON_ROW1_COL6,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 6, 0},
      {MidiParser::BUTTON_ROW1_COL7,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 7, 0},
      {MidiParser::BUTTON_ROW1_COL8,
       NOTE_BASE_G - NOTE_STRING_DIFF * 0 + START_OCTAVE * 12 + 8, 0},
      {MidiParser::BUTTON_ROW2_COL1,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 1, 0},
      {MidiParser::BUTTON_ROW2_COL2,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 2, 0},
      {MidiParser::BUTTON_ROW2_COL3,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 3, 0},
      {MidiParser::BUTTON_ROW2_COL4,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 4, 0},
      {MidiParser::BUTTON_ROW2_COL5,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 5, 0},
      {MidiParser::BUTTON_ROW2_COL6,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 6, 0},
      {MidiParser::BUTTON_ROW2_COL7,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 7, 0},
      {MidiParser::BUTTON_ROW2_COL8,
       NOTE_BASE_G - NOTE_STRING_DIFF * 1 + START_OCTAVE * 12 + 8, 0},
      {MidiParser::BUTTON_ROW3_COL1,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 1, 0},
      {MidiParser::BUTTON_ROW3_COL2,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 2, 0},
      {MidiParser::BUTTON_ROW3_COL3,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 3, 0},
      {MidiParser::BUTTON_ROW3_COL4,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 4, 0},
      {MidiParser::BUTTON_ROW3_COL5,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 5, 0},
      {MidiParser::BUTTON_ROW3_COL6,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 6, 0},
      {MidiParser::BUTTON_ROW3_COL7,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 7, 0},
      {MidiParser::BUTTON_ROW3_COL8,
       NOTE_BASE_G - NOTE_STRING_DIFF * 2 + START_OCTAVE * 12 + 8, 0},
      {MidiParser::BUTTON_ROW4_COL1,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 1, 0},
      {MidiParser::BUTTON_ROW4_COL2,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 2, 0},
      {MidiParser::BUTTON_ROW4_COL3,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 3, 0},
      {MidiParser::BUTTON_ROW4_COL4,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 4, 0},
      {MidiParser::BUTTON_ROW4_COL5,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 5, 0},
      {MidiParser::BUTTON_ROW4_COL6,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 6, 0},
      {MidiParser::BUTTON_ROW4_COL7,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 7, 0},
      {MidiParser::BUTTON_ROW4_COL8,
       NOTE_BASE_G - NOTE_STRING_DIFF * 3 + START_OCTAVE * 12 + 8, 0}};
  enum Colors {
    OFF = 0,
    GREEN = 1,
    RED = 4,
    YELLOW = 8,
    BLUE = 16,
    CYAN = 32,
    MAGENTA = 64,
    WHITE = 127
  };
  uint8_t _velocity = 100;
  int _midiOffsetHorizontal = 0;
  int _midiOffsetVertical = 0;

  static Keyboard *_instance;
  Keyboard();

public:
  static Keyboard *getInstance();
  uint8_t getVelocity();
  void setVelocity(uint8_t velocity);
  int getMidiOffset();
  void setMidiOffsetVertical(int value);
  void setMidiOffsetHorizontal(int value);
  void resetMidiOffset();
  void setColorsForMusicTones();
  void setColorsForMidiOffset();
  void setColors();
  void setMidiState(uint8_t midiNote, bool state);
};

#endif
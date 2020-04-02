#ifndef __MIDI_PARSER_HPP__
#define __MIDI_PARSER_HPP__

#include <iostream>
#include <vector>

class MidiParser {
public:
  enum TweakerStatusByteEnum { NOTE_ON = 144, CONTROL_CHANGE = 176, NOTE_ON_C16 = 159 };

  enum TweakerNoteOnEnum {
    BUTTON_ROW1_COL1 = 1,
    BUTTON_ROW1_COL2 = 2,
    BUTTON_ROW1_COL3 = 3,
    BUTTON_ROW1_COL4 = 4,
    BUTTON_ROW1_COL5 = 5,
    BUTTON_ROW1_COL6 = 6,
    BUTTON_ROW1_COL7 = 7,
    BUTTON_ROW1_COL8 = 8,
    BUTTON_ROW2_COL1 = 9,
    BUTTON_ROW2_COL2 = 10,
    BUTTON_ROW2_COL3 = 11,
    BUTTON_ROW2_COL4 = 12,
    BUTTON_ROW2_COL5 = 13,
    BUTTON_ROW2_COL6 = 14,
    BUTTON_ROW2_COL7 = 15,
    BUTTON_ROW2_COL8 = 16,
    BUTTON_ROW3_COL1 = 17,
    BUTTON_ROW3_COL2 = 18,
    BUTTON_ROW3_COL3 = 19,
    BUTTON_ROW3_COL4 = 20,
    BUTTON_ROW3_COL5 = 21,
    BUTTON_ROW3_COL6 = 22,
    BUTTON_ROW3_COL7 = 23,
    BUTTON_ROW3_COL8 = 24,
    BUTTON_ROW4_COL1 = 25,
    BUTTON_ROW4_COL2 = 26,
    BUTTON_ROW4_COL3 = 27,
    BUTTON_ROW4_COL4 = 28,
    BUTTON_ROW4_COL5 = 29,
    BUTTON_ROW4_COL6 = 30,
    BUTTON_ROW4_COL7 = 31,
    BUTTON_ROW4_COL8 = 32,
    BUTTON_GRID_NAVIGATION_UP = 39,
    BUTTON_GRID_NAVIGATION_DOWN = 41,
    BUTTON_GRID_NAVIGATION_LEFT = 42,
    BUTTON_GRID_NAVIGATION_RIGHT = 43,
    BUTTON_GRID_NAVIGATION_CENTER = 40,
    BUTTON_AB_ASSIGN_LEFT = 35,
    BUTTON_AB_ASSIGN_RIGHT = 38,
    BUTTON_SOLO_LEFT = 33,
    BUTTON_SOLO_RIGHT = 36,
    BUTTON_RECORD_ARM_LEFT = 34,
    BUTTON_RECORD_ARM_RIGHT = 37,
    BUTTON_PAD_ROW1_COL1 = 63,
    BUTTON_PAD_ROW1_COL2 = 64,
    BUTTON_PAD_ROW1_COL3 = 65,
    BUTTON_PAD_ROW1_COL4 = 66,
    BUTTON_PAD_ROW2_COL1 = 67,
    BUTTON_PAD_ROW2_COL2 = 68,
    BUTTON_PAD_ROW2_COL3 = 69,
    BUTTON_PAD_ROW2_COL4 = 70,
    BUTTON_SLIDER_LEFT = 53,
    BUTTON_SLIDER_RIGHT = 54,
    BUTTON_ENCODER_HIGH_LEFT = 45,
    BUTTON_ENCODER_MID_LEFT = 46,
    BUTTON_ENCODER_LOW_LEFT = 47,
    BUTTON_ENCODER_HIGH_RIGHT = 48,
    BUTTON_ENCODER_MID_RIGHT = 49,
    BUTTON_ENCODER_LOW_RIGHT = 50,
    BUTTON_POT_LEFT = 51,
    BUTTON_POT_RIGHT = 52,
    BUTTON_TRACK_SELECT = 44
  };

  enum TweakerControlChangeEnum {
    PAD_ROW1_COL1 = 71,
    PAD_ROW1_COL2 = 72,
    PAD_ROW1_COL3 = 73,
    PAD_ROW1_COL4 = 74,
    PAD_ROW2_COL1 = 75,
    PAD_ROW2_COL2 = 76,
    PAD_ROW2_COL3 = 77,
    PAD_ROW2_COL4 = 78,
    SLIDER_LEFT = 53,
    SLIDER_RIGHT = 54,
    SLIDER_CENTER = 55,
    ENCODER_HIGH_LEFT = 57,
    ENCODER_MID_LEFT = 58,
    ENCODER_LOW_LEFT = 59,
    ENCODER_HIGH_RIGHT = 60,
    ENCODER_MID_RIGHT = 61,
    ENCODER_LOW_RIGHT = 62,
    POT_LEFT = 51,
    POT_RIGHT = 52,
    TRACK_SELECT = 56
  };

private:
  static MidiParser *_instance;
  MidiParser();

public:
  static MidiParser *getInstance();
  void parse(double deltatime, std::vector<unsigned char> *message,
             void *userData);
  static void staticParse(double deltatime, std::vector<unsigned char> *message,
                          void *userData) {
    getInstance()->parse(deltatime, message, userData);
  }
  void printData(double deltatime, std::vector<unsigned char> *message,
                 void *userData);
  void parseNoteOn(uint8_t byte1, uint8_t byte2);
  void parseControlChange(uint8_t byte1, uint8_t byte2);
};

#endif

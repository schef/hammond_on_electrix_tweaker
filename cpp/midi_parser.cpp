#include "stdio.h"

#include "keyboard.hpp"
#include "midi_parser.hpp"
#include "midi_player.hpp"

#define FILE_NAME "midi_parser: "

MidiParser *MidiParser::_instance = nullptr;

MidiParser *MidiParser::getInstance() {
  if (_instance == nullptr) {
    _instance = new MidiParser();
  }
  return _instance;
}

MidiParser::MidiParser() { printf(FILE_NAME "constructor\n"); }

void MidiParser::printData(double deltatime,
                           std::vector<unsigned char> *message,
                           void *userData) {
  unsigned int nBytes = message->size();
  printf(FILE_NAME "printData [ ");
  for (unsigned int i = 0; i < nBytes; i++) {
    printf("%d ", message->at(i));
  }
  printf("] stamp = %f\n", deltatime);
}

void MidiParser::parse(double deltatime, std::vector<unsigned char> *message,
                       void *userData) {
  printData(deltatime, message, userData);

  switch (message->at(0)) {
  case NOTE_ON:
    printf(FILE_NAME "NOTE_ON\n");
    parseNoteOn(message->at(1), message->at(2));
    break;

  case CONTROL_CHANGE:
    printf(FILE_NAME "CONTROL_CHANGE\n");
    parseControlChange(message->at(1), message->at(2));
    break;

  default:
    break;
  }
}

void MidiParser::parseNoteOn(uint8_t byte1, uint8_t byte2) {
  switch (byte1) {
  case BUTTON_ROW1_COL1:
    printf("BUTTON_ROW1_COL1 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW1_COL2:
    printf("BUTTON_ROW1_COL2 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW1_COL3:
    printf("BUTTON_ROW1_COL3 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW1_COL4:
    printf("BUTTON_ROW1_COL4 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW1_COL5:
    printf("BUTTON_ROW1_COL5 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW1_COL6:
    printf("BUTTON_ROW1_COL6 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW1_COL7:
    printf("BUTTON_ROW1_COL7 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW1_COL8:
    printf("BUTTON_ROW1_COL8 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL1:
    printf("BUTTON_ROW2_COL1 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL2:
    printf("BUTTON_ROW2_COL2 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL3:
    printf("BUTTON_ROW2_COL3 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL4:
    printf("BUTTON_ROW2_COL4 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL5:
    printf("BUTTON_ROW2_COL5 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL6:
    printf("BUTTON_ROW2_COL6 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL7:
    printf("BUTTON_ROW2_COL7 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW2_COL8:
    printf("BUTTON_ROW2_COL8 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL1:
    printf("BUTTON_ROW3_COL1 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL2:
    printf("BUTTON_ROW3_COL2 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL3:
    printf("BUTTON_ROW3_COL3 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL4:
    printf("BUTTON_ROW3_COL4 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL5:
    printf("BUTTON_ROW3_COL5 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL6:
    printf("BUTTON_ROW3_COL6 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL7:
    printf("BUTTON_ROW3_COL7 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW3_COL8:
    printf("BUTTON_ROW3_COL8 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL1:
    printf("BUTTON_ROW4_COL1 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL2:
    printf("BUTTON_ROW4_COL2 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL3:
    printf("BUTTON_ROW4_COL3 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL4:
    printf("BUTTON_ROW4_COL4 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL5:
    printf("BUTTON_ROW4_COL5 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL6:
    printf("BUTTON_ROW4_COL6 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL7:
    printf("BUTTON_ROW4_COL7 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_ROW4_COL8:
    printf("BUTTON_ROW4_COL8 %d\n", byte2);
    Keyboard::getInstance()->setMidiState(byte1, byte2);
    break;

  case BUTTON_GRID_NAVIGATION_UP:
    printf("BUTTON_GRID_NAVIGATION_UP %d\n", byte2);
    if (byte2) {
      Keyboard::getInstance()->setMidiOffsetVertical(-5);
    }
    break;

  case BUTTON_GRID_NAVIGATION_DOWN:
    printf("BUTTON_GRID_NAVIGATION_DOWN %d\n", byte2);
    if (byte2) {
      Keyboard::getInstance()->setMidiOffsetVertical(5);
    }
    break;

  case BUTTON_GRID_NAVIGATION_LEFT:
    printf("BUTTON_GRID_NAVIGATION_LEFT %d\n", byte2);
    if (byte2) {
      Keyboard::getInstance()->setMidiOffsetHorizontal(1);
    }
    break;

  case BUTTON_GRID_NAVIGATION_RIGHT:
    printf("BUTTON_GRID_NAVIGATION_RIGHT %d\n", byte2);
    if (byte2) {
      Keyboard::getInstance()->setMidiOffsetHorizontal(-1);
    }
    break;

  case BUTTON_GRID_NAVIGATION_CENTER:
    printf("BUTTON_GRID_NAVIGATION_CENTER %d\n", byte2);
    if (byte2) {
      Keyboard::getInstance()->resetMidiOffset();
    }
    break;

  case BUTTON_AB_ASSIGN_LEFT:
    printf("BUTTON_AB_ASSIGN_LEFT %d\n", byte2);
    break;

  case BUTTON_AB_ASSIGN_RIGHT:
    printf("BUTTON_AB_ASSIGN_RIGHT %d\n", byte2);
    break;

  case BUTTON_SOLO_LEFT:
    printf("BUTTON_SOLO_LEFT %d\n", byte2);
    break;

  case BUTTON_SOLO_RIGHT:
    printf("BUTTON_SOLO_RIGHT %d\n", byte2);
    break;

  case BUTTON_RECORD_ARM_LEFT:
    printf("BUTTON_RECORD_ARM_LEFT %d\n", byte2);
    break;

  case BUTTON_RECORD_ARM_RIGHT:
    printf("BUTTON_RECORD_ARM_RIGHT %d\n", byte2);
    break;

  case BUTTON_PAD_ROW1_COL1:
    printf("BUTTON_PAD_ROW1_COL1 %d\n", byte2);
    break;

  case BUTTON_PAD_ROW1_COL2:
    printf("BUTTON_PAD_ROW1_COL2 %d\n", byte2);
    break;

  case BUTTON_PAD_ROW1_COL3:
    printf("BUTTON_PAD_ROW1_COL3 %d\n", byte2);
    break;

  case BUTTON_PAD_ROW1_COL4:
    printf("BUTTON_PAD_ROW1_COL4 %d\n", byte2);
    break;

  case BUTTON_PAD_ROW2_COL1:
    printf("BUTTON_PAD_ROW2_COL1 %d\n", byte2);
    break;

  case BUTTON_PAD_ROW2_COL2:
    printf("BUTTON_PAD_ROW2_COL2 %d\n", byte2);
    break;

  case BUTTON_PAD_ROW2_COL3:
    printf("BUTTON_PAD_ROW2_COL3 %d\n", byte2);
    break;

  case BUTTON_PAD_ROW2_COL4:
    printf("BUTTON_PAD_ROW2_COL4 %d\n", byte2);
    break;

  case BUTTON_SLIDER_LEFT:
    printf("BUTTON_SLIDER_LEFT %d\n", byte2);

  case BUTTON_SLIDER_RIGHT:
    printf("BUTTON_SLIDER_RIGHT %d\n", byte2);
    break;

  case BUTTON_ENCODER_HIGH_LEFT:
    printf("BUTTON_ENCODER_HIGH_LEFT %d\n", byte2);
    break;

  case BUTTON_ENCODER_MID_LEFT:
    printf("BUTTON_ENCODER_MID_LEFT %d\n", byte2);
    break;

  case BUTTON_ENCODER_LOW_LEFT:
    printf("BUTTON_ENCODER_LOW_LEFT %d\n", byte2);
    break;

  case BUTTON_ENCODER_HIGH_RIGHT:
    printf("BUTTON_ENCODER_HIGH_RIGHT %d\n", byte2);
    break;

  case BUTTON_ENCODER_MID_RIGHT:
    printf("BUTTON_ENCODER_MID_RIGHT %d\n", byte2);
    break;

  case BUTTON_ENCODER_LOW_RIGHT:
    printf("BUTTON_ENCODER_LOW_RIGHT %d\n", byte2);
    break;

  case BUTTON_POT_LEFT:
    printf("BUTTON_POT_LEFT %d\n", byte2);
    break;

  case BUTTON_POT_RIGHT:
    printf("BUTTON_POT_RIGHT %d\n", byte2);
    break;

  case BUTTON_TRACK_SELECT:
    printf("BUTTON_TRACK_SELECT %d\n", byte2);
    break;

  default:
    break;
  }
}

void MidiParser::parseControlChange(uint8_t byte1, uint8_t byte2) {
  switch (byte1) {
  case PAD_ROW1_COL1:
    printf(FILE_NAME "PAD_ROW1_COL1 %d\n", byte2);
    break;

  case PAD_ROW1_COL2:
    printf(FILE_NAME "PAD_ROW1_COL2 %d\n", byte2);
    break;

  case PAD_ROW1_COL3:
    printf(FILE_NAME "PAD_ROW1_COL3 %d\n", byte2);
    break;

  case PAD_ROW1_COL4:
    printf(FILE_NAME "PAD_ROW1_COL4 %d\n", byte2);
    break;

  case PAD_ROW2_COL1:
    printf(FILE_NAME "PAD_ROW2_COL1 %d\n", byte2);
    break;

  case PAD_ROW2_COL2:
    printf(FILE_NAME "PAD_ROW2_COL2 %d\n", byte2);
    break;

  case PAD_ROW2_COL3:
    printf(FILE_NAME "PAD_ROW2_COL3 %d\n", byte2);
    break;

  case PAD_ROW2_COL4:
    printf(FILE_NAME "PAD_ROW2_COL4 %d\n", byte2);
    break;

  case SLIDER_LEFT: {
    printf(FILE_NAME "SLIDER_LEFT %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 11, byte2);
  } break;

  case SLIDER_RIGHT:
    printf(FILE_NAME "SLIDER_RIGHT %d\n", byte2);
    break;

  case SLIDER_CENTER: {
    printf(FILE_NAME "SLIDER_CENTER %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 1, byte2);
  } break;

  case ENCODER_HIGH_LEFT:
    printf(FILE_NAME "ENCODER_HIGH_LEFT %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 103, 127 - byte2);
    break;

  case ENCODER_MID_LEFT:
    printf(FILE_NAME "ENCODER_MID_LEFT %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 102, 127 - byte2);
    break;

  case ENCODER_LOW_LEFT:
    printf(FILE_NAME "ENCODER_LOW_LEFT %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 101, 127 - byte2);
    break;

  case ENCODER_HIGH_RIGHT:
    printf(FILE_NAME "ENCODER_HIGH_RIGHT %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 104, 127 - byte2);
    break;

  case ENCODER_MID_RIGHT:
    printf(FILE_NAME "ENCODER_MID_RIGHT %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 105, 127 - byte2);
    break;

  case ENCODER_LOW_RIGHT:
    printf(FILE_NAME "ENCODER_LOW_RIGHT %d\n", byte2);
    MidiPlayer::getInstance()->sendMessageOut(MidiParser::CONTROL_CHANGE, 106, 127 - byte2);
    break;

  case POT_LEFT:
    printf(FILE_NAME "POT_LEFT %d\n", byte2);
    Keyboard::getInstance()->setVelocity(byte2);
    break;

  case POT_RIGHT:
    printf(FILE_NAME "POT_RIGHT %d\n", byte2);
    break;

  case TRACK_SELECT:
    printf(FILE_NAME "TRACK_SELECT %d\n", byte2);
    break;

  default:
    break;
  }
}
#include <chrono>
#include <stdlib.h>
#include <thread>

#include "midi_parser.hpp"
#include "midi_player.hpp"

#define FILE_NAME "main: "

int main() {
  printf(FILE_NAME "Boot sequence start\n");

  MidiPlayer::getInstance()->registerCallbackFunction(MidiParser::staticParse);

  printf(FILE_NAME "Boot sequence end\n");

  printf(FILE_NAME "Press any key to exit.\n");

  // const std::vector<unsigned char> noteOn = {0x90, 0x30, 0x64};
  // const std::vector<unsigned char> noteOff = {0x80, 0x30, 0x00};

  // while (true)
  // {
  // MidiPlayer::getInstance()->sendMessageOutTweaker(&noteOn);
  // std::this_thread::sleep_for(std::chrono::milliseconds(500));
  // MidiPlayer::getInstance()->sendMessageOutTweaker(&noteOff);
  // std::this_thread::sleep_for(std::chrono::milliseconds(500));
  // }

  getchar();
  return 0;
}
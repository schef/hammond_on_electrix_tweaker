#include <chrono>
#include <stdlib.h>
#include <thread>
#include <chrono>

using namespace std;

#include "midi_parser.hpp"
#include "midi_player.hpp"

#define FILE_NAME "main: "

int main() {
  printf(FILE_NAME "Boot sequence start\n");

  MidiPlayer::getInstance()->registerCallbackFunction(MidiParser::staticParse);

  printf(FILE_NAME "Boot sequence end\n");

  printf(FILE_NAME "Press any key to exit.\n");

  auto start = chrono::steady_clock::now();
  uint32_t keepAlive = 0;

  // while (true)
  // {
  // MidiPlayer::getInstance()->sendMessageOutTweaker(0x90, 0x30, 0x64);
  // std::this_thread::sleep_for(std::chrono::milliseconds(500));
  // MidiPlayer::getInstance()->sendMessageOutTweaker(0x80, 0x30, 0x00);
  // std::this_thread::sleep_for(std::chrono::milliseconds(500));
  // }

  //getchar();
  
  while(true){
    if (chrono::duration_cast<chrono::seconds>(chrono::steady_clock::now() - start).count() >= 5) {
      start = chrono::steady_clock::now();
      printf("keepAlive: %d\n", keepAlive);
      keepAlive++;
    }
  }
  return 0;
}

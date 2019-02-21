#include "RtMidi.h"
#include <cstdlib>
#include <iostream>
#include <string.h>

void usage(void) {
  // Error function in case of incorrect command-line
  // argument specifications.
  std::cout << "\nuseage: cmidiin <port>\n";
  std::cout << "    where port = the device to use (default = 0).\n\n";
  exit(0);
}

void mycallback(double deltatime, std::vector<unsigned char> *message,
                void * /*userData*/) {
  unsigned int nBytes = message->size();
  for (unsigned int i = 0; i < nBytes; i++)
    std::cout << "Byte " << i << " = " << (int)message->at(i) << ", ";
  if (nBytes > 0)
    std::cout << "stamp = " << deltatime << std::endl;
}

// This function should be embedded in a try/catch block in case of
// an exception.  It offers the user a choice of MIDI ports to open.
// It returns false if there are no ports available.
bool chooseMidiPort(RtMidiIn *rtmidi);

int main() {
  printf("Boot sequence start\n");

  RtMidiIn *midiin = nullptr;

  try {

    midiin = new RtMidiIn();

    // Call function to select port.
    if (chooseMidiPort(midiin) == false)
      goto cleanup;

    // Set our callback function.  This should be done immediately after
    // opening the port to avoid having incoming messages written to the
    // queue instead of sent to the callback function.
    midiin->setCallback(&mycallback);

    // Don't ignore sysex, timing, or active sensing messages.
    midiin->ignoreTypes(false, false, false);

    std::cout << "\nReading MIDI input ... press <enter> to quit.\n";
    char input;
    std::cin.get(input);

  } catch (RtMidiError &error) {
    error.printMessage();
  }

cleanup:

  delete midiin;

  return 0;
}

bool chooseMidiPort(RtMidiIn *rtmidi) {
  std::string portName;
  unsigned int nPorts = rtmidi->getPortCount();
  char searchName[] = "Tweaker:Tweaker MIDI 1 20:0";
  for (unsigned int i = 0; i < nPorts; i++) {
    portName = rtmidi->getPortName(i);
    if (strcmp(searchName, portName.c_str()) == 0){
      rtmidi->openPort(i);
      printf("Found tweaker on port %d\n", i);
      return true;
    };
  }

  return false;
}

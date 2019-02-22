#include <string.h>

#include "midi_player.hpp"

#define FILE_NAME "midi_player: "

#define TWEAKER_SEARCH_NAME "Tweaker:Tweaker"
#define VMPK_SEARCH_NAME "VMPK"
#define INVALID_SEARCH_NAME "INVALID"

#define MIDI_NAME "tweaker"
#define MIDI_IN_TWEAKER_PORT_NAME "fromTweaker"
#define MIDI_OUT_TWEAKER_PORT_NAME "toTweaker"
#define MIDI_OUT_PORT_NAME "output"

MidiPlayer *MidiPlayer::_instance = nullptr;

MidiPlayer *MidiPlayer::getInstance() {
  if (_instance == nullptr) {
    _instance = new MidiPlayer();
  }
  return _instance;
}

MidiPlayer::MidiPlayer() {
  printf(FILE_NAME "constructor\n");
  init();
}

void MidiPlayer::init() {
  try {
    _midiInTweaker = new RtMidiIn(RtMidiIn::Api::UNSPECIFIED, MIDI_NAME, 100);
    chooseMidiInPort(_midiInTweaker, (char *)TWEAKER_SEARCH_NAME,
                     (char *)MIDI_IN_TWEAKER_PORT_NAME);
    _midiInTweaker->setCallback(staticCallbackFunction);
    _midiInTweaker->ignoreTypes(false, false, false);

    _midiOutTweaker = new RtMidiOut(RtMidiIn::Api::UNSPECIFIED, MIDI_NAME);
    chooseMidiOutPort(_midiOutTweaker, (char *)TWEAKER_SEARCH_NAME,
                      (char *)MIDI_OUT_TWEAKER_PORT_NAME);

    _midiOut = new RtMidiOut(RtMidiIn::Api::UNSPECIFIED, MIDI_NAME);
    chooseMidiOutPort(_midiOut, (char *)INVALID_SEARCH_NAME,
                      (char *)MIDI_OUT_PORT_NAME);
  } catch (RtMidiError &error) {
    error.printMessage();
    delete _midiInTweaker;
  }
}

void MidiPlayer::chooseMidiInPort(RtMidiIn *rtmidi, char *searchName,
                                  char *portName) {
  printf(FILE_NAME "chooseMidiInPort\n");
  std::string existingPort;
  unsigned int nPorts = rtmidi->getPortCount();
  printf(FILE_NAME "searchName: %s\n", searchName);
  for (unsigned int i = 0; i < nPorts; i++) {
    existingPort = rtmidi->getPortName(i);
    printf(FILE_NAME "existingPort: %s\n", existingPort.c_str());
    if (memcmp(searchName, existingPort.c_str(), strlen(searchName) - 1) == 0) {
      rtmidi->openPort(i, portName);
      printf(FILE_NAME "midiInPort found\n");
      return;
    };
  }

  rtmidi->openVirtualPort(portName);
  printf(FILE_NAME "midiInPort not found, opening virtual port for testing.\n");
}

void MidiPlayer::chooseMidiOutPort(RtMidiOut *rtmidi, char *searchName,
                                   char *portName) {
  printf(FILE_NAME "chooseMidiOutPort\n");
  std::string existingPort;
  unsigned int nPorts = rtmidi->getPortCount();
  printf(FILE_NAME "searchName: %s\n", searchName);
  for (unsigned int i = 0; i < nPorts; i++) {
    existingPort = rtmidi->getPortName(i);
    printf(FILE_NAME "existingPort: %s\n", existingPort.c_str());
    if (memcmp(searchName, existingPort.c_str(), strlen(searchName) - 1) == 0) {
      rtmidi->openPort(i, portName);
      printf(FILE_NAME "midiOutPort found\n");
      return;
    };
  }

  rtmidi->openVirtualPort(portName);
  printf(FILE_NAME
         "midiOutPort not found, opening virtual port for testing.\n");
}

void MidiPlayer::registerCallbackFunction(void (*callbackFunction)(
    double deltatime, std::vector<unsigned char> *message, void *)) {
  printf(FILE_NAME "registerCallbackFunction\n");
  _callbackFunction = callbackFunction;
}

void MidiPlayer::callbackFunction(double deltatime,
                                  std::vector<unsigned char> *message,
                                  void *userData) {
  if (_callbackFunction) {
    _callbackFunction(deltatime, message, userData);
  }
}

void MidiPlayer::staticCallbackFunction(double deltatime,
                                        std::vector<unsigned char> *message,
                                        void *userData) {
  getInstance()->callbackFunction(deltatime, message, userData);
}

void MidiPlayer::sendMessageOutTweaker(
    const std::vector<unsigned char> *message) {
  if (_midiOutTweaker) {
    _midiOutTweaker->sendMessage(message);
  }
}

void MidiPlayer::sendMessageOut(const std::vector<unsigned char> *message) {
  if (_midiOut) {
    _midiOut->sendMessage(message);
  }
}
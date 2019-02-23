#ifndef __MIDI_PLAYER_HPP__
#define __MIDI_PLAYER_HPP__

#include "RtMidi.h"

class MidiPlayer
{
  private:
    void (*_callbackFunction)(double deltatime, std::vector<unsigned char> *message, void *userData) = nullptr;
    RtMidiIn *_midiInTweaker = nullptr;
    RtMidiOut *_midiOutTweaker = nullptr;
    RtMidiOut *_midiOut = nullptr;
    static MidiPlayer *_instance;
    MidiPlayer();
    void init();
    void chooseMidiInPort(RtMidiIn *rtmidi, char *searchName, char *portName);
    void chooseMidiOutPort(RtMidiOut *rtmidi, char *searchName, char *portName);
    void callbackFunction(double deltatime, std::vector<unsigned char> *message, void *userData);
    static void staticCallbackFunction(double deltatime, std::vector<unsigned char> *message, void *userData);

  public:
    static MidiPlayer *getInstance();
    void registerCallbackFunction(void (*callbackFunction)(double deltatime, std::vector<unsigned char> *message, void *));
    void sendMessageOutTweaker(const std::vector<unsigned char> *message);
    void sendMessageOutTweaker(uint8_t byte1, uint8_t byte2, uint8_t byte3);
    void sendMessageOut(const std::vector<unsigned char> *message);
    void sendMessageOut(uint8_t byte1, uint8_t byte2, uint8_t byte3);
};

#endif

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
			MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::RED);
		} else if (midiStateHolder[i].wantedMidi + getMidiOffset() == 60 + 12) {
			MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON,midiStateHolder[i].originalMidi,Colors::MAGENTA);
		} else if (midiStateHolder[i].wantedMidi + getMidiOffset() == 60 + 12 + 12) {
			MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::YELLOW);
		} else if (midiStateHolder[i].wantedMidi + getMidiOffset() == 60 - 12) {
			MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::GREEN);
		} else if (midiStateHolder[i].wantedMidi + getMidiOffset() == 60 - 12 - 12) {
			MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::BLUE);
		} else if (midiStateHolder[i].wantedMidi + getMidiOffset() > 127 or midiStateHolder[i].wantedMidi + getMidiOffset() < 0) {
			MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::CYAN);
		} else {
			MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, midiStateHolder[i].originalMidi, Colors::OFF);
		}
	}
}

void Keyboard::setColorsForMidiOffset() {
	if (getMidiOffset()) {
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_CENTER, Colors::OFF);
	} else {
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_CENTER, Colors::WHITE);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_UP, Colors::OFF);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON,MidiParser::BUTTON_GRID_NAVIGATION_DOWN,Colors::OFF);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON,MidiParser::BUTTON_GRID_NAVIGATION_LEFT, Colors::OFF);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_RIGHT,Colors::OFF);
	}

	if (_midiOffsetVertical > 0) {
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON,MidiParser::BUTTON_GRID_NAVIGATION_UP,Colors::OFF);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON,MidiParser::BUTTON_GRID_NAVIGATION_DOWN,Colors::WHITE);
	} else if (_midiOffsetVertical < 0) {
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON,MidiParser::BUTTON_GRID_NAVIGATION_UP,Colors::WHITE);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON,MidiParser::BUTTON_GRID_NAVIGATION_DOWN,Colors::OFF);
	}

	if (_midiOffsetHorizontal > 0) {
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_LEFT, Colors::WHITE);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_RIGHT, Colors::OFF);
	} else if (_midiOffsetHorizontal < 0) {
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_LEFT,Colors::OFF);
		MidiPlayer::getInstance()->sendMessageOutTweaker(MidiParser::NOTE_ON, MidiParser::BUTTON_GRID_NAVIGATION_RIGHT,Colors::WHITE);
	}
}

void Keyboard::setColors() {
	setColorsForMusicTones();
	setColorsForMidiOffset();
}

void Keyboard::setMidiState(uint8_t midiNote, bool state) {
	uint8_t midiNoteWithOffset;
	for (uint8_t i = 0; i < sizeof(midiStateHolder) / sizeof(MidiStateHolder); i++) {
		if (midiStateHolder[i].originalMidi == midiNote) {
			midiNoteWithOffset = midiStateHolder[i].wantedMidi + getMidiOffset();
			break;
		}
	}
	MidiPlayer::getInstance()->sendMessageOut(MidiParser::NOTE_ON, midiNoteWithOffset, state ? _velocity : 0);
}

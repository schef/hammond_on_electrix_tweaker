#!/bin/bash

jack_disconnect "ZynMidiRouter:main_in" "a2j:Tweaker [20] (capture): Tweaker MIDI 1"
jack_disconnect "ZynMidiRouter:main_in" "a2j:Tweaker [20] (capture): Tweaker MIDI 2"
jack_disconnect "ZynMidiRouter:main_in" "a2j:Midi Through [14] (capture): Midi Through Port-0"
jack_disconnect "a2j:Midi Through [14] (capture): Midi Through Port-0" "ZynMidiRouter:main_in"
jack_disconnect "a2j:Tweaker [20] (capture): Tweaker MIDI 1" "ZynMidiRouter:main_in"
jack_disconnect "a2j:Tweaker [20] (capture): Tweaker MIDI 2" "ZynMidiRouter:main_in"
aconnect 129 20
aconnect 20 128
jack_connect "a2j:tweaker [130] (capture): output" "ZynMidiRouter:main_in"
jack_connect "a2j:tweaker [129] (capture): output" "ZynMidiRouter:main_in"
jack_connect "a2j:tweaker [128] (capture): output" "ZynMidiRouter:main_in"

exit 0

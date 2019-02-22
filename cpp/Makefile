default: build run

SOURCE_FILE += main.cpp
SOURCE_FILE += midi_player.cpp
SOURCE_FILE += midi_parser.cpp
SOURCE_FILE += keyboard.cpp

INCLUDE_PATH += -I./
INCLUDE_PATH += -I/usr/include/rtmidi/

build:
	g++ -std=c++17 $(SOURCE_FILE) $(INCLUDE_PATH) `pkg-config --cflags --libs rtmidi` -g -O2 -o main

run:
	./main

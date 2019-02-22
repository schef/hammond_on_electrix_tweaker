default: build run

build:

	g++ -std=c++17 main.cpp midi_player.cpp -I./ -I/usr/include/rtmidi/ `pkg-config --cflags --libs rtmidi` -g -O2 -o main

run:
	./main

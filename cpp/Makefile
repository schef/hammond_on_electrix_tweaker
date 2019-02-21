default: build run

build:

	g++ main.cpp -I/usr/include/rtmidi/ `pkg-config --cflags --libs rtmidi` -g -O2 -o main

run:
	./main
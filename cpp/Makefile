CC=g++
CFLAGS=-Iinclude -std=c++11 -Wall
LIBS=-lcurl

default: main

main: Core.o Utils.o
	$(CC) $(CFLAGS) $(LIBS) -o main Core.o Utils.o main.cpp

Core.o: Core.cpp
	$(CC) $(CFLAGS) $(LIBS) -c Core.cpp

Utils.o: Utils.cpp
	$(CC) $(CFLAGS) $(LIBS) -c Utils.cpp

clean:
	rm main *.o
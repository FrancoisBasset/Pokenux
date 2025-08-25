WARNINGS = -Wall -Wextra -Wshadow -Wconversion -pedantic

CFLAGS = $(shell pkg-config --cflags gtk4)
LIBS = $(shell pkg-config --libs gtk4)

SRC = main.c

all: clean main

resources.c:
	glib-compile-resources resources.xml --generate-source

main: $(SRC)
	gcc $(WARNINGS) -O2 $(CFLAGS) $(SRC) -o main $(LIBS) -Wl,--export-dynamic

clean:
	rm -rf main .cache resources.c

bear:
	bear -- make
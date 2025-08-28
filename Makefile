WARNINGS = -Wall -Wextra -Wshadow -Wconversion -pedantic

CFLAGS = $(shell pkg-config --cflags gtk4 libcurl)
LIBS = $(shell pkg-config --libs gtk4 libcurl)

SRC = main.c api/tcgdex.c api/curl.c api/cJSON.c

all: clean pokenux

resources.c:
	glib-compile-resources resources.xml --generate-source

pokenux: $(SRC)
	gcc $(WARNINGS) -O2 $(CFLAGS) $(SRC) -o pokenux $(LIBS) -Wl,--export-dynamic

clean:
	rm -rf pokenux .cache resources.c

check:
	cppcheck --language=c --enable=all --template=gcc --suppress=missingIncludeSystem .

bear:
	bear -- make

vg:
	valgrind --leak-check=full --show-leak-kinds=all ./pokenux
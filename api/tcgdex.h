#ifndef TCGDEX_H
#define TCGDEX_H

#include "../core/serie.h"

extern char* tcgdex_language;

void tcgdex_set_language(char* language);
Serie* tcgdex_get_series(int* length);

#endif
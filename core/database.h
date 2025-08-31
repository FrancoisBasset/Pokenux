#ifndef DATABASE_H
#define DATABASE_H
#include "serie.h"
#include "extension.h"

extern char* database_language;

void database_init(void);
void database_open(void);
void database_close(void);

void database_set_language(char* language);
void database_tcgdex_populate(char* language);

#endif
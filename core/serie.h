#ifndef SERIE_H
#define SERIE_H

#include "extension.h"

typedef char* link;

typedef struct {
    char* id;
    char* name;
    link logo;
    link release_date;
    Extension* extensions;
    int extensions_length;
} Serie;

void serie_free(Serie serie);

#endif
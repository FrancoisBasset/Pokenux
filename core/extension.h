#ifndef EXTENSION_H
#define EXTENSION_H

#include "card.h"

typedef char* link;

typedef struct {
    char* id;
    char* name;
    link logo;
    link symbol;
    int count_official;
    int count_total;
    char* release_date;
    Card* cards;
    char* abbreviation;
} Extension;

#endif
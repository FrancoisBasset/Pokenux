#ifndef CARD_H
#define CARD_H

typedef struct {
    char* id;
    char* image;
    char* name;
    char* category;
    char* rarity;
    char* index;
    char* illustrator;
    char* regulation_mark;
    int hp;
    char* description;
} Card;

#endif
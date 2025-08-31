#include "core/database.h"

int main() {
    database_init();

    database_open();
    database_tcgdex_populate("fr");
    database_close();

    return 0;
}
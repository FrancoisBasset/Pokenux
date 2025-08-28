#include <stdio.h>
#include <stdlib.h>
#include "api/tcgdex.h"
#include "core/serie.h"

void serie_free(Serie serie) {
    free(serie.id);
    free(serie.name);
    free(serie.logo);
    free(serie.release_date);
    free(serie.extensions);
}

int main() {
    tcgdex_set_language("fr");

    int series_length;
    Serie* series = tcgdex_get_series(&series_length);

    for (int i = 0; i < series_length; i++) {
        printf("%s %s %s %s\n", series[i].id, series[i].name, series[i].logo, series[i].release_date);
        serie_free(series[i]);
    }

    free(series);

    return 0;
}
#include <stdlib.h>
#include "serie.h"

void serie_free(Serie serie) {
    free(serie.id);
    free(serie.name);
    free(serie.logo);
    free(serie.release_date);
    free(serie.extensions);
}
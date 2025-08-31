#include <stdlib.h>
#include "extension.h"

void extension_free(Extension extension) {
    free(extension.id);
    free(extension.name);
    free(extension.logo);
    free(extension.symbol);
    free(extension.release_date);
    free(extension.abbreviation);
}
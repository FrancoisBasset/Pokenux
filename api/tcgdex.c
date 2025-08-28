#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tcgdex.h"
#include "cJSON.h"
#include "curl.h"

char* tcgdex_language;

static char* tcgdex_get_language() {
    if (tcgdex_language == NULL) {
        return "en";
    }

    return tcgdex_language;
}

void tcgdex_set_language(char *language) {
    tcgdex_language = language;
}

static char* get_url() {
    char* url = calloc(100, sizeof(char));

    sprintf(url, "https://api.tcgdex.net/v2/%s/", tcgdex_get_language());
    
    return url;
}

static char* get_series_url() {
    char* url = get_url();
    strcat(url, "series");

    return url;
}

static char* get_serie_url(char* id) {
    char* url = get_series_url();
    strcat(url, "/");
    strcat(url, id);

    return url;
}

static char** tcgdex_get_series_id(int *length) {
    char* url = get_series_url();

    cJSON* json = curl_get_json(url);

    *length = cJSON_GetArraySize(json);

    char** series_id = malloc(sizeof(char*) * (size_t) *length);

    for (int i = 0; i < *length; i++) {
        cJSON* jsonSerie = cJSON_GetArrayItem(json, i);

        cJSON* id = cJSON_GetObjectItem(jsonSerie, "id");
        series_id[i] = strdup(id->valuestring);
    }

    cJSON_Delete(json);
    free(url);

    return series_id;
}

static Serie tcgdex_get_serie(char* serie_id) {
    char* url = get_serie_url(serie_id);

    cJSON* jsonSerie = curl_get_json(url);

    cJSON* id = cJSON_GetObjectItem(jsonSerie, "id");
    cJSON* name = cJSON_GetObjectItem(jsonSerie, "name");
    cJSON* logo = cJSON_GetObjectItem(jsonSerie, "logo");
    cJSON* release_date = cJSON_GetObjectItem(jsonSerie, "releaseDate");

    Serie serie;
    serie.id = strdup(id->valuestring);
    serie.name = strdup(name->valuestring);
    if (cJSON_IsString(logo)) {
        serie.logo = strdup(logo->valuestring);
    } else {
        serie.logo = strdup("");
    }
    if (cJSON_IsString(release_date)) {
        serie.release_date = strdup(release_date->valuestring);
    } else {
        serie.release_date = strdup("");
    }
    serie.extensions = malloc(sizeof(Extension) * 0);
    serie.extensions_length = 0;

    free(url);
    cJSON_Delete(jsonSerie);

    return serie;
}

Serie* tcgdex_get_series(int *length) {
    char** series_id = tcgdex_get_series_id(length);

    Serie* series = malloc(sizeof(Serie) * (size_t) *length);

    for (int i = 0; i < *length; i++) {
        Serie serie = tcgdex_get_serie(series_id[i]);
        series[i] = serie;
        free(series_id[i]);
    }

    free(series_id);

    return series;
}
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

static char* get_extension_url(char* id) {
    char* url = get_url();
    strcat(url, "sets/");
    strcat(url, id);

    return url;
}

static Extension tcgdex_get_extension(char* extension_id) {
    char* url = get_extension_url(extension_id);

    cJSON* jsonExtension = curl_get_json(url);

    free(url);

    char* id = cJSON_GetObjectItem(jsonExtension, "id")->valuestring;
    char* name = cJSON_GetObjectItem(jsonExtension, "name")->valuestring;
    
    cJSON* jsonLogo = cJSON_GetObjectItem(jsonExtension, "logo");
    char* logo = jsonLogo ? jsonLogo->valuestring : "";

    cJSON* jsonSymbol = cJSON_GetObjectItem(jsonExtension, "symbol");
    char* symbol = jsonSymbol ? jsonSymbol->valuestring : "";

    cJSON* card_count = cJSON_GetObjectItem(jsonExtension, "cardCount");
    int count_official = cJSON_GetObjectItem(card_count, "official")->valueint;
    int count_total = cJSON_GetObjectItem(card_count, "total")->valueint;

    char* release_date = cJSON_GetObjectItem(jsonExtension, "releaseDate")->valuestring;
    
    cJSON* jsonAbbreviation = cJSON_GetObjectItem(jsonExtension, "abbreviation");
    char* abbreviation = "";
    if (jsonAbbreviation) {
        abbreviation = cJSON_GetObjectItem(jsonAbbreviation, "official")->valuestring;
    }

    Extension extension = {
        .id = strdup(id),
        .name = strdup(name),
        .logo = strdup(logo),
        .symbol = strdup(symbol),
        .count_official = count_official,
        .count_total = count_total,
        .release_date = strdup(release_date),
        .cards = NULL,
        .abbreviation = strdup(abbreviation)
    };

    cJSON_Delete(jsonExtension);

    return extension;
}

static Serie tcgdex_get_serie(char* serie_id) {
    char* url = get_serie_url(serie_id);

    cJSON* jsonSerie = curl_get_json(url);

    cJSON* id = cJSON_GetObjectItem(jsonSerie, "id");
    cJSON* name = cJSON_GetObjectItem(jsonSerie, "name");
    cJSON* logo = cJSON_GetObjectItem(jsonSerie, "logo");
    cJSON* release_date = cJSON_GetObjectItem(jsonSerie, "releaseDate");
    cJSON* jsonExtensions = cJSON_GetObjectItem(jsonSerie, "sets");

    int extension_length = cJSON_GetArraySize(jsonExtensions);

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
    serie.extensions = malloc(sizeof(Extension) * (size_t)extension_length);
    for (int i = 0; i < extension_length; i++) {
        cJSON* jsonExtension = cJSON_GetArrayItem(jsonExtensions, i);
        serie.extensions[i] = tcgdex_get_extension(cJSON_GetObjectItem(jsonExtension, "id")->valuestring);
    }
    serie.extensions_length = extension_length;

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
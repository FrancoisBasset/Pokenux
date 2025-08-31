#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>
#include "database.h"
#include "../api/tcgdex.h"
#include "serie.h"
#include "extension.h"

sqlite3* database = NULL;
char* database_language;

static void database_insert_serie(Serie serie, char* language);
static void database_insert_extension(Extension extension, char* serie_id, char* language);

void database_init(void) {
    database_open();

    char* languages[] = { "en", "fr", "es" };

    char* series_sql = calloc(sizeof(char), 1000);
    char* extensions_sql = calloc(sizeof(char), 1000);

    for (int i = 0; i < 3; i++) {
        sprintf(series_sql, "CREATE TABLE 'series_%s' ('id' TEXT, 'name' TEXT, 'logo' TEXT, 'release_date' TEXT, PRIMARY KEY('id'))", languages[i]);
        sprintf(extensions_sql, "CREATE TABLE 'extensions_%s' ('id' TEXT, 'serie_id' INTEGER, 'name' TEXT, 'logo' TEXT, 'symbol' TEXT, 'count_official' INTEGER, 'count_total' INTEGER, 'release_date' TEXT, 'abbreviation' TEXT, PRIMARY KEY('id'))", languages[i]);

        sqlite3_exec(database, series_sql, NULL, NULL, NULL);
        sqlite3_exec(database, extensions_sql, NULL, NULL, NULL);
    }

    free(series_sql);
    free(extensions_sql);

    database_close();
}

void database_open(void) {
    if (database == NULL) {
        sqlite3_open("./pokenux.db", &database);
    }
}

void database_close(void) {
    if (database != NULL) {
        sqlite3_close(database);
        database = NULL;
    }
}

void database_set_language(char* language) {
    database_language = language;
}

void database_tcgdex_populate(char* language) {
    tcgdex_set_language(language);

    int series_length;
    Serie* series = tcgdex_get_series(&series_length);

    for (int i = 0; i < series_length; i++) {
        database_insert_serie(series[i], language);
        serie_free(series[i]);
    }

    free(series);
}

static void database_insert_serie(Serie serie, char* language) {
    char* insert_sql = calloc(sizeof(char), 1000);
    sprintf(insert_sql, "INSERT INTO series_%s VALUES (?, ?, ?, ?)", language);

    sqlite3_stmt *insert_stmt;
    sqlite3_prepare(database, insert_sql, 1000, &insert_stmt, NULL);
    sqlite3_bind_text(insert_stmt, 1, serie.id, -1, NULL);
    sqlite3_bind_text(insert_stmt, 2, serie.name, -1, NULL);
    sqlite3_bind_text(insert_stmt, 3, serie.logo, -1, NULL);
    sqlite3_bind_text(insert_stmt, 4, serie.release_date, -1, NULL);
    
    sqlite3_step(insert_stmt);

    for (int i = 0; i < serie.extensions_length; i++) {
        database_insert_extension(serie.extensions[i], serie.id, language);
        extension_free(serie.extensions[i]);
    }

    free(insert_sql);
    sqlite3_finalize(insert_stmt);
}

static void database_insert_extension(Extension extension, char* serie_id, char* language) {
    char* insert_sql = calloc(sizeof(char), 1000);
    sprintf(insert_sql, "INSERT INTO extensions_%s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", language);

    sqlite3_stmt *insert_stmt;
    sqlite3_prepare(database, insert_sql, 1000, &insert_stmt, NULL);
    sqlite3_bind_text(insert_stmt, 1, extension.id, -1, NULL);
    sqlite3_bind_text(insert_stmt, 2, serie_id, -1, NULL);
    sqlite3_bind_text(insert_stmt, 3, extension.name, -1, NULL);
    sqlite3_bind_text(insert_stmt, 4, extension.logo, -1, NULL);
    sqlite3_bind_text(insert_stmt, 5, extension.symbol, -1, NULL);
    sqlite3_bind_int(insert_stmt, 6, extension.count_official);
    sqlite3_bind_int(insert_stmt, 7, extension.count_total);
    sqlite3_bind_text(insert_stmt, 8, extension.release_date, -1, NULL);
    sqlite3_bind_text(insert_stmt, 9, extension.abbreviation, -1, NULL);

    free(insert_sql);
    
    sqlite3_step(insert_stmt);
    sqlite3_finalize(insert_stmt);
}

from tcgdexsdk import TCGdex

from pokenux.models.serie import Serie

def get_series():
    series: list[Serie] = []

    sdk = TCGdex('fr')

    for serie in sdk.serie.listSync():
        series.append(Serie(serie.id, serie.name))#, serie.logo))

    return series
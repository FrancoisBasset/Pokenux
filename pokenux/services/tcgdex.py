from tcgdexsdk import TCGdex, SerieResume, SetResume, Serie


class TcgDexService:
    def __init__(self, language: str) -> None:
        self.sdk = TCGdex(language)

    def get_series(self) -> list[SerieResume]:
        return self.sdk.serie.listSync()

    def get_sets(self, serie_id: str) -> list[SetResume]:
        serie: Serie = self.sdk.serie.getSync(serie_id)

        return serie.sets
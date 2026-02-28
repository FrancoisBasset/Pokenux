from textual.app import ComposeResult
from textual.screen import Screen
from tcgdexsdk import TCGdex
from textual.widgets import Label

class SeriesScreen(Screen):
    sdk = TCGdex('fr')
    series: list[tuple[str, str, str]] = []

    def on_mount(self):
        self.series = self.get_series()

    def compose(self) -> ComposeResult:
        for serie in self.series:
            yield Label(serie[0])

    def get_series(self) -> list:
        series: list[tuple[str, str, str]] = []

        for serie in self.sdk.serie.listSync():
            self.notify(serie.id)
            series.append((serie.id, serie.name, serie.logo))

        return series
from textual.app import ComposeResult
from tcgdexsdk import SerieResume
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button

from pokenux.services.tcgdex import TcgDexService

class SeriesContent(Widget):
    series: list[SerieResume] = reactive([], recompose=True)

    def on_mount(self):
        self.series = TcgDexService('fr').get_series()

    class SerieSelected(Message):
        def __init__(self, serie: SerieResume):
            super().__init__()
            self.serie = serie

    def compose(self) -> ComposeResult:
        for serie in self.series:
            yield Button(serie.name, id=serie.id)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        selected_serie = [serie for serie in self.series if serie.id == event.button.id]
        self.post_message(self.SerieSelected(selected_serie[0]))
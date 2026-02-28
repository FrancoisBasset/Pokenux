from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button

from pokenux.components.breadcrumb import Breadcrumb
from pokenux.models.serie import Serie
from pokenux.models.set import Set

class CardExplorerScreen(Screen):
    breadcrumb: Breadcrumb
    series: list[Serie] = [
        Serie('EV', 'Ecarlate et Violet'),
        Serie('EB', 'Épée et Bouclier'),
        Serie('SL', 'Soleil et Lune')
    ]
    selected_serie: Serie | None = reactive(None)
    selected_set: Set | None = None

    def on_mount(self):
        self.breadcrumb = self.query_one('#breadcrumb', Breadcrumb)

    def compose(self) -> ComposeResult:
        yield Breadcrumb(id='breadcrumb')
        for serie in self.series:
            yield Button(serie.name, id=serie.id)

    @on(Button.Pressed, '#all_series_button')
    def on_all_series_button_pressed(self):
        self.selected_serie = None

    def on_button_pressed(self, event: Button.Pressed):
        if self.selected_serie is None and event.button.id != 'all_series_button':
            self.selected_serie = [s for s in self.series if s.id == event.button.id][0]

    def watch_selected_serie(self):
        if self.selected_serie is None:
            self.breadcrumb.buttons = [('all_series_button', 'Toutes les séries')]
            for serie in self.series:
                self.query_one('#' + serie.id, Button).display = True
        else:
            self.breadcrumb.buttons = [*self.breadcrumb.buttons, (self.selected_serie.id, self.selected_serie.name)]
            for serie in self.series:
                self.query_one('#' + serie.id, Button).display = False
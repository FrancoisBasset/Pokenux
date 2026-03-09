from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widgets import Button

class CardExplorerBreadcrumb(HorizontalGroup):
    serie: str|None = reactive(None, recompose=True)
    set: str|None = reactive(None, recompose=True)

    DEFAULT_CSS = """
    Button {
        border: none !important;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Button('Toutes les séries', id='all_series_button')
        if self.serie:
            yield Button(self.serie, id='serie_button')
            if self.set:
                yield Button(self.set)

    @on(Button.Pressed, '#all_series_button')
    def on_all_series_button_pressed(self) -> None:
        self.serie = None
        self.parent.serie = None
        self.set = None
        self.parent.set = None
        self.refresh()

    @on(Button.Pressed, '#current_serie_button')
    def on_current_serie_button_pressed(self) -> None:
        self.set = None
        self.parent.set = None
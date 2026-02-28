from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widgets import Button

class Breadcrumb(HorizontalGroup):
    buttons: reactive[list[tuple[str, str]]] = reactive([], recompose=True)

    DEFAULT_CSS = """
    Button {
        border: none !important;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        for button in self.buttons:
            yield Button(button[1], id=button[0])

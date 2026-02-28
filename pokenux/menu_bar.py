from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.events import Click
from textual.widgets import Static

class MenuBar(HorizontalGroup):
    DEFAULT_CSS = """
    Static {
        background: black;
    }
    """
    selected_screen: str

    def __init__(self, selected_screen: str = None):
        super().__init__()
        self.selected_screen = selected_screen

    def on_mount(self):
        if self.selected_screen:
            self.query_one('#' + self.selected_screen + '-button', Static).styles.background = 'green'

    def compose(self) -> ComposeResult:
        yield Static("Menu", id="menu-button")
        yield Static("Dashboard", id="dashboard-button")
        yield Static("Paramètres", id="settings-button")

    @on(Click, '#menu-button')
    def on_click_menu(self):
        self.app.push_screen('menu')

    @on(Click, '#dashboard-button')
    def on_click_dashboard(self):
        self.app.push_screen('dashboard')

    @on(Click, '#settings-button')
    def on_click_settings(self):
        self.app.push_screen('settings')
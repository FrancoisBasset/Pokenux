from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label

from pokenux.menu_bar import MenuBar

class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Dashboard")
        yield MenuBar('dashboard')

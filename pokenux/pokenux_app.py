from textual.app import App, ComposeResult

from pokenux.menu_bar import MenuBar
from pokenux.screens.settings_screen import SettingsScreen
from pokenux.screens.menu_screen import MenuScreen
from pokenux.screens.dashboard_screen import DashboardScreen
from pokenux.screens.card_explorer_screen import CardExplorerScreen

class PokenuxApp(App):
    SCREENS = {
        'menu': MenuScreen,
        'dashboard': DashboardScreen,
        'settings': SettingsScreen,
        'card-explorer': CardExplorerScreen
    }

    CSS_PATH = 'pokenux.tcss'

    def compose(self) -> ComposeResult:
        yield MenuBar()
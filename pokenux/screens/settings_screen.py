from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Select, Button

from pokenux.menu_bar import MenuBar

class SettingsScreen(Screen):
    languages = [('English', 'en'), ('Français', 'fr')]

    def compose(self) -> ComposeResult:
        yield Select(options=self.languages, tooltip='App language')
        yield Select(options=self.languages, tooltip='Card language')
        yield Select(options=self.languages, tooltip='Pokémon language')
        yield Button('Reset data')

        yield MenuBar('settings')
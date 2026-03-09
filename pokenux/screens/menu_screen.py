from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button

from pokenux.menu_bar import MenuBar

class MenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label('TCG')
        yield Button('Voir les cartes', id='card-explorer-button')
        yield Button('Quiz')
        yield Button('Simulateur')
        yield Label('Pokédex')
        yield Button('Voir les Pokémon')
        yield Button('Quiz')
        yield MenuBar('menu')

    @on(Button.Pressed, '#card-explorer-button')
    def on_card_explorer_button_click(self):
        self.app.push_screen('card-explorer')
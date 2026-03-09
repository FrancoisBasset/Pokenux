from tcgdexsdk import SetResume
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button

class SetsContent(Widget):
    sets: list[SetResume] = reactive([], recompose=True)

    def compose(self) -> ComposeResult:
        for set in self.sets:
            yield Button(set.name, id=set.id.replace('.', '-'))

    class SetSelected(Message):
        def __init__(self, set: SetResume):
            super().__init__()
            self.set = set

    def on_button_pressed(self, event: Button.Pressed) -> None:
        selected_set = [set for set in self.sets if set.id == event.button.id.replace('-', '.')]
        self.post_message(self.SetSelected(selected_set[0]))
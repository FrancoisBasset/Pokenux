from typing import cast

from textual.app import App
from textual.widgets import TabPane, TabbedContent

from pokenux.textual.utils import enums, i18n
from pokenux.textual.utils.bindings import get_main_bindings
from textual.css.query import NoMatches


class Translator:
    def __init__(self, app: App):
        self.app = app

    def translate_app(self):
        bindings = get_main_bindings()

        for binding in bindings:
            self.app._bindings.key_to_bindings[binding.key] = [binding]

        self.app.refresh_bindings()

        self._translate_inputs()
        self._translate_buttons()
        self._translate_panes()
        self._translate_labels()
        self._translate_selects()

    def _translate_selects(self):
        for select in self.app.query("Select.i18n"):
            if select.name:
                select.prompt = i18n.trans(select.name)
                select.set_options(getattr(enums, select.name)())

    def _translate_inputs(self):
        for input_widget in self.app.query("Input.i18n"):
            if input_widget.name:
                input_widget.placeholder = i18n.trans(input_widget.name)

    def _translate_labels(self):
        for label in self.app.query("Label.i18n"):
            if label.name:
                label.update(i18n.trans(label.name))

    def _translate_buttons(self):
        for button in self.app.query("Button.i18n"):
            if button.name:
                button.label = i18n.trans(button.name)

    def _translate_panes(self):
        for tab_pane in self.app.query("TabPane.i18n"):
            if tab_pane.name:
                try:
                    tabbed_content = cast(
                        TabbedContent,
                        tab_pane.query_ancestor(TabbedContent, TabbedContent),
                    )
                    tab = tabbed_content.get_tab(tab_pane)
                except NoMatches:
                    tab_pane._title = tab_pane.render_str(
                        self._tab_pane_title(tab_pane)
                    )
                    continue

                title = self._tab_pane_title(
                    tab_pane,
                    closable=tab.label_text.rstrip().endswith("×"),
                )
                tab_pane._title = tab_pane.render_str(title)
                tab.label = title

    def _tab_pane_title(self, tab_pane: TabPane, closable: bool = False) -> str:
        if tab_pane.name is None:
            return ""

        title = i18n.trans(tab_pane.name)
        if closable and tab_pane.id:
            title += f" [bold @click=app.close_tab('{tab_pane.id}')]×[/]"

        return title

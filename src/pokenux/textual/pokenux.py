from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label, TabPane, TabbedContent
from pokenux.services.user_data import UserData
from pokenux.textual.utils import bindings, i18n
from textual.css.query import NoMatches

from pokenux.textual.views.parameters_view import ParametersView

UserData.init()
i18n.set_language(UserData.config_file.get("app_lang", "en"))


class Pokenux(App):
    BINDINGS = bindings.get_main_bindings()
    CSS_PATH = "style.css"

    def on_mount(self):
        self.tabbed_content: TabbedContent = self.query_one("#tabbed_content")
        self.panes: list[TabPane] = []

    def compose(self) -> ComposeResult:
        yield Header(name="Pokenux", icon="◒")
        with TabbedContent(id="tabbed_content"):
            with TabPane("+", id="tab_new_tab"):
                yield Label(i18n.trans("new"), name="new", classes="i18n")
        yield Footer()

    def action_close_tab(self, tab_id: str) -> None:
        self.tabbed_content.remove_pane(tab_id)

    async def action_show_parameters(self) -> None:
        try:
            self.tabbed_content.get_pane("parameters")
        except NoMatches:
            parameter_view = TabPane(
                i18n.trans("parameters")
                + " [bold @click=app.close_tab('parameters')]×[/]",
                ParametersView(),
                id="parameters",
                name="parameters",
                classes="i18n",
            )
            await self.tabbed_content.add_pane(parameter_view, before="tab_new_tab")

        self.tabbed_content.active = "parameters"

from textual.binding import Binding

from pokenux.services.user_data import UserData
from pokenux.textual.utils import i18n


def get_main_bindings() -> list[Binding]:
    UserData.init()
    i18n.set_language(UserData.config_file.get("app_lang", "en"))

    return [
        Binding("q", "quit", i18n.trans("quit")),
        Binding("p", "show_parameters", i18n.trans("parameters")),
    ]

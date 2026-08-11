import gettext
from pathlib import Path


def set_language(language: str):
    localesPath = Path(__file__).resolve().parent.parent.parent / "locales"

    global trans
    trans = gettext.translation(
        "pokenux", localedir=localesPath, languages=[language]
    ).gettext

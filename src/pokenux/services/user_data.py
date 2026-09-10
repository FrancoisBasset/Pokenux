import json
from pathlib import Path
from typing import Callable
from urllib.request import urlopen
from zipfile import ZipFile

from tcgdexsdk import Serie
import tomlkit

from pokenux.models.pokemon.pokemon import Pokemon


class UserData:
    path: str
    config_path: str
    assets_path: str
    config_file: tomlkit.TOMLDocument

    @staticmethod
    def init():
        UserData.path = str(Path.home()) + "/.local/share/pokenux"
        UserData.assets_path = UserData.path + "/assets"
        UserData.config_path = UserData.path + "/config.toml"

        if not Path.exists(UserData.path):
            Path.mkdir(UserData.path)

        if not Path.exists(UserData.config_path):
            Path.touch(UserData.config_path)

        UserData.config_file = tomlkit.load(open(UserData.config_path))

    @staticmethod
    def assets_are_missing() -> bool:
        return (
            not Path.exists(UserData.assets_path)
            or len(list(Path(UserData.assets_path).glob("**/*"))) == 0
        )

    @staticmethod
    def download_assets(cancelled: Callable[[], bool]) -> bool:
        url = "https://github.com/FrancoisBasset/pokenux/releases/download/1.0.0/pokenux-data.zip"

        path = Path(UserData.path)
        zip_path = path / "pokemon-data.zip"

        try:
            with urlopen(url) as response:
                with zip_path.open("wb") as file:
                    while chunk := response.read(1024 * 1024):
                        if cancelled():
                            return False

                        file.write(chunk)

            if cancelled():
                return False

            # Extract
            with ZipFile(zip_path, "r") as zip_file:
                for member in zip_file.infolist():
                    if cancelled():
                        return False

                    zip_file.extract(member, path)

            return True

        finally:
            zip_path.unlink(missing_ok=True)

    @staticmethod
    def save_config():
        with open(UserData.config_path, "w") as file:
            tomlkit.dump(UserData.config_file, file)

    @staticmethod
    def get_all_pokemon() -> list[Pokemon]:
        with open(UserData.path + "/assets/data/pokemon.json", "r") as f:
            return [Pokemon.from_dict(data) for data in json.load(f)]

    @staticmethod
    def get_all_series(language: str) -> list[Serie]:
        with open(f"{UserData.path}/assets/data/tcg_{language}.json", "r") as f:
            return [Serie.from_dict(data) for data in json.load(f)]

    @staticmethod
    def get_all_generations() -> list[str]:
        with open(UserData.path + "/assets/data/generations.json", "r") as f:
            return json.load(f)

    @staticmethod
    def get_all_types() -> list:
        with open(UserData.path + "/assets/data/types.json", "r") as f:
            return json.load(f)

    @staticmethod
    def get_app_lang() -> str:
        return UserData.config_file.get("app_lang", "en")

    @staticmethod
    def get_pokemon_lang() -> str:
        return UserData.config_file.get("pokemon_lang", "en")

    @staticmethod
    def get_tcg_lang() -> str:
        return UserData.config_file.get("tcg_lang", "en")

    @staticmethod
    def set_app_lang(lang: str):
        UserData.config_file["app_lang"] = lang

    @staticmethod
    def set_pokemon_lang(lang: str):
        UserData.config_file["pokemon_lang"] = lang

    @staticmethod
    def set_tcg_lang(lang: str):
        UserData.config_file["tcg_lang"] = lang
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

        UserData.init_config()

    @staticmethod
    def init_config():
        if not Path.exists(UserData.config_path):
            Path.touch(UserData.config_path)

        UserData.config_file = tomlkit.load(open(UserData.config_path))
        UserData.config_file.setdefault("app_lang", "en")
        UserData.config_file.setdefault("pokemon_lang", "en")
        UserData.config_file.setdefault("tcg_lang", "en")

    @staticmethod
    def assets_are_missing() -> bool:
        return (
            not Path.exists(UserData.assets_path)
            or len(list(Path(UserData.assets_path).glob("**/*"))) == 0
        )

    @staticmethod
    def download_assets(cancelled: Callable[[], bool]) -> bool:
        url = "https://github.com/FrancoisBasset/pokenux/releases/download/1.0.0/pokemon-data-1.0.0.zip"

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
    def get_all_pokemon_from_jsons() -> list[Pokemon]:
        with open(UserData.path + "/assets/data/pokemon.json", "r") as f:
            return [Pokemon.from_dict(data) for data in json.load(f)]

    @staticmethod
    def get_series_from_jsons(language: str) -> list[Serie]:
        with open(f"{UserData.path}/assets/data/tcg_{language}.json", "r") as f:
            return [Serie.from_dict(data) for data in json.load(f)]

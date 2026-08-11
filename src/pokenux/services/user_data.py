from pathlib import Path

import tomlkit


class UserData:
    _config_path: str
    config_file: tomlkit.TOMLDocument

    @staticmethod
    def init():
        path: str = str(Path.home()) + "/.local/share/pokenux"
        UserData._config_path = path + "/config.toml"

        if not Path.exists(path):
            Path.mkdir(path)

        if not Path.exists(UserData._config_path):
            Path.touch(UserData._config_path)

        UserData.config_file = tomlkit.load(open(UserData._config_path))

    @staticmethod
    def save_config():
        with open(UserData._config_path, "w") as file:
            tomlkit.dump(UserData.config_file, file)

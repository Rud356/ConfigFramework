from os import environ, getcwd
from pathlib import Path
from configparser import ConfigParser

_configframework_config_path = (
    environ.get('CONFIGFRAMEWORK_SETTINGS_PATH') or
    Path(getcwd()) / "configframework_settings.ini"
)

try:
    with open(_configframework_config_path, encoding='utf8') as f:
        config = ConfigParser()
        config.read_file(f)

    if 'LoadersVariables' not in config:
        raise ValueError("No data")

except (FileNotFoundError, ValueError):
    config = ConfigParser()
    config.add_section("LoadersVariables")
    config.set("LoadersVariables", "LogPath", "config_framework.log")
    config.set("LoadersVariables", "AllowCreatingNotExistingKeys", "False")
    config.set("LoadersVariables", "JSONConfigLoader.dump_indent", "4")
    config.set("LoadersVariables", "EnvironmentConfigLoader.mute_warning", "False")

    with open(_configframework_config_path, 'w', encoding='utf8') as f:
        config.write(f)

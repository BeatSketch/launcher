from typing import Literal, cast as _cast

from util.config import save as _save
from util.config.dtype import BeatSketchConfig
from util.config.load import (
    load_config_file as _load_config_file,
    default_config as _default_config,
    validate as _validate,
)
from util.config.merge import merge as _merge


def load_and_validate_config(path: str) -> tuple[bool, BeatSketchConfig]:
    """Load the configuration file from the specified path and validate it with the jsonschema

    Args:
        path: The path to the config file to load

    Returns:
        A tuple containing validation status and a valid config (if validation is False, the default config)
    """
    try:
        loaded_config = _load_config_file(path)
    except Exception:
        return (False, _default_config())

    global _config
    global _config_location

    _config_location = path

    if _validate(loaded_config):
        conf = _cast(
            BeatSketchConfig, _merge(_cast(dict, _default_config()), loaded_config)
        )
        _config = conf
        return (True, conf)
    else:
        _config = _default_config()
        return (False, _default_config())


global _config
_config = _default_config()

global _config_location
_config_location = "config.yml"


def get_config() -> BeatSketchConfig:
    return _config


def update_rotation(side: Literal["x", "y", "z"], value: str):
    try:
        validated = int(value)

        global _config
        _config["saber_angle"][side] = validated
    except Exception:
        pass


def update_enabled_cleanup(kind: Literal["distance", "collisions"], enabled: bool):
    global _config
    _config["cleanup"][kind] = enabled


def update_vibrate(enabled: bool):
    global _config
    _config["vibrate"] = enabled


def save_config():
    _save.save_config(_config, _config_location)

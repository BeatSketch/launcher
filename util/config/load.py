import jsonschema as _jsonschema
import json as _json
import yaml as _yaml

from util.config.dtype import BeatSketchConfig

# Load schema
with open("config.schema.json") as file:
    _schema = _json.load(file)
    file.close()


def load_config_file(file: str) -> dict:
    """Loads and parses the yaml file at the specified location

    Args:
        file: Filepath to the config file to be loaded

    Returns:
        A dict containing the parsed yaml file
    """
    with open(file, "r") as f:
        parsed = _yaml.load(f, Loader=_yaml.FullLoader)
    return parsed


def validate(config: dict | list) -> bool:
    """Validates the provided config

    Args:
        config: The config to validate

    Returns:
        True if the config passed schema validation, false otherwise
    """
    try:
        _jsonschema.validate(config, _schema)
    except _jsonschema.SchemaError:
        print("Schema invalid")
        return False
    except _jsonschema.ValidationError:
        print("Config invalid")
        return False

    return True


def default_config() -> BeatSketchConfig:
    """Get the default configuration. Is used as a starting position for the config

    Returns:
        The default configuration
    """
    return {
        "saber_angle": {"x": -20, "y": 0, "z": 0},
        "default_save_path": "~/BeatSketch/",
        "folder_loc_for_picker": "~/Downloads/",
        "mirror": False,
        "used_model": "mlp",
        "cleanup": {"collisions": True, "distance": True},
        "vibrate": True,
    }

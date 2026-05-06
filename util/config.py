from typing import TypedDict, cast
import jsonschema
import json
import yaml


class BeatSketchConfig(TypedDict):
    saber_angle: BeatSketchSaberAngleConfig
    default_save_path: str
    folder_loc_for_picker: str


class BeatSketchSaberAngleConfig(TypedDict):
    x: int
    y: int
    z: int


# Load schema
with open("config.schema.json") as file:
    schema = json.load(file)
    file.close()


def _load_config_file(file: str) -> dict:
    """Loads and parses the yaml file at the specified location

    Args:
        file: [TODO:description]

    Returns:
        [TODO:return]
    """
    with open(file, "r") as f:
        parsed = yaml.load(f, Loader=yaml.FullLoader)
    return parsed


def _validate(config: dict | list) -> bool:
    """Validates the provided config

    Args:
        config: The config to validate

    Returns:
        True if the config passed schema validation, false otherwise
    """
    try:
        jsonschema.validate(config, schema)
    except jsonschema.SchemaError:
        print("Schema invalid")
        return False
    except jsonschema.ValidationError:
        print("Config invalid")
        return False

    return True


def _default_config() -> BeatSketchConfig:
    """Get the default configuration. Is used as a starting position for the config

    Returns:
        The default configuration
    """
    return {
        "saber_angle": {"x": 20, "y": 0, "z": 0},
        "default_save_path": "~",
        "folder_loc_for_picker": "~/Downloads",
    }


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

    def merge(a: dict, b: dict) -> dict:
        """Merge two dictionaries. Dict b takes precedence

        Args:
            a: The base dictionary to merge into
            b: The dictionary to merge into a. Its values take precedence

        Returns:
            The merged dictionary
        """
        combined = {}
        for key in b:
            val = b[key]
            try:
                a[key]
                if isinstance(val, dict):
                    combined[key] = merge(val, a[key])
                elif isinstance(val, list):
                    combined[key] = val
                    for v in a[key]:
                        combined[key].append(v)
                else:
                    combined[key] = val
            except KeyError:
                combined[key] = val

        for key in a:
            try:
                b[key]
            except KeyError:
                combined[key] = a[key]

        return combined

    if _validate(loaded_config):
        return (
            True,
            cast(BeatSketchConfig, merge(cast(dict, _default_config()), loaded_config)),
        )
    else:
        return (False, _default_config())

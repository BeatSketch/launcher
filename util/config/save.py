import yaml

from util.config.dtype import BeatSketchConfig


def save_config(config: BeatSketchConfig, path: str):
    # Add below to the output string
    out = "# yaml-language-server: $schema=https://raw.githubusercontent.com/BeatSketch/launcher/refs/heads/main/config.schema.json\n\n"
    with open(path, "w") as f:
        f.write(out + yaml.dump(config))

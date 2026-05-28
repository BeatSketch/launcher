import json


def save_lightshow(path: str):
    with open(path, "w") as file:
        file.write(json.dumps({ "version": "4.0.0" }))

from map_handler.map.load import beatmap_v3, info_v2
from map_handler.map.load.dtype import BeatSketchParsingBeatMapDifficultyData
from map_handler.map.map import BeatSaberMap
import json as _json


def load_map(path: str) -> BeatSaberMap | None:
    """Load a map from the specified path

    Args:
        path: Path to the folder to load the map from

    Returns:
        True if parsing of info file parsing was successful
    """
    base_path = path + ("" if path.endswith("/") else "/")
    beatmaps, map = _parse_info(base_path)
    if not map:
        return None

    for map_details in beatmaps:
        _parse_beatmap(base_path, map_details, map)

    return map


def _parse_info(
    path: str,
) -> tuple[list[BeatSketchParsingBeatMapDifficultyData], BeatSaberMap | None]:
    """Parse an info file at the specified path

    Returns:
        Tuple containing first the status,
        then the list of beatmap file names
    """
    with open(path + "Info.dat", "r") as f:
        data = _json.loads(f.read())
        try:
            if data["_version"] == "2.0.0" or data["_version"] == "2.1.0":
                return info_v2.parse(data, path)
        except KeyError:
            try:
                pass
            except KeyError:
                pass

    return [], None


def _parse_beatmap(
    path: str,
    details: BeatSketchParsingBeatMapDifficultyData,
    map: BeatSaberMap,
) -> bool:
    """Parse a beatmap / difficulty at the specified path

    Returns:
        True if parsing was successful, False otherwise
    """
    with open(path + details["file"], "r") as f:
        data = _json.loads(f.read())
        try:
            # Parse V3 format (more coming in the future)
            if (
                data["version"] == "3.0.0"
                or data["version"] == "3.1.0"
                or data["version"] == "3.2.0"
                or data["version"] == "3.3.0"
            ):
                return beatmap_v3.parse(data, details, map)
        except KeyError:
            try:
                pass
            except KeyError:
                pass

    return False

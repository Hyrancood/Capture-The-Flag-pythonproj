import pathlib
import re
import pygame


class Paths:
    def __init__(self, assets=None, maps=None):
        self.assets = assets
        self.maps = maps


INSTANCE = Paths()


def load_assets(dir: str) -> dict:
    result = {}
    for path in pathlib.Path(dir).iterdir():
        if path.is_dir():
            result.update(load_assets(f"{dir}/{path.name}"))
            continue
        result[f"{dir}/{path.name}"] = pygame.image.load(f"{dir}/{path.name}")
    return result


def read_config(path: str):
    global INSTANCE
    file = pathlib.Path(path)
    if file.is_dir():
        raise ValueError("Path should be a file")
    for line in open(path):
        line = line.strip()
        if re.fullmatch(r"assets\s*=\s*\".*\"", line):
            assets_path = line[line.find("\"")+1:line.rfind("\"")].strip()
            if not pathlib.Path(assets_path).is_dir():
                raise ValueError(f"Assets folder error: {assets_path}")
            INSTANCE.assets = assets_path
        elif re.fullmatch(r"maps\s*=\s*\".*\"", line):
            maps_path = line[line.find("\"")+1:line.rfind("\"")].strip()
            if not pathlib.Path(maps_path).is_dir():
                raise ValueError(f"Maps folder error: {maps_path}")
            INSTANCE.maps = maps_path
        elif not re.fullmatch(r"\s*", line):
            raise ValueError(f"Corrupted string: {line}")
    if INSTANCE.assets is None:
        raise ValueError("No assets directory set")
    if INSTANCE.maps is None:
        raise ValueError("No maps directory set")
    INSTANCE.assets = load_assets(INSTANCE.assets)

def get(asset_name: str) -> pygame.Surface:
    global INSTANCE
    return INSTANCE.assets.get(f"assets/{asset_name}")
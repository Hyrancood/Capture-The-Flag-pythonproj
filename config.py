import pathlib
import re

import pygame


class Paths:
    def __init__(self, assets=None, maps=None, replays=None):
        self.assets = assets
        self.maps = maps
        self.replays = replays


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
        elif re.fullmatch(r"replays\s*=\s*\".*\"", line):
            replays_path = line[line.find("\"")+1:line.rfind("\"")].strip()
            if not pathlib.Path(replays_path).is_dir():
                raise ValueError(f"Maps folder error: {replays_path}")
            INSTANCE.replays = replays_path
        elif not re.fullmatch(r"\s*", line):
            raise ValueError(f"Corrupted string: {line}")
    if INSTANCE.assets is None:
        raise ValueError("No assets directory set")
    if INSTANCE.maps is None:
        raise ValueError("No maps directory set")
    if INSTANCE.replays is None:
        raise ValueError("No replays directory set")
    assets_path = INSTANCE.assets
    INSTANCE.assets = load_assets(assets_path)
    files = set()
    for file in {'assets/map_choose_button.png', 'assets/ability1.png', 'assets/ground/right_ground.png', 'assets/ability2_pushed.png', 'assets/ability2.png', 'assets/ability5.png', 'assets/ground/bottom_right_ground.png', 'assets/map_choose_error_button.png', 'assets/start.png', 'assets/ground/top_left_corner_ground.png', 'assets/ground/top_right_corner_ground.png', 'assets/ground/bottom_right_corner_ground.png', 'assets/ground/ground.png', 'assets/abilities.png', 'assets/open_maps_folder.png', 'assets/ability3.png', 'assets/ability5_pushed.png', 'assets/reload_maps_button.png', 'assets/ground/left_ground.png', 'assets/ground/top_right_ground.png', 'assets/ground/bottom_left_corner_ground.png', 'assets/ground/top_ground.png', 'assets/maps_menu_bg.png', 'assets/ground/bottom_ground.png', 'assets/ability4_pushed.png', 'assets/ability1_pushed.png', 'assets/ground/bottom_left_ground.png', 'assets/thorns.png', 'assets/main_menu_bg.png', 'assets/ground/top_left_ground.png', 'assets/play.png', 'assets/ability3_pushed.png', 'assets/replays.png', 'assets/start_pushed.png', 'assets/maps_menu_play_button.png', 'assets/ability4.png'}:
        if INSTANCE.assets.get(file) is None:
            files.add(file)
    if len(files) > 0:
        raise ValueError(f"Folder {assets_path} hasn't some assets: '{files}")

def get(asset_name: str) -> pygame.Surface:
    global INSTANCE
    return INSTANCE.assets.get(f"assets/{asset_name}")
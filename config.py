"""Хранит конфигурационную информацию и загруженные ресурсы"""

import pathlib
import re
from typing import Dict

import pygame


class Paths:
    """
    Хранит используемые игрой пути

    :ivar assets: путь к ресурсам (текстуры и т.п.)
    :type assets: str
    :ivar maps: путь к файлам игровых карт
    :type maps: str
    :ivar replays: путь к папке с записями игр
    :type replays: str
    """

    def __init__(self, assets: str = None, maps: str = None, replays: str = None):
        """
        Создание экземпляра

        :param assets: путь к ресурсам
        :param maps: путь к картам
        :param replays: путь к записям
        """
        self.assets = assets
        self.maps = maps
        self.replays = replays


INSTANCE = Paths()
"""Используемый экземляр"""


def load_assets(directory: str) -> Dict[str, pygame.Surface]:
    """
    Рекурсивно загружает все ресурсы из указанной директории (и вложенных)

    :param directory: папка с ресурсами
    :return: словарь с загруженными ресурсами
    """
    result = {}
    for path in pathlib.Path(directory).iterdir():
        if path.is_dir():
            result.update(load_assets(f"{directory}/{path.name}"))
            continue
        result[f"{directory}/{path.name}"] = pygame.image.load(f"{directory}/{path.name}")
    return result


def read_config(path: str):
    """
    Считывание переданного конфиг-файла

    :param path: путь к конфигурационному файлу
    :raises ValueError:
        если переданный путь оказался директорией, а не файлом
        если в файле оказалась непредусмотренная строка
        если указанный в конфиге путь вёл на файл, а не на директорию
        если обязательная директория не была указана
        если в папке с ресурсами не оказалось некоторых файлов
    """
    global INSTANCE
    file = pathlib.Path(path)
    if file.is_dir():
        raise ValueError("Path should be a file")
    paths = {"assets": None, "maps": None, "replays": None}
    for line in open(path):
        line = line.strip()
        conf = None
        for c in paths:
            if re.fullmatch(rf"{c}\s*=\s*\".*\"", line):
                conf = c
        if conf is None:
            if not re.fullmatch(r"\s*", line):
                raise ValueError(f"Corrupted string: {line}")
            else:
                continue
        full_path = f"{file.parent}/{line[line.find("\"") + 1:line.rfind("\"")].strip()}"
        folder = pathlib.Path(full_path)
        if not folder.exists():
            folder.mkdir()
        if not folder.is_dir():
            raise ValueError(f"{conf} folder error: {full_path}")
        paths[conf] = full_path
    INSTANCE = Paths(**paths)
    if INSTANCE.assets is None:
        raise ValueError("No assets directory set")
    if INSTANCE.maps is None:
        raise ValueError("No maps directory set")
    if INSTANCE.replays is None:
        raise ValueError("No replays directory set")
    assets_path = INSTANCE.assets
    INSTANCE.assets = (assets_path, load_assets(assets_path))
    files = set()
    for file in {'map_choose_button.png', 'ability1.png', 'ground/right_ground.png', 'ability2_pushed.png',
                 'ability2.png', 'ability5.png', 'ground/bottom_right_ground.png', 'map_choose_error_button.png',
                 'start.png', 'ground/top_left_corner_ground.png', 'ground/top_right_corner_ground.png',
                 'ground/bottom_right_corner_ground.png', 'ground/ground.png', 'abilities.png', 'open_maps_folder.png',
                 'ability3.png', 'ability5_pushed.png', 'reload_maps_button.png', 'ground/left_ground.png',
                 'ground/top_right_ground.png', 'ground/bottom_left_corner_ground.png', 'ground/top_ground.png',
                 'maps_menu_bg.png', 'ground/bottom_ground.png', 'ability4_pushed.png', 'ability1_pushed.png',
                 'ground/bottom_left_ground.png', 'thorns.png', 'main_menu_bg.png', 'ground/top_left_ground.png',
                 'play.png', 'ability3_pushed.png', 'replays.png', 'start_pushed.png', 'maps_menu_play_button.png',
                 'ability4.png', "rec_on.png", "rec_off.png"}:
        if INSTANCE.assets[1].get(f"{INSTANCE.assets[0]}/{file}") is None:
            files.add(file)
    if len(files) > 0:
        raise ValueError(f"Folder {assets_path} hasn't some assets: '{files}")


def get(asset_name: str) -> pygame.Surface:
    """
    Возвращает загруженный файл по его имени

    :param asset_name: название ресурса
    :return: ресурс
    """
    global INSTANCE
    return INSTANCE.assets[1].get(f"{INSTANCE.assets[0]}/{asset_name}")

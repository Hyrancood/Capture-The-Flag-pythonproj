"""Рендерер карты"""
from typing import List, Tuple

import pygame

import config
import gamemap as gmap


def get_platform(name:str) -> pygame.Surface:
    """
    Получение текстуры земли по укороченному названию

    :param name: укороченное название
    :return: загруженная текстура
    """
    name = name.replace("-", "_") + "_ground" if name != "ground" else name
    return config.get(f"ground/{name}.png")



def get_sprite(x: int, y: int, map_platforms: List[List[int]], sizes:Tuple[int, int]) -> pygame.Surface:
    """
    Получение текстуры платформы в зависимости от наличия и расположения соседей

    :param x: 'x'-кордината платформы
    :param y: 'y'-кордината платформы
    :param map_platforms: матрица карты с платформами
    :param sizes: размеры карты
    :return: текстура
    """
    sprite = get_platform("ground")
    if y - 1 >= 0 and x + 1 < sizes[0]:
        if map_platforms[y - 1][x] and map_platforms[y][x+1] and not map_platforms[y-1][x+1]:
            return get_platform("top-right-corner")
    if y - 1 >= 0 and x - 1 >= 0:
        if map_platforms[y - 1][x] and map_platforms[y][x-1] and not map_platforms[y-1][x-1]:
            return get_platform("top-left-corner")
    if y + 1 < sizes[1] and x + 1 < sizes[0]:
        if map_platforms[y + 1][x] and map_platforms[y][x+1] and not map_platforms[y+1][x+1]:
            return get_platform("bottom-right-corner")
    if y + 1 < sizes[1] and x - 1 >= 0:
        if map_platforms[y + 1][x] and map_platforms[y][x-1] and not map_platforms[y+1][x-1]:
            return get_platform("bottom-left-corner")
    if y - 1 >= 0:
        if not map_platforms[y - 1][x]:
            sprite = get_platform("top")
            if x + 1 < sizes[0]:
                if not map_platforms[y][x + 1]:
                    sprite = get_platform("top-right")
            if x - 1 >= 0:
                if not map_platforms[y][x - 1]:
                    sprite = get_platform("top-left")
            return sprite
    if y + 1 < sizes[1]:
        if not map_platforms[y + 1][x]:
            sprite = get_platform("bottom")
            if x + 1 < sizes[0]:
                if not map_platforms[y][x + 1]:
                    sprite = get_platform("bottom-right")
            if x - 1 >= 0:
                if not map_platforms[y][x - 1]:
                    sprite = get_platform("bottom-left")
            return sprite
    if x + 1 < sizes[0]:
        if not map_platforms[y][x+1]:
            sprite = get_platform("right")
    if x - 1 >= 0:
        if not map_platforms[y][x-1]:
            sprite = get_platform("left")
    return sprite


def map_surface(gamemap: gmap.Map) -> pygame.Surface:
    """
    Отрисовка игровой карты

    :param gamemap: игровая карта
    :return: отрисованное изображение карты
    """
    sizes = gamemap.get_sizes()
    sizes32 = (sizes[0]*32, sizes[1]*32)
    surface = pygame.Surface(sizes32)
    surface.fill((10, 100, 160))

    platforms_only = [[0 for __ in range(sizes[0])] for _ in range(sizes[1])]
    for x in range(sizes[0]):
        for y in range(sizes[1]):
            if gamemap.map[y][x] == 1:
                platforms_only[y][x] = 1
            else:
                platforms_only[y][x] = 0
    for x in range(sizes[0]):
        for y in range(sizes[1]):
            if gamemap.map[y][x] == 1:
                surface.blit(get_sprite(x, y, platforms_only, sizes), (x * 32, y * 32))
            if gamemap.map[y][x] == 2:
                surface.blit(config.get("thorns.png"), (x * 32, y * 32))
    return surface


def draw_background_for_map(gamemap: gmap.Map) -> Tuple[pygame.Surface, pygame.Surface, Tuple[int, int], pygame.Rect]:
    """
    Отрисовывает тёмный задний фон и рассчитывает где надо отрисовать изображение карты

    :param gamemap: игровая карта
    :return: карта, отрисованная на чёрном фоне; отрисованная карта; позиция отрисовки; Rect карты
    """
    surface = pygame.Surface((1280, 720))
    surface.fill((20, 20, 20))
    sizes = gamemap.get_sizes()
    width = sizes[0]*32
    x = (1280 - width)//2 - 1
    height = sizes[1]*32
    y = (720 - height)//2 - 1
    rendered_map = map_surface(gamemap)
    surface.blit(rendered_map, (x, y))
    return surface, rendered_map, (x, y), pygame.Rect(x, y, width, height)

def draw_background_for_replay(gamemap: gmap.Map) -> pygame.Surface:
    """
    Отрисовывает карту для воспроизведения

    :param gamemap: игровая карта, сохранённая в повторе
    :return: отрисованная карта
    """
    if not isinstance(gamemap, gmap.Map):
        raise TypeError
    surface = pygame.Surface((1280, 720))
    surface.fill((20, 20, 20))
    surf = pygame.Surface((gamemap.rect.width, gamemap.rect.height))
    surf.fill((10, 100, 160))
    surface.blit(surf, gamemap.rect)
    platforms_only = [[0 for __ in range(gamemap.sizes['x'])] for _ in range(gamemap.sizes['y'])]
    for platform in gamemap.platforms:
        x = (platform.rect.left - gamemap.rect.left)//32
        for _ in range(platform.rect.left, platform.rect.right-1, 32):
            y = (platform.rect.top - gamemap.rect.top)//32
            for __ in range(platform.rect.top, platform.rect.bottom-1, 32):
                platforms_only[y][x] = 1
                y += 1
            x += 1
    for x in range(gamemap.sizes['x']):
        for y in range(gamemap.sizes['y']):
            if platforms_only[y][x] == 1:
                surface.blit(get_sprite(x, y, platforms_only, (gamemap.sizes['x'], gamemap.sizes['y'])),
                             (x * 32 + gamemap.rect.left, y * 32 + gamemap.rect.top))
    for thorn in gamemap.thorns:
        surface.blit(config.get("thorns.png"), thorn.rect)
    return surface
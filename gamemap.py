"""Игровая карта"""
from typing import Tuple

import pygame


class Map:
    """
        Игровая карта

        :ivar name: названия карты
        :type name: Dict[str, str]
        :ivar rect: размеры карты на экране
        :type rect: pygame.Rect
        :ivar sizes: размеры карты
        :type sizes: Dict[str, int]
        :ivar platforms: список платформ для перемещения
        :type platforms: List[Platform]
        :ivar thorns: список опасных шипов
        :type thorns: List[Platform]
        :ivar flags: флаги
        :type flags: Dict[str, Tuple[int, int]]
        :ivar map: матрица карты
        :type map: List[List[int]]
    """
    def __init__(self, **data):
        """
        Создаёт новый экземпляр карты по переданным данным

        :param data: данные для воссоздания карты
        :keyword replay: индикатор того, что карта воспроизводится из записи, а не из файла карты
        """
        if data.get('replay', False):
            self.name = {"ru": "", "en": ""}
            self.rect = pygame.Rect(*data['rect'])
            self.sizes = {"x": self.rect.width//32, "y": self.rect.height//32}
            self.platforms = []
            for platform in data['platforms']:
                self.platforms.append(Platform(replay=True, rect=platform))
            self.thorns = []
            for thorn in data['thorns']:
                self.thorns.append(Platform(replay=True, rect=thorn))
        else:
            self.name = {}
            for obj in data["name"]:
                for lang in obj:
                    self.name[lang] = obj[lang]
            self.sizes = {}
            for obj in data["sizes"]:
                for size in obj:
                    self.sizes[size] = obj[size]
            self.map = [[0 for __ in range(self.sizes['x'])] for _ in range(self.sizes['y'])]
            self.platforms = []
            for platform in data.get('platforms', []):
                plat = Platform(**platform, map_y=self.sizes['y'])
                for x in plat.get_x_range():
                    for y in plat.get_y_range_for_map(self):
                        self.map[y][x] = 1
                self.platforms.append(plat)
            self.thorns = []
            for thorns in data.get('thorns', []):
                self.map[self.sizes['y'] - thorns['y']][thorns['x'] - 1] = 2
                self.thorns.append(Platform(**thorns, map_y=self.sizes['y']))
            self.flags = {}
            for flag in data['flags']:
                color, x, y = flag['color'], flag['x'] - 1, self.sizes['y'] -  flag['y']
                self.map[y][x] = 3
                self.flags[color] = (x, y)

    def get_sizes(self) -> Tuple[int, int]:
        """
        Возвращает размеры карты (в ячейках) в виде кортежа

        :return: размеры карты
        """
        return self.sizes['x'], self.sizes['y']


class Platform:
    """
    Статичные объекты на карте

    :ivar rect: хитбокс объекта
    :type rect: pygame.Rect
    :ivar x: 'x'-координата объекта
    :type x: int
    :ivar y: 'y'-координата объекта
    :type y: int
    :ivar w: ширина
    :type w: int
    :ivar h: высота объекта
    :type h: int
    """
    def __init__(self, **kwargs):
        if kwargs.get('replay', False):
            self.rect = pygame.Rect(*kwargs['rect'])
        else:
            self.x = kwargs['x'] - 1
            self.y = kwargs['y'] - 1
            self.w = kwargs.get('w', 1)
            self.h = kwargs.get('h', 1)
            map_y = kwargs['map_y']
            self.rect = pygame.Rect(32*self.x, 32*(map_y - self.y - self.h), 32*self.w, 32*self.h)

    def get_x_range(self) -> range:
        """
        Возвращает диапазон от начала 'x'-координат до конца объекта

        :return: диапазон (x, x+w)
        """
        return range(self.x, self.x + self.w)

    def get_y_range(self) -> range:
        """
            Возвращает диапазон от начала 'y'-координат до конца объекта

            :return: диапазон (y, y+h)
        """
        return range(self.y, self.y + self.h)

    def get_y_range_for_map(self, gmap: Map) -> range:
        """
            Возвращает диапазон от начала 'y'-координат до конца объекта для карты (разные системы координат)

            :param gmap: игровая карта
            :return: диапазон (map_y - y - h, map_y - y)
        """
        return range(gmap.sizes['y'] - self.y - self.h, gmap.sizes['y'] - self.y)
import pygame

import gamemap
import rendermap as renderer
from player import Player


class Core:
    def __init__(self):
        self.map = None
        self.collides = []
        self.thorns = []
        self.teams = {
            "red": Team(Player("red"), None),
            "blue": Team(Player("blue"), None)
        }
        self.is_game = False
        self.winner = None

    def start_game(self):
        """
        Инициирует начало игры

        :raises ValueError: если к началу игры карта не была выбрана
        :return: данные по отрисовке заднего фона
        :rtype: tuple
        """
        if self.map is None:
            raise ValueError
        background = renderer.draw_background_for_map(self.map)
        for platform in self.collides:
            platform.move_ip(background[2])
        for thorn in self.thorns:
            thorn.move_ip(background[2])
        for team_name in self.teams:
            team = self.teams[team_name]
            team.flag.shift(background[2])
            x, y = team.flag.get_init_cords()
            team.player.spawn(spawn_x=x, spawn_y=y-64)
        self.is_game = True
        return background

    def set_map(self, gmap: gamemap.Map):
        """
        Устанавливает карту игры

        :param gmap: игровая карта (класс gamemap.Map)
        :raises TypeError: если был передан не объект gamemap.Map
        """
        if not isinstance(gmap, gamemap.Map):
            raise TypeError
        self.map = gmap
        for platform in gmap.platforms:
            self.collides.append(platform.rect)
        for thorn in gmap.thorns:
            self.thorns.append(thorn.rect)
        for flag in gmap.flags:
            res = gmap.flags[flag]
            self.teams[flag].flag = Flag(res[0]*32, 32*res[1], flag)


class Team:
    def __init__(self, player:Player, flag):
        self.player = player
        self.flag = flag


class Flag:
    def __init__(self, x, y, color):
        """
        Создаёт объект флага по координатам карты

        :param x: x-координата 'ячейки' в которой находится флаг
        :param y: y-координата 'ячейки' в которой находится флаг
        """
        self.color = color
        self.init_x, self.init_y = x, y - 16
        self.rect = pygame.Rect(x + 8, y - 16, 16, 48)
        self.sprite = pygame.Surface((16, 48))
        self.sprite.fill((255, 0, 0) if color == "red" else (0, 0, 255))
        self.is_carried = False

    def shift(self, offset):
        self.init_x += offset[0]
        self.init_y += offset[1]
        self.rect.move_ip(*offset)

    def get_init_cords(self) -> tuple:
        """
        Возвращает координаты флага

        :return: координаты на экране
        :rtype: tuple
        """
        return self.init_x, self.init_y

    def render_at(self, screen: pygame.Surface):
        """
        Отрисовывает флаг на переданном экране

        :param screen: элемент на котором нужно отобразить флаг
        :type screen: pygame.Surface

        """
        if not isinstance(screen, pygame.Surface):
            raise TypeError
        if not self.is_carried:
            screen.blit(self.sprite, self.rect)



instance = Core()
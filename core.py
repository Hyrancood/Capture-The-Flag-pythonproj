import gamemap as gmap
import rendermap as renderer
from player import Player
import pygame


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
        if self.map == None:
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

    def set_map(self, gmap: gmap.Map):
        self.map = gmap
        for platform in gmap.platforms:
            self.collides.append(platform.rect)
        for thorn in gmap.thorns:
            self.thorns.append(thorn.rect)
        for flag in gmap.flags:
            res = gmap.flags[flag]
            self.teams[flag].flag = Flag(res[0]*32, 32*res[1], flag)

    def player_collide_with_platforms(self, player):
        collide = player.rect.collidelistall(self.collides)
        if len(collide) > 0:
            pass #TODO: обработка столкновения с платформами

    def player_collide_with_flag(self, player):
        for team_name in self.teams:
            team = self.teams[team_name]
            if team.player != player:
                if team.flag.rect.colliderect(player.rect):
                    pass #TODO: взаимодействие с флагами, подбор флага


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

    def render_at(self, screen):
        if not self.is_carried:
            screen.blit(self.sprite, self.rect)



instance = Core()
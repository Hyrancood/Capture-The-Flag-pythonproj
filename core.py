"""Хранит основную информацию об иге"""
import datetime
import pathlib
from typing import Tuple, List

import pygame

import abilities
import config
import gamemap
import player
import rendermap as renderer
from player import Player


class Core:
    """
    Хранилище данных игры

    :ivar map: игровая карта
    :type map: gamemap.Map
    :ivar collides: список платформ
    :type collides: List[gamemap.Platform]
    :ivar thorns: список шипов
    :type thorns: List[gamemap.Platform]
    :ivar teams: хранилище команд
    :type teams: Dict[str, Team]
    :ivar is_game: идёт ли сейчас игра
    :type is_game: bool
    :ivar should_write_replay: нужно ли записывать текущую игру
    :type should_write_replay: bool
    :ivar replay_file: файл, в который записывается запись игры, если данная функция включена
    :type replay_file: TextIOWrapper
    :ivar winner: победитель текущей игры
    :type winner: Player
    """

    def __init__(self):
        """
        Создание нового экземпляра
        """
        self.map = None
        self.collides = []
        self.thorns = []
        self.teams = {
            "red": Team(Player("red"), None),
            "blue": Team(Player("blue"), None)
        }
        self.is_game = False
        self.should_write_replay = False
        self.replay_file = None
        self.winner = None

    def start_game(self) -> Tuple[pygame.Surface, pygame.Surface, Tuple[int, int], pygame.Rect]:
        """
        Инициирует начало игры

        :raises ValueError: если к началу игры карта не была выбрана
        :return: данные по отрисовке заднего фона
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
            team.player.spawn(spawn_x=x, spawn_y=y - 64)
        self.is_game = True
        if self.should_write_replay:
            folder = pathlib.Path(config.INSTANCE.replays)
            now = datetime.datetime.now()
            time = now.strftime('%y-%m-%d-%H-%M-%S')
            file_name = f"{folder.name}/replay-{time}.rpl"
            i = 1
            while pathlib.Path(file_name).exists():
                file_name = f"{folder.name}/replay-{time}-{i}.rpl"
                i += 1
            self.replay_file = open(file_name, 'w', encoding="UTF-8")
            self.replay_file.writelines([f"{rect_to_str(background[3])}\n",
                                         f"{array_of_rects_to_str(self.collides)}\n",
                                         f"{array_of_rects_to_str(self.thorns)}\n",
                                         f"{team_to_str(self.teams['red'])}\n",
                                         f"{team_to_str(self.teams['blue'])}\n"])
            self.write_frame()
        return background

    def set_winner(self, winner: player.Player):
        """
        Устанавливает победителя и завершает игру

        :param winner: игрок, ставшим победителем
        """
        self.winner = winner
        self.is_game = False
        if self.should_write_replay:
            name = 'Синий' if instance.winner.color == 'blue' else 'Красный'
            self.replay_file.writelines([f"end\n", f"Победитель - {name}"])
            self.replay_file.close()
            self.replay_file = None

    def write_frame(self):
        """
        Записывает текущий фрейм если запись повторов включена
        """
        if self.should_write_replay:
            self.replay_file.writelines([f"{team_in_game_to_str(self.teams['red'])}\n",
                                         f"{team_in_game_to_str(self.teams['blue'])}\n"])

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
            self.teams[flag].flag = Flag(res[0] * 32, 32 * res[1], flag)


class Team:
    """
    Класс команды, хранящий игрока и его флаг

    :ivar player: игрок
    :type player: player.Player
    :ivar flag: флаг
    :type flag: Flag
    """

    def __init__(self, p: Player, flag: "Flag"):
        """
        Создание нового экземпляра команды

        :param p: игрок
        :param flag: флаг
        """
        self.player = p
        self.flag = flag


class Flag:
    """
    Класс флага игрока

    :ivar color: цвет флага ('red' или 'blue')
    :type color: str
    :ivar x: 'x'-кордината флага
    :type x: int
    :ivar y: 'y'-кордината флага
    :type y: int
    :ivar rect: хитбокс флага
    :ivar rect: pygame.Rect
    """

    def __init__(self, x: int, y: int, color: str, rect: pygame.Rect = None):
        """
        Создаёт объект флага по координатам карты

        :param x: x-координата 'ячейки' в которой находится флаг
        :param y: y-координата 'ячейки' в которой находится флаг
        :param color: цвет флага
        :param rect: хитбокс флага
        :raise ValueError: если color не равен 'red' или 'blue'
        """
        if not (color in ('red', 'blue')):
            raise ValueError(f"Flag's color should be 'red' or 'blue', get {color}")
        self.color = color
        if rect is None:
            self.init_x, self.init_y = x, y - 16
            self.rect = pygame.Rect(x + 8, y - 16, 16, 48)
        else:
            self.rect = pygame.Rect(rect)
            self.init_x, self.init_y = rect.left - 8, rect.top
        self.sprite = pygame.Surface((16, 48))
        self.sprite.fill((255, 0, 0) if color == "red" else (0, 0, 255))
        self.is_carried = False

    def shift(self, offset: Tuple[int, int]):
        """
        Смещает флаг на указанное расстояние

        :param offset: (x, y) вектор смещения флага
        """
        self.init_x += offset[0]
        self.init_y += offset[1]
        self.rect.move_ip(*offset)

    def get_init_cords(self) -> Tuple[int, int]:
        """
        Возвращает координаты флага

        :return: координаты на экране
        """
        return self.init_x, self.init_y

    def render_at(self, screen: pygame.Surface):
        """
        Отрисовывает флаг на переданном экране

        :param screen: элемент на котором нужно отобразить флаг
        :type screen: pygame.Surface
        :raise TypeError: если screen не является pygame.Surfaces
        """
        if not isinstance(screen, pygame.Surface):
            raise TypeError
        if not self.is_carried:
            screen.blit(self.sprite, self.rect)


instance = Core()
"""Экземпляр текущей игры"""


def array_of_rects_to_str(rects_list: List[pygame.Rect]) -> str:
    """
    Сереализует список Rect'ов в строку

    :param rects_list: список для сериализации
    :return: сериализованный список
    """
    result = ""
    for rect in rects_list:
        result += rect_to_str(rect) + ";"
    return result[:-1]


def str_to_array_of_rects(string: str) -> List[pygame.Rect]:
    """
    Десерилизует список Rect'ов из строки

    :param string: сериализованный список
    :return: список Rect'ов
    :raise TypeError: если была передана не строка
    """
    if not isinstance(string, str):
        raise TypeError
    return [str_to_rect(rect) for rect in string.split(";")]


def rect_to_str(rect: pygame.Rect) -> str:
    """
    Сериализует Rect в строку

    :param rect: Rect для сериализации
    :return: итог сериализации
    :raise TypeError: если был передан не Rect
    """
    if not isinstance(rect, pygame.Rect):
        raise TypeError
    return f"{rect.left},{rect.top},{rect.width},{rect.height}"


def str_to_rect(string: str) -> pygame.Rect:
    """
    Десериализует строку в Rect

    :param string: сериализованный Rect
    :return: десериализованный Rect
    :raise TypeError: если была передана не строка
    :raises ValueError:
        если был передан не сериализованный Rect вида 'int,int,int,int'
    """
    if not isinstance(string, str):
        raise TypeError
    if string.count(',') != 3:
        raise ValueError
    else:
        for x in string.split(','):
            try:
                int(x)
            except TypeError:
                raise ValueError
    return pygame.Rect(*map(int, string.split(',')))


def team_to_str(team: "Team") -> str:
    """
    Сериализует команду

    :param team: команда для сериализации
    :return: итог сериализации
    :raise TypeError: если был передан не Team
    """
    if not isinstance(team, Team):
        raise TypeError
    return f"{rect_to_str(team.flag.rect)}-{rect_to_str(team.player.rect)}-{player_abilities_to_str(team.player)}"


def str_to_team(string: str, color: str) -> Team:
    """
    Десериализует строку в команду

    :param string: сериализованная команда
    :param color: цвет команды
    :return: десериализованная команда
    :raise TypeError: если 'color' или 'string' не являются строками
    :raise ValueError: если 'color' отличается от 'red' и 'blue'
    """
    if not isinstance(string, str):
        raise TypeError
    if not isinstance(color, str):
        raise TypeError
    if not (color == "red" or color == "blue"):
        raise ValueError
    flag_rect, player_rect, player_abilities = string.split("-")
    p = Player(color)
    p.rect = str_to_rect(player_rect)
    p.set_abilities(str_to_player_abilities(player_abilities))
    flag = Flag(0, 0, color, str_to_rect(flag_rect))
    return Team(p, flag)


def player_abilities_to_str(p: player.Player) -> str:
    """
    Сериализует способности игрока

    :param p: игрок, чьи способности надо сериализовать
    :return: итог сериализации
    :raise TypeError: если 'p' не является объектом класса player.Player
    """
    if not isinstance(p, player.Player):
        raise TypeError
    result = ""
    for button in p.ability_buttons.values():
        ability = button.ability
        if ability is not None:
            result += f"{ability.sprite_id},{ability.cooldown},{ability.ticks};"
    return result[:-1]


def str_to_player_abilities(string: str) -> List[abilities.Ability | None]:
    """
    Десериализует способности игрока из строки

    :param string: сериализованные способности
    :return: список способностей игрока
    :raise TypeError: если была переданна не строка
    """
    if not isinstance(string, str):
        raise TypeError
    return [str_to_ability(ability) for ability in string.split(";")]


def str_to_ability(string: str) -> abilities.Ability:
    """
    Десериализует способность игрока из строки

    :param string: сериализованная способность
    :return: итог десериализации
    :raise TypeError: если была передана не строка
    """
    if not isinstance(string, str):
        raise TypeError
    if string == "":
        return None
    sprite_id, cooldown, ticks = map(int, string.split(","))
    ability = abilities.Ability(sprite_id, cooldown, 0)
    ability.ticks = ticks
    return ability


def team_in_game_to_str(team: "Team"):
    """
    Скриализует игровое состояние команды в строку

    :param team: команда для сериализации
    :return: итог сериализации
    :raise TypeError: если был передан объект класса Team
    """
    if not isinstance(team, Team):
        raise TypeError
    return f"{team.flag.is_carried}-{team.player.dead}-{team.player.carried_flag is not None}-{rect_to_str(team.player.rect)}-{player_abilities_to_str(team.player)}"


def str_to_team_in_game(string: str, team: "Team"):
    """
    Десериализует игровое состояние команду из строки

    :param string: сериализованное состояние
    :param team: команда, на которую будет применяться изменения
    :raises TypeError:
        если переданная 'string' не является строкой
        если переданная 'team' не является объектом Team
    """
    if not isinstance(string, str):
        raise TypeError
    if not isinstance(team, Team):
        raise TypeError
    flag_is_carried, dead, carry_flag, player_rect, player_abilities = string.split("-")
    team.flag.is_carried = flag_is_carried == "True"
    team.player.rect = str_to_rect(player_rect)
    team.player.dead = int(dead)
    team.player.carried_flag = None if carry_flag == "False" else instance.teams[
        "red" if team.player.color == "blue" else "blue"].flag
    team.player.set_abilities(str_to_player_abilities(player_abilities))

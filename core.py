import datetime
import pathlib

import pygame

import abilities
import config
import gamemap
import player
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
        self.should_write_replay = True
        self.replay_file = None
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
        self.winner = winner
        self.is_game = False
        if self.should_write_replay:
            name = 'Синий' if instance.winner.color == 'blue' else 'Красный'
            self.replay_file.writelines([f"end\n", f"Победитель - {name}"])
            self.replay_file.close()
            self.replay_file = None

    def write_frame(self):
        if not self.should_write_replay:
            return
        self.replay_file.writelines([f"{team_in_game_to_str(self.teams['red'])}\n",
                                     f"{team_in_game_to_str(self.teams['blue'])}\n"])
        pass

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
    def __init__(self, x: int, y: int, color: str, rect: pygame.Rect =None):
        """
        Создаёт объект флага по координатам карты

        :param x: x-координата 'ячейки' в которой находится флаг
        :param y: y-координата 'ячейки' в которой находится флаг
        """
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


def array_of_rects_to_str(rects_list: list):
    result = ""
    for rect in rects_list:
        result += rect_to_str(rect) + ";"
    return result[:-1]

def str_to_array_of_rects(string: str):
    if not isinstance(string, str):
        raise TypeError
    return [str_to_rect(rect) for rect in string.split(";")]

def rect_to_str(rect: pygame.Rect):
    if not isinstance(rect, pygame.Rect):
        raise TypeError
    return f"{rect.left},{rect.top},{rect.width},{rect.height}"

def str_to_rect(string: str):
    if not isinstance(string, str):
        raise TypeError
    if string.count(',')!=3:
        raise ValueError
    else:
        for x in string.split(','):
            try:
                _ = int(x)
            except TypeError:
                raise ValueError
    return pygame.Rect(*map(int, string.split(',')))

def team_to_str(team: "Team"):
    if not isinstance(team, Team):
        raise TypeError
    return f"{rect_to_str(team.flag.rect)}-{rect_to_str(team.player.rect)}-{player_abilities_to_str(team.player)}"

def str_to_team(string: str, color: str):
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

def player_abilities_to_str(p: player.Player):
    if not isinstance(p, player.Player):
        raise TypeError
    result = ""
    for button in p.ability_buttons.values():
        ability = button.ability
        if ability is not None:
            result += f"{ability.sprite_id},{ability.cooldown},{ability.ticks};"
    return result[:-1]

def str_to_player_abilities(string: str):
    if not isinstance(string, str):
        raise TypeError
    return [str_to_ability(ability)[0] for ability in string.split(";")]

def str_to_ability(string: str):
    if not isinstance(string, str):
        raise TypeError
    if string == "":
        return None, None
    sprite_id, cooldown, ticks = map(int, string.split(","))
    ability = abilities.Ability(sprite_id, cooldown, 0)
    ability.ticks = ticks
    return ability, ticks

def team_in_game_to_str(team: "Team"):
    if not isinstance(team, Team):
        raise TypeError
    return f"{team.flag.is_carried}-{team.player.dead}-{team.player.carried_flag is not None}-{rect_to_str(team.player.rect)}-{player_abilities_to_str(team.player)}"

def str_to_team_in_game(string: str, team: "Team"):
    if not isinstance(string, str):
        raise TypeError
    if not isinstance(team, Team):
        raise TypeError
    flag_is_carried, dead, carry_flag, player_rect, player_abilities = string.split("-")
    team.flag.is_carried = flag_is_carried == "True"
    team.player.rect = str_to_rect(player_rect)
    team.player.dead = int(dead)
    team.player.carried_flag = None if carry_flag == "False" else instance.teams["red" if team.player.color == "blue" else "blue"].flag
    team.player.set_abilities(str_to_player_abilities(player_abilities))

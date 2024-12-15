import pathlib
import re
import subprocess

import pygame

import config
import core
import gamemap
import rendermap

FILES = None
REPLAY_FILE = None
BACKGROUND = None
REPLAY = True
INDEX = 0
BUTTON = 1
CAN_RUN = False

def start_replay(file_path: str, **kwargs):
    global REPLAY_FILE, BACKGROUND, REPLAY
    REPLAY_FILE = open(file_path, 'r', encoding="UTF-8")
    BACKGROUND = core.str_to_rect(REPLAY_FILE.readline().strip())
    platforms = core.str_to_array_of_rects(REPLAY_FILE.readline().strip())
    thorns = core.str_to_array_of_rects(REPLAY_FILE.readline().strip())
    core.instance.teams = {
        "red": core.str_to_team(REPLAY_FILE.readline().strip(), "red"),
        "blue": core.str_to_team(REPLAY_FILE.readline().strip(), "blue")
    }
    gmap = gamemap.Map(replay=True, rect=BACKGROUND, platforms=platforms, thorns=thorns)
    BACKGROUND = (rendermap.draw_background_for_replay(gmap), BACKGROUND)
    for team in core.instance.teams.values():
        x, y = team.flag.get_init_cords()
        team.player.spawn(spawn_x=x, spawn_y=y - 64)
    kwargs['screen'].blit(BACKGROUND[0], (0, 0))
    pygame.display.flip()


def draw_frame(**kwargs):
    global REPLAY_FILE, BACKGROUND, REPLAY
    if REPLAY_FILE is None:
        raise ValueError
    screen = kwargs['screen']
    screen.blit(BACKGROUND[0], (0, 0))
    for team_name in ('red', 'blue'):
        line = REPLAY_FILE.readline().strip()
        if line == "":
            REPLAY_FILE = None
            return "MAIN"
        if line == "end":
            font = pygame.font.SysFont("Comic Sans MS", 80)
            screen.blit(font.render(REPLAY_FILE.readline().strip(), False,
                                              (255, 255, 255)), (220, 300))
            pygame.display.flip()
            REPLAY = False
            return "REPLAYS"
        while line.startswith("draw-"):
            rect, color = line[5:].split("-")
            rect, color = core.str_to_rect(rect), tuple(map(int, color.split(",")))
            surf = pygame.Surface((rect.width, rect.height))
            surf.fill(color)
            screen.blit(surf, rect)
            line = REPLAY_FILE.readline().strip()
        core.str_to_team_in_game(line, core.instance.teams[team_name])
        flag = core.instance.teams[team_name].flag
        p = core.instance.teams[team_name].player
        if p.is_dead():
            p.drawn_respawn_time_on_screen(screen, kwargs['font'])
        else:
            p.blit_on_screen(screen)
        p.update_abilities(**kwargs, area=BACKGROUND[1])
        if not flag.is_carried:
            flag.render_at(screen)

def open_replays_folder():
    subprocess.Popen(f'explorer "{pathlib.Path(config.INSTANCE.replays).absolute().name}"')

def updates_files():
    global FILES, CAN_RUN, INDEX
    FILES = []
    for file in pathlib.Path(config.INSTANCE.replays).iterdir():
        if re.fullmatch(r"replay-\d\d-\d\d-\d\d-\d\d-\d\d-\d\d.rpl", file.name):
            date = file.name[7:24]
            year, month, day, hour, minute, second = date.split('-')
            FILES.append((file, f"Запись от {day}/{month}/{year} в {hour}:{minute}:{second}", date))
    FILES.sort(key=lambda f: f[2], reverse=True)
    FILES = FILES[:4]
    CAN_RUN = len(FILES) > 0
    INDEX = 0


def choose_file(**kwargs):
    global FILES
    if FILES is None:
        updates_files()
    print(FILES)
    for event in kwargs['events']:
        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                return None
    return None

def draw_replay(screen: pygame.Surface, index: int, y: int, chosen: bool=False):
    global FILES
    if index >= len(FILES):
        raise ValueError
    btn = config.get("map_choose_button.png").copy()
    btn.set_alpha(255 if chosen else 100)
    screen.blit(btn, (115, y))
    font = pygame.font.SysFont("Comic Sans MS", 48)
    file = FILES[index]
    screen.blit(font.render(file[1], False, (0, 0, 0)), (165, y + 18))

def draw_button(screen: pygame.Surface, asset: str, index: int, x: int):
    global BUTTON
    surface = config.get(asset).copy()
    surface.set_alpha(255 if index == BUTTON else 150)
    screen.blit(surface, (x, 619))

def run(**kwargs):
    global REPLAY_FILE, BACKGROUND, REPLAY, INDEX, FILES, BUTTON, CAN_RUN
    screen = kwargs['screen']
    if REPLAY_FILE is None:
        screen.blit(config.get("maps_menu_bg.png"), (0, 0))
        if FILES is None:
            updates_files()
        y = 51
        for i in range(len(FILES)):
            draw_replay(screen, i, y, INDEX == i)
            y += 134
        draw_button(screen,"open_maps_folder.png", 0, 115)
        draw_button(screen, "maps_menu_play_button.png", 1, 382)
        draw_button(screen, "reload_maps_button.png", 2, 1084)
        pygame.display.flip()
    for event in kwargs['events']:
        if event.type == pygame.KEYDOWN:
            if event.key == 27 or (event.key == 13 and not REPLAY and REPLAY_FILE is not None):
                REPLAY_FILE = None
                REPLAY = True
                return "MAIN"
            if REPLAY_FILE is None:
                if event.key in (115, 1073741905) and FILES is not None:
                    INDEX = min(len(FILES) - 1, INDEX + 1)
                if event.key in (119, 1073741906) and FILES is not None:
                    INDEX = max(0, INDEX - 1)
                if event.key in (97, 1073741904):
                    BUTTON = max(0, BUTTON - 1) if CAN_RUN else 0
                if event.key in (100, 1073741903):
                    BUTTON = min(2, BUTTON + 1) if CAN_RUN else 2
                if event.key == 13:
                    if BUTTON == 0:
                        open_replays_folder()
                    elif BUTTON == 1 and CAN_RUN:
                        start_replay(FILES[INDEX][0], **kwargs)
                    else:
                        BUTTON = 2
                        updates_files()

    if REPLAY_FILE is not None and REPLAY:
        draw_frame(**kwargs)
        pygame.display.update(BACKGROUND[1])
    elif not REPLAY:
        kwargs["clock"].tick(2)
        return "REPLAYS"
    kwargs["clock"].tick(60)
    return "REPLAYS"
import pathlib

import pygame

import config
import core
import gamemap
import rendermap

REPLAY_FILE = None
BACKGROUND = None
REPLAY = True

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

def run(**kwargs):
    global REPLAY_FILE, BACKGROUND, REPLAY
    if REPLAY_FILE is None:
        name = None
        for path in pathlib.Path(config.INSTANCE.replays).iterdir():
            if name is None or name > path.name:
                name = f"{config.INSTANCE.replays}/{path.name}"
        if name is None:
            return "MAIN"
        start_replay(name, **kwargs)
    for event in kwargs['events']:
        if event.type == pygame.KEYDOWN:
            if event.key == 27 or (event.key == 13 and not REPLAY):
                REPLAY_FILE = None
                REPLAY = True
                return "MAIN"
    if not REPLAY:
        kwargs["clock"].tick(2)
        return "REPLAYS"
    draw_frame(**kwargs)
    pygame.display.update(BACKGROUND[1])
    kwargs["clock"].tick(60)
    return "REPLAYS"
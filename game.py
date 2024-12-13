import pygame
from PIL.ImageChops import screen

import core
import gamemap as gmap
import player
from core import instance


BG = None


def awards(**kwargs):
    font = pygame.font.SysFont("Comic Sans MS", 80)
    screen = kwargs['screen']
    name = 'Синий' if core.instance.winner.color == 'blue' else 'Красный'
    screen.blit(font.render(f"Победитель - {name}",
                            False, (255, 255, 255)), (220, 300))
    for event in kwargs['events']:
        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                core.instance = core.Core()
                return "MAIN"
    pygame.display.flip()

def game(**kwargs):
    global BG
    screen = kwargs["screen"]  # Surface
    if not core.instance.is_game:
        BG = core.instance.start_game()
        screen.blit(BG[0], (0, 0))
        pygame.display.flip()

    screen.blit(BG[1], BG[2])
    for platform in core.instance.collides:
        surf = pygame.Surface((platform.width, platform.height))
        surf.fill((255, 0, 128))
        surf.set_alpha(200)
        screen.blit(surf, platform)
    for team_name in core.instance.teams:
        team = core.instance.teams[team_name]
        team.player.update(**kwargs,
                           platforms=core.instance.collides,
                           teams=core.instance.teams,
                           thorns=core.instance.thorns,
                           area=BG[3])
        team.flag.render_at(screen)
        if team.player.winner:
            core.instance.winner = team.player
    pygame.display.update(BG[3])


def run(**kwargs):
    if core.instance.winner is None:
        game(**kwargs)
    else:
        if awards(**kwargs) is not None:
            return "MAIN"
    kwargs["clock"].tick(60)
    return "GAME"
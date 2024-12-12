import pygame
import core
import gamemap as gmap
import player
from core import instance


BG = None


def run(**kwargs):
    global BG
    screen = kwargs["screen"] #Surface
    if not core.instance.is_game:
        BG = core.instance.start_game()
        screen.blit(BG[0], (0, 0))
        pygame.display.flip()

    screen.blit(BG[1], BG[2])

# platforms' hitboxes
#    for platform in core.instance.collides:
#        surf = pygame.Surface((platform.width, platform.height))
#        surf.fill((255, 0, 128))
#        surf.set_alpha(200)
#        screen.blit(surf, platform)
    for team_name in core.instance.teams:
        team = core.instance.teams[team_name]
        team.flag.render_at(screen)
        #team.player.tick(kwargs)
        team_player_rect = team.player.rect
        surf = pygame.Surface((team_player_rect.width, team_player_rect.height))
        surf.fill((255, 255, 0))
        surf.set_alpha(200)
        screen.blit(surf, team_player_rect)
        team.player.update(**kwargs, platforms=core.instance.collides, teams=core.instance.teams)

    pygame.display.update(BG[3])
    kwargs["clock"].tick(60)
    return "GAME"
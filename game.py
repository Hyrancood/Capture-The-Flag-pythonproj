"""Основная игра"""
import pygame

import core

BG = None
"""Задний фон"""


def awards(**kwargs) -> str:
    """
    Этап 'награждения'

    :param kwargs: данные игры
    :keyword screen: экран
    :return: Следующее окно
    """
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
    pygame.display.update(BG[3])

def game(**kwargs) -> bool:
    """
    Основной этап игры

    :param kwargs: данные игры
    :keyword screen: экран
    :return: закончилась ли игра или нет
    """
    global BG
    screen = kwargs["screen"]  # Surface
    if not core.instance.is_game:
        BG = core.instance.start_game()
        screen.blit(BG[0], (0, 0))
        pygame.display.flip()

    screen.blit(BG[1], BG[2])
    for team_name in core.instance.teams:
        team = core.instance.teams[team_name]
        team.player.update(**kwargs,
                           platforms=core.instance.collides,
                           teams=core.instance.teams,
                           thorns=core.instance.thorns,
                           area=BG[3],
                           replay_file=core.instance.replay_file)
        team.flag.render_at(screen)
        if team.player.winner:
            core.instance.set_winner(team.player)
            pygame.display.update(BG[3])
            return True
    pygame.display.update(BG[3])
    return False


def run(**kwargs):
    if core.instance.winner is None:
        if not game(**kwargs):
            core.instance.write_frame()
    elif awards(**kwargs) is not None:
        return "MAIN"
    kwargs["clock"].tick(60)
    return "GAME"
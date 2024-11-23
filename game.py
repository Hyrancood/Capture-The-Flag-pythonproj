import pygame


def run(**kwargs):
    screen = kwargs["screen"]

    screen.fill("red")
    pygame.display.flip()
    kwargs["clock"].tick(60)
    return "GAME"
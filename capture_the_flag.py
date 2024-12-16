"""Основа игры"""
import argparse
import re

import pygame

import config
import game
import main
import maps
import pregame
import replays

USE = main.run
"""Текущий исполнительный файл"""
MODES = {
    "MAIN": main.run,
    "REPLAYS": replays.run,
    "MAPS": maps.run,
    "PREGAME": pregame.run,
    "GAME": game.run,
}
"""Список всех исполняющих файлов"""

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--path", nargs='?', const=1, type=str,
                            default="paths.config", help="use path file as config")
    args = arg_parser.parse_args()
    path = str(args.path)
    if re.fullmatch("'.*'", path) or re.fullmatch("\".*\"", path):
        path = path[1:-1]
    config.read_config(path)
    pregame.load_assets()
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 36)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        USE = MODES[USE(**{"screen": screen, "clock": clock, "events": events, "font": font})]
    pygame.quit()

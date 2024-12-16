"""Выбор карты для игры"""
import pathlib
import subprocess

import pygame

import config
import core
import gamemap as gmap
import readmap


MAPS = None
"""Доступные для выбора карты"""
NEXT_MODE = {"CHOOSE_MAP": "BUTTONS", "BUTTONS": "CHOOSE_MAP"}
"""Смена режимов"""
MODE = "CHOOSE_MAP"
"""Текущий режим"""
CAN_PLAY = False
"""Можно ли начинать игру"""
index = 0
"""Индекс выбранной карты"""
btn = 1
"""Указатель выбранной кнопки управления"""


def draw_map_button(screen: pygame.Surface, gamemap: gmap.Map, font: pygame.font.Font, y: int, chosen=False):
    """
    Отрисовка кнопки карты

    :param screen: экран
    :param gamemap: игровая карта (уже распаршена из файла)
    :param font: шрифт
    :param y: 'y'-координата для отрисовки
    :param chosen: выбрана ли эта карта
    """
    btn = config.get("map_choose_button.png").copy()
    if not chosen:
        btn.set_alpha(100)
    screen.blit(btn, (115, y))
    lang_y = 13
    for lang in sorted(gamemap.name, reverse=True):
        screen.blit(font.render(gamemap.name[lang], False, (0, 0, 0)), (165, y + lang_y))
        lang_y += 40


def draw_error_button(screen: pygame.Surface, font: pygame.font.Font, filename: str, y: int, chosen=False):
    """
    Отрисовка кнопки не прошедшей валидацию карты

    :param screen: экран
    :param font: шрифт для надписей
    :param filename: название файла
    :param y: 'y'-координата для отрисовки
    :param chosen: выбрана ли эта карта
    """
    btn = config.get("map_choose_error_button.png").copy()
    fnt = font.render(filename, False, (0, 0, 0))
    if not chosen:
        btn.set_alpha(170)
        fnt.set_alpha(170)
    screen.blit(btn, (115, y))
    screen.blit(fnt, (165, y + 13))


def update_maps(screen: pygame.Surface, font: pygame.font.Font):
    """
    Обновляет карты

    :param screen: поверхность для отрисовки кнопок
    :param font: шрифт названий карт
    """
    global MAPS, index, CAN_PLAY
    index = 0
    MAPS = []
    y = 51
    NORMAL = []
    ERROR = []
    for mapfile in pathlib.Path("maps").iterdir():
        if not mapfile.is_file():
            continue
        file = mapfile.name
        if file.strip().split('.')[-1] != "ctfmap":
            continue
        try:
            NORMAL.append((screen, readmap.from_file(mapfile), font))
        except ValueError:
            ERROR.append((screen, font, file))
    i = 0
    for mp in NORMAL:
        if i == 4:
            break
        MAPS.append((True, draw_map_button, (*mp, y)))
        y += 134
        i += 1
    for mp in ERROR:
        if i == 4:
            break
        MAPS.append((False, draw_error_button, (*mp, y)))
        y += 134
        i += 1
    if len(NORMAL) > 0:
        CAN_PLAY = True


def open_maps_folder():
    """Открывает папку с картами через проводник"""
    subprocess.Popen(f'explorer "{pathlib.Path(config.INSTANCE.maps).absolute().name}"')

def display_buttons(screen: pygame.Surface):
    """
    Отрисовывает кнопки на поверхности

    :param screen: экран для отрисовки
    """
    global btn
    BUTTONS = [(config.get("open_maps_folder.png"), 115),
               (config.get("maps_menu_play_button.png"), 382),
               (config.get("reload_maps_button.png"), 1084)]
    for i in (0, 1, 2):
        button = BUTTONS[i]
        if i == btn:
            button[0].set_alpha(255)
        else:
            button[0].set_alpha(150)
        screen.blit(button[0], (button[1], 619))

def run(**kwargs):
    """
    Обработка текущего окна

    :param kwargs: данные игры
    :return: следующее окно
    """
    global MAPS, index, NEXT_MODE, MODE, btn, CAN_PLAY
    screen = kwargs['screen']
    font = kwargs['font']
    screen.blit(config.get("maps_menu_bg.png"), (0, 0))
    if MAPS is None:
        update_maps(screen, font)
    for event in kwargs['events']:
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                return "PREGAME"
            if event.key == 9:
                MODE = NEXT_MODE[MODE]
            if MODE == "CHOOSE_MAP":
                if event.key in (100, 115, 1073741903, 1073741905):
                    index = min(len(MAPS) - 1, index + 1)
                if event.key in (97, 119, 1073741904, 1073741906):
                    index = max(0, index - 1)
                if event.key == 13:
                    MODE = "BUTTONS"
                    if len(MAPS) > 0:
                        if  MAPS[index][0]:
                            btn = 1
                            CAN_PLAY = True
                        else:
                            btn = 0
                            CAN_PLAY = False
                    else:
                        btn = 0
                        CAN_PLAY = False
            elif MODE == "BUTTONS":
                if event.key in (100, 115, 1073741903, 1073741905):
                    btn = min(2, btn + 1)
                    if btn == 1 and not CAN_PLAY:
                        btn = 2
                if event.key in (97, 119, 1073741904, 1073741906):
                    btn = max(0, btn - 1)
                    if btn == 1 and not CAN_PLAY:
                        btn = 0
                if event.key == 13:
                    if btn == 0:
                        open_maps_folder()
                    elif btn == 1 and CAN_PLAY:
                        core.instance.set_map(MAPS[index][2][1])
                        MAPS = None
                        MODE = "CHOOSE_MAP"
                        CAN_PLAY = False
                        return "GAME"
                    elif btn == 2:
                        update_maps(screen, font)
                    else:
                        btn = 0

    for i in range(len(MAPS)):
        map_data = MAPS[i]
        map_data[1](*map_data[2], i == index)
    display_buttons(screen)
    pygame.display.flip()
    return "MAPS"
import pygame
import pathlib, subprocess
import readmap, core
import gamemap as gmap


background = pygame.image.load("assets/maps_menu_bg.png")
map_choose = pygame.image.load("assets/map_choose_button.png")
map_error = pygame.image.load("assets/map_choose_error_button.png")
folder_button = pygame.image.load("assets/open_maps_folder.png")
reload_button = pygame.image.load("assets/reload_maps_button.png")
play_button = pygame.image.load("assets/maps_menu_play_button.png")

MAPS = None
NEXT_MODE = {"CHOOSE_MAP": "BUTTONS", "BUTTONS": "CHOOSE_MAP"}
MODE = "CHOOSE_MAP"
CAN_PLAY = False
index = 0
btn = 1


def draw_map_button(screen: pygame.Surface, gamemap: gmap.Map, font: pygame.font.Font, y: int, chosen=False):
    btn = map_choose.copy()
    if not chosen:
        btn.set_alpha(100)
    screen.blit(btn, (115, y))
    lang_y = 13
    for lang in sorted(gamemap.name, reverse=True):
        screen.blit(font.render(gamemap.name[lang], False, (0, 0, 0)), (165, y + lang_y))
        lang_y += 40


def draw_error_button(screen: pygame.Surface, font: pygame.font.Font, filename: str, y: int, chosen=False):
    btn = map_error.copy()
    fnt = font.render(filename, False, (0, 0, 0))
    if not chosen:
        btn.set_alpha(170)
        fnt.set_alpha(170)
    screen.blit(btn, (115, y))
    screen.blit(fnt, (165, y + 13))


def update_maps(screen: pygame.Surface, font: pygame.font.Font):
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

    for mp in NORMAL:
        MAPS.append((True, draw_map_button, (*mp, y)))
        y += 134
    for mp in ERROR:
        MAPS.append((False, draw_error_button, (*mp, y)))
        y += 134
    if len(NORMAL) > 0:
        CAN_PLAY = True


def open_maps_folder():
    subprocess.Popen(f'explorer "{pathlib.Path("maps").absolute().name}"')

def display_buttons(screen: pygame.Surface):
    global btn
    BUTTONS = [(folder_button, 115), (play_button, 382), (reload_button, 1084)]
    for i in (0, 1, 2):
        button = BUTTONS[i]
        if i == btn:
            button[0].set_alpha(255)
        else:
            button[0].set_alpha(150)
        screen.blit(button[0], (button[1], 619))

# noinspection PyTypeChecker
def run(**kwargs):
    global MAPS, index, NEXT_MODE, MODE, btn, CAN_PLAY
    screen = kwargs['screen']
    font = kwargs['font']
    screen.blit(background, (0, 0))
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
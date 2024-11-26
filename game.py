import pygame
import readmap
import gamemap as gmap


MAP = readmap.from_file("maps/default.ctfmap") #gmap.Map()
PLATFORMS = {
    "ground": pygame.image.load("assets/ground/ground.png"),
    "top": pygame.image.load("assets/ground/top_ground.png"),
    "top-right": pygame.image.load("assets/ground/top_right_ground.png"),
    "right": pygame.image.load("assets/ground/right_ground.png"),
    "bottom-right": pygame.image.load("assets/ground/bottom_right_ground.png"),
    "bottom": pygame.image.load("assets/ground/bottom_ground.png"),
    "bottom-left": pygame.image.load("assets/ground/bottom_left_ground.png"),
    "left": pygame.image.load("assets/ground/left_ground.png"),
    "top-left": pygame.image.load("assets/ground/top_left_ground.png"),
    "top-right-corner": pygame.image.load("assets/ground/top_right_corner_ground.png"),
    "top-left-corner": pygame.image.load("assets/ground/top_left_corner_ground.png"),
    "bottom-right-corner": pygame.image.load("assets/ground/bottom_right_corner_ground.png"),
    "bottom-left-corner": pygame.image.load("assets/ground/bottom_left_corner_ground.png")
}
THORNS = pygame.image.load("assets/thorns.png")
BG = None


def get_sprite(x, y, map_platforms, sizes):
    sprite = PLATFORMS["ground"]
    if y - 1 >= 0 and x + 1 < sizes[0]:
        if map_platforms[y - 1][x] and map_platforms[y][x+1] and not map_platforms[y-1][x+1]:
            return PLATFORMS["top-right-corner"]
    if y - 1 >= 0 and x - 1 >= 0:
        if map_platforms[y - 1][x] and map_platforms[y][x-1] and not map_platforms[y-1][x-1]:
            return PLATFORMS["top-left-corner"]
    if y + 1 < sizes[1] and x + 1 < sizes[0]:
        if map_platforms[y + 1][x] and map_platforms[y][x+1] and not map_platforms[y+1][x+1]:
            return PLATFORMS["bottom-right-corner"]
    if y + 1 < sizes[1] and x - 1 >= 0:
        if map_platforms[y + 1][x] and map_platforms[y][x-1] and not map_platforms[y+1][x-1]:
            return PLATFORMS["bottom-left-corner"]
    if y - 1 >= 0:
        if not map_platforms[y - 1][x]:
            sprite = PLATFORMS["top"]
            if x + 1 < sizes[0]:
                if not map_platforms[y][x + 1]:
                    sprite = PLATFORMS["top-right"]
            if x - 1 >= 0:
                if not map_platforms[y][x - 1]:
                    sprite = PLATFORMS["top-left"]
            return sprite
    if y + 1 < sizes[1]:
        if not map_platforms[y + 1][x]:
            sprite = PLATFORMS["bottom"]
            if x + 1 < sizes[0]:
                if not map_platforms[y][x + 1]:
                    sprite = PLATFORMS["bottom-right"]
            if x - 1 >= 0:
                if not map_platforms[y][x - 1]:
                    sprite = PLATFORMS["bottom-left"]
            return sprite
    if x + 1 < sizes[0]:
        if not map_platforms[y][x+1]:
            sprite = PLATFORMS["right"]
    if x - 1 >= 0:
        if not map_platforms[y][x-1]:
            sprite = PLATFORMS["left"]
    return sprite


def map_surface(gamemap: gmap.Map):
    sizes = gamemap.get_sizes()
    sizes32 = (sizes[0]*32, sizes[1]*32)
    surface = pygame.Surface(sizes32)
    surface.fill((10, 100, 160))

    platforms_only = [[0 for __ in range(sizes[0])] for _ in range(sizes[1])]
    for x in range(sizes[0]):
        for y in range(sizes[1]):
            if gamemap.map[y][x] == 1:
                platforms_only[y][x] = 1
            else:
                platforms_only[y][x] = 0
    for x in range(sizes[0]):
        for y in range(sizes[1]):
            if gamemap.map[y][x] == 1:
                surface.blit(get_sprite(x, y, platforms_only, sizes), (x * 32, y * 32))
            if gamemap.map[y][x] == 2:
                surface.blit(THORNS, (x * 32, y * 32))
    return surface



def draw_background_for_map(gamemap: gmap.Map):
    surface = pygame.Surface((1280, 720))
    surface.fill((20, 20, 20))
    sizes = gamemap.get_sizes()
    x = (1280 - sizes[0]*32)//2 - 1
    y = (720 - sizes[1]*32)//2 - 1
    surface.blit(map_surface(gamemap), (x, y))
    return surface


def run(**kwargs):
    global BG
    screen = kwargs["screen"]
    if BG is None:
        BG = draw_background_for_map(MAP)
    screen.blit(BG, (0,0))

    pygame.display.flip()
    kwargs["clock"].tick(60)
    return "GAME"


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    BG = draw_background_for_map(MAP)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        screen.blit(BG, (0,0))
        pygame.display.flip()
    pygame.quit()
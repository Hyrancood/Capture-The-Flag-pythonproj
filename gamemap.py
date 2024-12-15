import pygame


class Map:
    def __init__(self, **data):
        if data.get('replay', False):
            self.name = {"ru": "", "en": ""}
            self.rect = pygame.Rect(*data['rect'])
            self.sizes = {"x": self.rect.width//32, "y": self.rect.height//32}
            self.platforms = []
            for platform in data['platforms']:
                self.platforms.append(Platform(replay=True, rect=platform))
            self.thorns = []
            for thorn in data['thorns']:
                self.thorns.append(Platform(replay=True, rect=thorn))
        else:
            self.name = {}
            for obj in data["name"]:
                for lang in obj:
                    self.name[lang] = obj[lang]
            self.sizes = {}
            for obj in data["sizes"]:
                for size in obj:
                    self.sizes[size] = obj[size]
            self.map = [[0 for __ in range(self.sizes['x'])] for _ in range(self.sizes['y'])]
            self.platforms = []
            for platform in data.get('platforms', []):
                plat = Platform(**platform, map_y=self.sizes['y'])
                for x in plat.get_x_range():
                    for y in plat.get_y_range_for_map(self):
                        self.map[y][x] = 1
                self.platforms.append(plat)
            self.thorns = []
            for thorns in data.get('thorns', []):
                self.map[self.sizes['y'] - thorns['y']][thorns['x'] - 1] = 2
                self.thorns.append(Platform(**thorns, map_y=self.sizes['y']))
            self.flags = {}
            for flag in data['flags']:
                color, x, y = flag['color'], flag['x'] - 1, self.sizes['y'] -  flag['y']
                self.map[y][x] = 3
                self.flags[color] = (x, y)

    def printmap(self):
        for line in self.map:
            print(*line)

    def get_sizes(self):
        return self.sizes['x'], self.sizes['y']


class Platform:
    def __init__(self, **kwargs):
        if kwargs.get('replay', False):
            self.rect = pygame.Rect(*kwargs['rect'])
        else:
            self.x = kwargs['x'] - 1
            self.y = kwargs['y'] - 1
            self.w = kwargs.get('w', 1)
            self.h = kwargs.get('h', 1)
            map_y = kwargs['map_y']
            self.rect = pygame.Rect(32*self.x, 32*(map_y - self.y - self.h), 32*self.w, 32*self.h)

    def get_x_range(self):
        return range(self.x, self.x + self.w)

    def get_y_range(self):
        return range(self.y, self.y + self.h)

    def get_y_range_for_map(self, gmap: Map):
        return range(gmap.sizes['y'] - self.y - self.h, gmap.sizes['y'] - self.y)
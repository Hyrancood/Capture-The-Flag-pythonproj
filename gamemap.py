import pygame


class Map:
    def __init__(self, data):
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
            plat = Platform(**platform, map_y=self.sizes[1])
            for x in plat.get_x_range():
                for y in plat.get_y_range_for_map(self.sizes['y']):
                    self.map[y][x] = 1
            self.platforms.append(plat)
        for thorns in data.get('thorns', []):
            self.map[self.sizes['y'] - thorns['y']][thorns['x'] - 1] = 2
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

    def get_y_range_for_map(self, map_y):
        return range(map_y - self.y - self.h, map_y - self.y)
from pygame.sprite import collide_circle

import gamemap as gmap


class Core:
    def __init__(self):
        self.blue_player = None
        self.red_player = None
        self.map = None
        self.collides = []

    def set_map(self, gmap: gmap.Map):
        self.map = gmap
        for platform in gmap.platforms:
            self.collides.append(platform.get_rect_for_map(gmap.sizes[1]))

    def player_collide_with_platforms(self, player):
        collide = player.rect.collidelistall(self.collides)
        if len(collide) > 0:
            pass


instance = Core()
import vector
import pygame

G_ACCELERATION = 0.2
DASH_POWER = 7
DASH_COOLDOWN = 60*7 #60 fps
DASH_DURATION = 14 #frames


class Player:
    def __init__(self,chosen_color):
        self.color=chosen_color
        self.in_air=0
        self.dash = 0
        if self.color=='red':
            self.movement_buttons = {1073741903:'right', 1073741904:'left', 1073741906:'up', 1073741905: "dash"}
        else:
            self.movement_buttons = {100:'right', 97:'left', 119:'up', 115: "dash"}
        self.rect=pygame.Rect(0,0,32,64)
        self.first_ability=None
        self.second_ability=None
        self.speed=3.7
        self.velocity=vector.Vector()

    def set_abilities(self,abilities):
        for i1 in range(len(abilities)):
            if abilities[i1] == 1:
                self.first_ability=i1
                for i2 in range(i1+1,len(abilities)):
                    if abilities[i2] == 1:
                        self.second_ability=i2

    def set_position(self,x_set,y_set):
        self.rect.move(x_set, y_set)

    def opposite(self, teams):
        return teams['blue'].player if self.color=='red' else teams['red'].player

    def is_on_ground(self, platforms):
        test_pos = [self.rect.bottomleft, self.rect.midbottom, self.rect.bottomright]
        return any(any(platform.collidepoint((pos[0], pos[1]+1)) for pos in test_pos) for platform in platforms)

    def is_standing_on_other_player(self, other: "Player"):
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(0, 1)
        return not self.rect.colliderect(other.rect) and player_rect.colliderect(other.rect)

    def is_in_dash(self):
        return abs(self.dash) > DASH_COOLDOWN - DASH_DURATION

    def update(self,**kwargs):
        #self.handle_events(kwargs['events'])
        self.handle_movement(**kwargs)

    def calculate_velocity(self, **kwargs):
        on_ground = (self.is_on_ground(kwargs['platforms']) or
                     self.is_standing_on_other_player(self.opposite(kwargs['teams'])))
        if not on_ground:
            self.velocity.y += G_ACCELERATION
        else:
            self.velocity.y = 0
        for event in kwargs['events']:
            if event.type == pygame.KEYDOWN:
                key = self.movement_buttons.get(event.key)
                if key == 'right':
                    self.velocity.x += self.speed
                if key == 'left':
                    self.velocity.x -= self.speed
                if key == 'up' and on_ground:
                    self.velocity.y -= self.speed * 2.3
                if key == "dash" and self.velocity.x != 0 and self.dash == 0:
                    mode = 1 if self.velocity.x > 0 else -1
                    self.velocity.x += self.speed * DASH_POWER * mode
                    self.dash = DASH_COOLDOWN * mode
            if event.type == pygame.KEYUP:
                if self.movement_buttons.get(event.key) == 'right':
                    self.velocity.x -= self.speed
                if self.movement_buttons.get(event.key) == 'left':
                    self.velocity.x += self.speed
        if self.dash != 0:
            mode = 1 if self.dash > 0 else -1
            if self.is_in_dash():
                self.velocity.x -= mode * self.speed * (DASH_POWER / DASH_DURATION)
            self.dash -= mode

    def handle_movement(self, **kwargs):
        self.calculate_velocity(**kwargs)
        self.handle_collisions_with_platforms(**kwargs)
        self.handle_collision_with_other_player(self.opposite(kwargs['teams']))
        self.handle_collision_with_enemy_flag(**kwargs)
        #self.rect.move_ip(self.velocity.x, self.velocity.y)

    def handle_collisions_with_platforms(self, **kwargs):
        pass

    def handle_collision_with_other_player(self, other: "Player"):
        dx, dy = self.velocity.x, self.velocity.y
        if abs(dx) < 0.05:
            dx = 0
        if abs(dy) < 0.05:
            dy = 0
        self.rect.move_ip(0, dy)
        if self.rect.colliderect(other.rect):
            if dy > 0:
                self.rect.bottom = other.rect.top
            if dy < 0:
                self.rect.top = other.rect.bottom
        self.rect.move_ip(dx, 0)
        if self.rect.colliderect(other.rect):
            if dx > 0:
                self.rect.right = other.rect.left
            if dx < 0:
                self.rect.left = other.rect.right

    def handle_collision_with_enemy_flag(self, **kwargs):
        pass

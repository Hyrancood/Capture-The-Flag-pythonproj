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
        self.spawn_point = None
        self.dash = 0
        self.dead = 0
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

    def is_dead(self):
        return self.dead > 0

    def die(self):
        self.dead = 60 * 5

    def blit_on_screen(self, screen):
        surf = pygame.Surface((self.rect.width, self.rect.height))
        surf.fill((255, 255, 0))
        surf.set_alpha(200)
        screen.blit(surf, self.rect)

    def set_position(self,x_set,y_set):
        self.rect.move(x_set, y_set)

    def opposite(self, teams):
        return teams['blue'].player if self.color=='red' else teams['red'].player

    def is_on_ground(self, platforms):
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(0, 1)
        return any(player_rect.colliderect(platform) for platform in platforms)

    def is_standing_on_other_player(self, other: "Player"):
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(0, 1)
        return not self.rect.colliderect(other.rect) and player_rect.colliderect(other.rect)

    def is_in_dash(self):
        return abs(self.dash) > DASH_COOLDOWN - DASH_DURATION

    def spawn(self, **kwargs):
        if self.spawn_point is None:
            self.spawn_point = (kwargs['spawn_x'], kwargs['spawn_y'])
        self.rect = pygame.Rect(self.spawn_point, (32, 64))
        self.velocity=vector.Vector()
        self.dash = 0

    def update(self,**kwargs):
        #self.handle_events(kwargs['events'])
        if self.is_dead():
            self.dead -= 1
            if self.dead == 0:
                self.spawn(**kwargs)
        else:
            self.handle_movement(**kwargs)
            if self.rect.collidelist(kwargs['thorns']) >= 0:
                self.die()
            self.blit_on_screen(kwargs['screen'])

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

    def handle_collision_with_rect(self, dx, dy, rect: pygame.Rect):
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(0, dy)
        if player_rect.colliderect(rect):
            if dy > 0:
                dy -= (player_rect.bottom - rect.top)
                player_rect.bottom = rect.top
            if dy < 0:
                dy += rect.bottom - player_rect.top
                player_rect.top = rect.bottom
        player_rect.move_ip(dx, 0)
        if player_rect.colliderect(rect):
            if dx > 0:
                dx -= (player_rect.right - rect.left)
                player_rect.right = rect.left
            if dx < 0:
                dx += rect.right - player_rect.left
                player_rect.left = rect.right
        return dx, dy

    def handle_collisions_with_platforms(self, **kwargs):
        dx, dy = kwargs['dx'], kwargs['dy']
        for platform in kwargs['platforms']:
            dx, dy = self.handle_collision_with_rect(dx, dy, platform)
        return dx, dy

    def handle_collision_with_other_player(self, dx, dy, other: "Player"):
        if other.is_dead():
            return dx, dy
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(dx, dy)
        if player_rect.colliderect(other.rect) and self.is_in_dash():
            if (not other.is_in_dash()) or (other.is_in_dash() and other.dash < self.dash):
                other.die()
                return dx, dy
        return self.handle_collision_with_rect(dx, dy, other.rect)

    def handle_collision_with_enemy_flag(self, **kwargs):
        dx, dy = kwargs['dx'], kwargs['dy']
        return dx, dy

    def handle_movement(self, **kwargs):
        self.calculate_velocity(**kwargs)
        dx, dy = self.velocity.x, self.velocity.y
        dx, dy = self.handle_collisions_with_platforms(**kwargs, dx=dx, dy=dy)
        dx, dy = self.handle_collision_with_other_player(dx, dy, self.opposite(kwargs['teams']))
        dx, dy = self.handle_collision_with_enemy_flag(**kwargs, dx=dx, dy=dy)
        self.rect.move_ip(dx, dy)
        if dy > self.velocity.y:
            self.velocity.y = 0

import pygame
from vector import Vector


class Ability:
    def __init__(self, cooldown: int, duration: int):
        self.cooldown = cooldown
        self.duration = duration
        self.ticks = 0
        self.owner = None
        self.enemy = None

    def set_player(self, owner, enemy):
        self.owner = owner
        self.enemy = enemy
        self.ticks = 0

    def use(self, **kwargs):
        if self.ticks == 0:
            return True
        return False

    def consume_cooldown(self):
        if self.ticks > 0:
            self.ticks -= 1

class Freeze(Ability):
    def __init__(self):
        super().__init__(660, 180)

    def use(self, **kwargs):
        if super().use(**kwargs):
            owner=self.owner
            enemy=self.enemy
            if owner.distance(enemy) <= 200 and not owner.is_dead() and not enemy.is_dead():
                self.enemy.speed/=2
                self.minus = self.enemy.velocity.x / 2
                self.enemy.velocity.x -= self.minus
                self.ticks = self.cooldown

    def deactivate(self):
        self.enemy.velocity.x += self.minus
        self.enemy.speed *= 2

    def consume_cooldown(self):
        super().consume_cooldown()
        if self.ticks == self.cooldown - self.duration:
            self.deactivate()


class Bomb(Ability):
    def __init__(self):
        super().__init__(900, 0)

    def use(self, **kwargs):
        if super().use(**kwargs):
            owner=self.owner
            enemy=self.enemy
            if owner.distance(enemy) <= 200 and not owner.is_dead() and not enemy.is_dead():
                enemy.die()
                self.ticks = self.cooldown

class Swap(Ability):
    def __init__(self):
        super().__init__(660, 0)

    def use(self, **kwargs):
        if super().use(**kwargs):
            owner = self.owner
            enemy = self.enemy
            if owner.distance(enemy) <= 300 and not owner.is_dead() and not enemy.is_dead():
                owner.rect, enemy.rect = pygame.Rect(enemy.rect), pygame.Rect(owner.rect)
                self.ticks = self.cooldown

class Pulling(Ability):
    def __init__(self):
        super().__init__(720, 10)

    def use(self, **kwargs):
        if super().use(**kwargs):
            self.enemy.unpush_all_movement_buttons()
            self.x = max(-20, min(20, (self.owner.rect.left - self.enemy.rect.left)/self.duration))
            self.y = max(-20, min(20, (self.owner.rect.top - self.enemy.rect.top)/self.duration))
            self.enemy.velocity.x += self.x
            self.enemy.velocity.y += self.y
            self.ticks = self.cooldown

    def deactivate(self):
        self.enemy.velocity.x -= self.x
        self.enemy.velocity.y -= self.y

    def consume_cooldown(self):
        super().consume_cooldown()
        if self.ticks == self.cooldown - self.duration:
            self.deactivate()

class Fireball(Ability):
    def __init__(self):
        super().__init__(600, 180)
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.velocity = Vector()
        self.platforms = []
        self.can_damage = False
        self.surface = None
        self.screen = None
        self.surface = pygame.Surface((24, 24))
        self.surface.fill((255, 64, 64))

    def use(self, **kwargs):
        if super().use(**kwargs):
            self.platforms = kwargs['platforms']
            self.velocity.x = self.owner.velocity.x
            self.velocity.y = self.owner.velocity.y/2
            self.ticks = self.cooldown
            self.can_damage = True
            self.screen = kwargs['screen']
            self.rect = pygame.Rect(self.owner.rect.topleft, (24, 24))
            self.rect.move_ip(4, 4)

    def consume_cooldown(self):
        super().consume_cooldown()
        if (not self.can_damage) or self.ticks == self.cooldown - self.duration:
            self.can_damage = False
            return
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        if self.rect.collidelist(self.platforms) > -1:
            self.can_damage = False
        if self.can_damage:
            self.screen.blit(self.surface, self.rect)
            if self.rect.colliderect(self.enemy):
                self.enemy.die()
                self.can_damage = False
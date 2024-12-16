"""Все игровые способности игроков"""

import pygame

import config
from vector import Vector


class Ability:
    '''
    Класс способностей, является общим родительским классом для классов всех способностей в игре

    :ivar cooldown: продолжительность отката способности в фреймах
    :type cooldown: int
    :ivar duration: продолжительность действия способности в фреймах
    :type duration: int
    :ivar ticks: текущее время до отката способности в фреймах
    :type ticks: int
    :ivar owner: владелец способности
    :type owner: Player
    :ivar enemy: противник владельца способности
    :type enemy: Player
    :ivar sprite_id: номер спрайта способности
    :type sprite_id: int
    '''
    def __init__(self, sprite_id: int, cooldown: int, duration: int):
        '''
        Создание объекта-способности

        :param sprite_id: номер спрайта способности
        :param cooldown: продолжительность отката способности в фреймах
        :param duration: продолжительность действия способности в фреймах
        '''
        self.cooldown = cooldown
        self.duration = duration
        self.ticks = 0
        self.owner = None
        self.enemy = None
        self.sprite_id = sprite_id

    def set_player(self, owner, enemy):
        '''
        Установление игрока, владеющего способностью, а также его противника

        :param owner: владелец способности
        :type owner: Player
        :param enemy: противник владельца способности
        :type enemy: Player
        '''
        self.owner = owner
        self.enemy = enemy
        self.ticks = 0

    def use(self, **kwargs):
        '''
        Определяет, можно ли сейчас использовать способность (перезарядилась ли она)

        :param kwargs: параметры, нужные для использования в некоторых способностях
        :type kwargs: dict
        :return: разрешено ли использование
        :rtype: bool
        '''
        if self.ticks == 0:
            return True
        return False

    def consume_cooldown(self):
        '''
        Уменьшает оставшееся время отката способности
        '''
        if self.ticks > 0:
            self.ticks -= 1

    def blit_on(self, screen: pygame.Surface, map_area: pygame.Rect, x_offset: int):
        '''
        Размещает иконки способностей на экране в зависимости от оставшегося времени их отката

        :param screen: выводимое на экран изображение
        :type screen:  pygame.Surface
        :param map_area: игровая область
        :type map_area: pygame.Rect
        :param x_offset: смещение иконки по оси x
        :type x_offset: int
        '''
        rect = pygame.Rect(0, 0, 64, 64)
        rect.move_ip(map_area.topleft)
        rect.move_ip(x_offset, map_area.height - 80)
        screen.blit(config.get("abilities.png"), rect, area=(self.sprite_id*64, 64, 64, 64))
        percent = int(64*self.ticks/self.cooldown)
        rect.move_ip(0, percent)
        screen.blit(config.get("abilities.png"), rect, area=(self.sprite_id * 64, percent, 64, 64 - percent))

class Freeze(Ability):
    '''
    Способность, позволяющая заморозить противника

    :ivar minus: значение, на которое уменьшается скорость противника при активации
    :type minus: int
    '''
    def __init__(self):
        '''
        Создание объекта, заимствовано у родительского класса
        '''
        super().__init__(0, 660, 180)

    def use(self, **kwargs):
        '''
        "Замораживает" противника в определенном радиусе засчет уменьшения его скорости

        :param kwargs: не используются здесь
        :type kwargs: dict
        '''
        if super().use(**kwargs):
            owner=self.owner
            enemy=self.enemy
            if owner.distance(enemy) <= 200 and not owner.is_dead() and not enemy.is_dead():
                self.enemy.speed/=2
                self.minus = self.enemy.velocity.x / 2
                self.enemy.velocity.x -= self.minus
                self.ticks = self.cooldown

    def deactivate(self):
        '''
        Отмена заморозки, скорость противника становится исходной
        '''
        self.enemy.velocity.x += self.minus
        self.enemy.speed *= 2

    def consume_cooldown(self):
        '''
        Уменьшает время до отката, отменяет эффект способности в нужное время
        '''
        super().consume_cooldown()
        if self.ticks == self.cooldown - self.duration:
            self.deactivate()


class Bomb(Ability):
    '''
    Способность, позволяющая взорвать противника
    '''
    def __init__(self):
        '''
        Создание объекта, заимствовано у родительского класса
        '''
        super().__init__(1, 900, 0)

    def use(self, **kwargs):
        '''
        Убивает противника в определенном радиусе

        :param kwargs: не используется здесь
        :type kwargs: dict
        '''
        if super().use(**kwargs):
            owner=self.owner
            enemy=self.enemy
            if owner.distance(enemy) <= 200 and not owner.is_dead() and not enemy.is_dead():
                enemy.die()
                self.ticks = self.cooldown

class Swap(Ability):
    '''
    Способность, обменивающая игроков местами
    '''
    def __init__(self):
        '''
        Создание объекта, заимствовано у родительского класса
        '''
        super().__init__(2, 660, 0)

    def use(self, **kwargs):
        '''
        Меняет игроков местями если они не слишком далеко друг от другс

        :param kwargs: не используется здесь
        :type kwargs: dict
        '''
        if super().use(**kwargs):
            owner = self.owner
            enemy = self.enemy
            if owner.distance(enemy) <= 300 and not owner.is_dead() and not enemy.is_dead():
                owner.rect, enemy.rect = pygame.Rect(enemy.rect), pygame.Rect(owner.rect)
                self.ticks = self.cooldown

class Pulling(Ability):
    '''
    Способность, притягивающая противника к владельцу

    :ivar x: скорость притяжения по х
    :type x: int
    :ivar y: скорость притяжения по у
    :type y: int
    '''
    def __init__(self):
        '''
        Создание объекта, заимствовано у родительского класса
        '''
        super().__init__(3, 720, 10)

    def use(self, **kwargs):
        '''
        Притягивает противника в зоне досягаемости к владельцу

        :param kwargs: не используется здесь
        :type kwargs: dict
        '''
        if super().use(**kwargs):
            self.enemy.unpush_all_movement_buttons()
            self.x = max(-20, min(20, (self.owner.rect.left - self.enemy.rect.left)/self.duration))
            self.y = max(-20, min(20, (self.owner.rect.top - self.enemy.rect.top)/self.duration))
            self.enemy.velocity.x += self.x
            self.enemy.velocity.y += self.y
            self.ticks = self.cooldown

    def deactivate(self):
        '''
        Отмена притягивания противника
        '''
        self.enemy.velocity.x -= self.x
        self.enemy.velocity.y -= self.y

    def consume_cooldown(self):
        '''
        Уменьшает время до отката, отменяет эффект способности в нужное время
        '''
        super().consume_cooldown()
        if self.ticks == self.cooldown - self.duration:
            self.deactivate()

class Fireball(Ability):
    '''
    Способность, позволяющая запустить огненный шар

    :ivar rect: рект шара
    :type rect: pygame.Rect
    :ivar velocity: скорость шара
    :type velocity: Vector
    :ivar platforms: список передаваемых платформ, с которыми шар может столкнуться
    :type platforms: list
    :ivar can_damage: наносит ли урон
    :type can_damage: bool
    :ivar surface: поверхность огненного шара
    :type surface: pygame.Surface
    :ivar screen: передаваемый экран
    :type screen: pygame.Surface
    :ivar replay_file: файл с реплеем текущей игры (если записывается)
    :type replay_file: TextIOWrapper
    '''
    def __init__(self):
        '''
        Создание объекта
        '''
        super().__init__(4, 600, 180)
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.velocity = Vector()
        self.platforms = []
        self.can_damage = False
        self.screen = None
        self.replay_file = None
        self.surface = pygame.Surface((24, 24))
        self.surface.fill((255, 64, 64))

    def use(self, **kwargs):
        """
        Выпускает в  сторону движения владельца огненный шар, уничтожающийся при столкновении с платформами и убивающий противника при столкновении с ним

        :keyword screen: передаваемый экран
        :type screen: pygame.Surface
        :keyword replay_file: файл с реплеем, если записывается
        :type replay_file: TextIOWrapper
        :keyword platforms: платформы, с которыми шар может столкнуться
        :type platforms: list
        """
        if super().use(**kwargs):
            self.platforms = kwargs['platforms']
            self.velocity.x = self.owner.velocity.x
            self.velocity.y = self.owner.velocity.y/2
            self.ticks = self.cooldown
            self.can_damage = True
            self.screen = kwargs['screen']
            self.replay_file = kwargs['replay_file']
            self.rect = pygame.Rect(self.owner.rect.topleft, (24, 24))
            self.rect.move_ip(4, 4)

    def consume_cooldown(self):
        '''
        Отрисовка шара, проработка столкновения шара с платформой/противником

        :returns: ничего, return нужен для завершения метода при уничтожении шара
        :rtype: None
        '''
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
            if self.replay_file is not None:
                self.replay_file.writelines([f"draw-{self.rect.left},{self.rect.top},{self.rect.width},{self.rect.height}-255, 64, 64\n"])
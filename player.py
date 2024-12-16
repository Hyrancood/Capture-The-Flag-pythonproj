'''Класс персонажей, а также классы кнопок для взаимодействия с персонажами'''

import pygame

import abilities
import vector

G_ACCELERATION = 0.2
DASH_POWER = 7
DASH_COOLDOWN = 60*7 #60 fps
DASH_DURATION = 14 #frames

class Button:
    '''
    Класс кнопки, родительский класс для кнопок, позволяющих взаимодействовать с персонажами

    :ivar is_pressed: нажата ли кнопка
    :type is_pressed: bool
    '''
    def __init__(self):
        '''
        Инициализация кнопки (по умолчанию не нажата)
        '''
        self.is_pressed = False

    def pressed(self, player: "Player", **kwargs):
        '''
        Нажатие кнопки

        :param player: игрок, к которому соответствует кнопка
        :type player: Player
        :param kwargs: параметры, нужные в подклассах
        :type kwargs: dict
        :returns: True если кнопка была успешно нажата методом, False если кнопка была нажата до этого
        :rtype: bool
        '''
        if not self.is_pressed:
            self.is_pressed = True
            return True
        return False

    def unpressed(self, player: "Player"):
        '''
        Разжатие кнопки

        :param player: игрок, к которому соответствует кнопка
        :type player: Player
        :returns: True если кнопка была успешно разжата методом, False если кнопка была разжата до этого
        :rtype: bool
        '''
        if self.is_pressed:
            self.is_pressed = False
            return True
        return False

class LeftButton(Button):
    '''
    Класс кнопки, двигающей игрока влево

    :ivar speed: значение, на которую кнопка изменяет скорость игрока
    :type speed: int
    '''
    def pressed(self, player: "Player", **kwargs):
        '''
        Нажатие левой кнопки, двигает игрока влево

        :param player: игрок, которого двигает эта кнопка
        :type player: Player
        :param kwargs: нужны в других подклассах
        :type kwargs: dict
        '''
        if super().pressed(player):
            self.speed = player.speed
            player.velocity.x -= player.speed

    def unpressed(self, player: "Player"):
        '''
        Разжатие левой кнопки, останавливает движение игрока влево

        :param player: игрок, которого двигает эта кнопка
        :type player: Player
        :param kwargs: нужны в других подклассах
        :type kwargs: dict
        '''
        if super().unpressed(player):
            player.velocity.x += self.speed

class RightButton(Button):
    '''
    Класс кнопки, двигающей игрока вправо

    :ivar speed: значение, на которую кнопка изменяет скорость игрока
    :type speed: int
    '''
    def pressed(self, player: "Player", **kwargs):
        '''
        Нажатие правой кнопки, двигает игрока вправо

        :param player: игрок, которого двигает эта кнопка
        :type player: Player
        :param kwargs: нужны в других подклассах
        :type kwargs: dict
        '''
        if super().pressed(player):
            self.speed = player.speed
            player.velocity.x += player.speed

    def unpressed(self, player: "Player"):
        '''
        Разжатие правой кнопки, останавливает движение игрока вправо

        :param player: игрок, которого двигает эта кнопка
        :type player: Player
        :param kwargs: нужны в других подклассах
        :type kwargs: dict
        '''
        if super().unpressed(player):
            player.velocity.x -= self.speed

class UpButton(Button):
    '''
    Кнопка прыжка
    '''
    def pressed(self, player: "Player", **kwargs):
        '''
        Нажатие кнопки прыжка, игрок прыгает вверх, если стоит на земле

        :param player: игрок, которого двигает эта кнопка
        :type player: Player
        :param kwargs: нужны в других подклассах
        :type kwargs: dict
        '''
        if super().pressed(player) and player.is_stand(**kwargs):
            player.velocity.y -= player.speed*2.3

class DashButton(Button):
    '''
    Кнопка дэша
    '''
    def pressed(self, player: "Player", **kwargs):
        '''
        Нажатие кнопки дэша, игрок совершает рывок в сторону движения

        :param player:
        :type player: Player
        :param kwargs: параметры, нужные в других подклассах
        :type kwargs: dict
        '''
        if super().pressed(player) and player.velocity.x != 0 and player.dash == 0:
            mode = 1 if player.velocity.x > 0 else -1
            player.velocity.x += player.speed * DASH_POWER * mode
            player.dash = DASH_COOLDOWN * mode

class AbilityButton(Button):
    '''
    Кнопка способности

    :ivar ability: конкретная способность, соответствующая кнопке
    :type ability: abilities.Ability
    '''
    def __init__(self):
        '''
        Инициализация кнопки, по умолчанию ей не соответствует способность (None)
        '''
        super().__init__()
        self.ability = None

    def set_ability(self, ability: abilities.Ability):
        '''
        Устанавливает соответствие кнопки конкретной способности

        :param ability: устанавливавемая способность
        :type ability: abilities.Ability
        '''
        self.ability = ability

    def pressed(self, player: "Player", **kwargs):
        '''
        Нажатие кнопки, применяет способность

        :param player: игрок, который применяет способность
        :type player: Player
        :param kwargs: нужны для некоторых способностей
        :type kwargs: dict
        '''
        if super().pressed(player, **kwargs) and self.ability is not None:
            self.ability.use(**kwargs)

class Player:
    '''
    Класс игрока, нужен для взаимодействия с игроком через клавиатуру, взаимодействия других объектов с игроком и т.д.

    :ivar color: цвет игрока
    :type color: str
    :ivar spawn_point: позиция спавна игрока
    :type spawn_point: tuple
    :ivar dash: оставшееся время дэша в фреймах
    :type dash: int
    :ivar dead: оставшееся время смерти в фремах
    :type dead: int
    :ivar movement_buttons: сопоставление кнопок передвижения индексам кнопок клавиатуры
    :type movement_buttons: dict
    :ivar ability_buttons: сопоставление кнопок способностей индексам кнопок клавиатуры
    :type ability buttons: dict
    :ivar rect: рект игрока
    :type rect: pygame.Rect
    :ivar speed: скорость игрока
    :type speed: int
    :ivar velocity: текущая скорость игрока
    :type velocity: vector.Vector
    :ivar carried_flag: флаг, который игрок несет (если несет)
    :type carried_flag: core.Flag
    :ivar winner: победил ли игрок
    :type winner: bool
    '''
    def __init__(self,chosen_color):
        '''
        Создание игрока

        :param chosen_color: выбранный цвет игрока
        :type chosen_color: str
        '''
        self.color=chosen_color
        self.spawn_point = None
        self.dash = 0
        self.dead = 0
        if self.color=='red':
            self.movement_buttons = {1073741903: RightButton(), 1073741904: LeftButton(), 1073741906: UpButton(), 1073741905: DashButton()}
            self.ability_buttons = {1073742053: AbilityButton(), 1073742052: AbilityButton()}
        else:
            self.movement_buttons = {100: RightButton(), 97: LeftButton(), 119: UpButton(), 115: DashButton()}
            self.ability_buttons = {101: AbilityButton(), 113: AbilityButton()}
        self.rect=pygame.Rect(0,0,32,64)
        self.speed=3.7
        self.velocity=vector.Vector()
        self.carried_flag = None
        self.winner = False

    def set_abilities(self, chosen_abilities):
        '''
        Позволяет установить выбранные способности на игрока

        :param chosen_abilities: выбранные способности
        :type chosen_abilities: list
        '''
        i = 0
        for item in self.ability_buttons.items():
            if i < len(chosen_abilities):
                item[1].set_ability(chosen_abilities[i])
                i += 1

    def distance(self, other: "Player"):
        '''
        Измеряет расстояние между игроками

        :param other: другой игрок
        :type other: PLayer
        :returns: декартово расстояние между игроками
        :rtype: float
        :raises TypeError: если передаваемый тип - не Player
        '''
        if not isinstance(other, Player):
            raise TypeError
        return (abs(self.rect.top - other.rect.top)**2 +
                abs(self.rect.left - other.rect.left)**2)**0.5

    def is_dead(self):
        '''
        Проверяет мертв ли игрок

        :returns: мертв игрок или нет
        :rtype: bool
        '''
        return self.dead > 0

    def die(self):
        '''
        Убийство игрока (задается время смерти и сбрасывается флаг)
        '''
        self.dead = 60 * 5
        if self.carried_flag is not None:
            self.carried_flag.is_carried = False
            self.carried_flag = None

    def blit_on_screen(self, screen):
        '''
        Рисование игрока на экране (вместе с флагом, если он взят)

        :param screen: передаваемый экран
        :type screen: pygame.Surface
        '''
        surf = pygame.Surface((self.rect.width, self.rect.height))
        surf.fill((200 if self.color == "red" else 0, 180, 255 if self.color == "blue" else 0))
        screen.blit(surf, self.rect)
        if self.carried_flag is not None:
            surf = pygame.Surface((16, 16))
            surf.fill((255, 0, 0) if self.carried_flag.color == "red" else (0, 0, 255))
            x, y = self.rect.topleft
            screen.blit(surf, (x + 8, y - 16))

    def drawn_respawn_time_on_screen(self, screen, font: pygame.font.Font):
        '''
        Рисование оствашегося до респавна времени на экране над точкой спавна

        :param screen: передаваемый экран
        :type screen: pygame.Surface
        :param font: шрифт выводимых цифр
        :type font: pygame.font.Font
        '''
        screen.blit(font.render(str(int(self.dead//60)), False, (0,0,0)),
                    (self.spawn_point[0]+5, self.spawn_point[1]))

    def opposite(self, teams):
        '''
        Определяет противника

        :param teams: список команд
        :type teams: dict
        :returns: противник
        :rtype: PLayer
        :raises TypeError: если передаваемый тип - не Player
        '''
        return teams['blue'].player if self.color=='red' else teams['red'].player

    def is_on_ground(self, platforms):
        '''
        Проверяет, на земле ли игрок

        :param platforms: массив платформ, на которых может стоять игрок
        :type platform: array
        :returns: стоит ли игрок на земле
        :rtype: bool
        :raises TypeError: если передаваемый тип - не list из pygame.Rect
        '''
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(0, 1)
        return any(player_rect.colliderect(platform) for platform in platforms)

    def is_standing_on_other_player(self, other: "Player"):
        '''
        Проверяет, стоит ли игрок на другом игроке

        :param other: другой игрок
        :type other: Player
        :returns: стоит ли игрок на другом игроке
        :rtype: bool
        :raises TypeError: если передаваемый тип - не Player
        '''
        if not isinstance(other, Player):
            raise TypeError
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(0, 1)
        return not self.rect.colliderect(other.rect) and player_rect.colliderect(other.rect)

    def is_stand(self, **kwargs):
        '''
        Проверяет, стоит ли игрок

        :keyword platforms: передаваемые платформы
        :type platforms: list
        :keyword teams: передаваемые команды
        :type teams: dict
        :returns: стоит ли игрок
        :rtype: bool
        :raises TypeError: если передаваемый тип в kwargs['platforms'] - не list из pygame.Rect или в kwargs['teams'] -  не iist из core.Team
        '''
        return (self.is_on_ground(kwargs['platforms']) or
                self.is_standing_on_other_player(self.opposite(kwargs['teams'])))

    def is_in_dash(self):
        '''
        Проверяет, находится ли игрок в дэше

        :returns: в дэше ли игрок
        :rtype: bool
        '''
        return abs(self.dash) > DASH_COOLDOWN - DASH_DURATION

    def spawn(self, **kwargs):
        '''
        Возрождает игрока на заданных координатах, обнуляет скорость и кулдаун дэша, отжимает кнопки игрока

        :keyword spawn_x: х координата точки возрождения
        :type spawn_x: int
        :keyword spawn_у: y координата точки возрождения
        :type spawn_y: int
        '''
        if self.spawn_point is None:
            self.spawn_point = (kwargs['spawn_x'], kwargs['spawn_y'])
        self.rect = pygame.Rect(self.spawn_point, (32, 64))
        self.velocity=vector.Vector()
        self.dash = 0
        for button in self.movement_buttons.values():
            button.is_pressed = False
        for button in self.ability_buttons.values():
            button.is_pressed = False

    def update(self,**kwargs):
        '''
        Воспроизводит все изменения в статусах и положении игроков, взаимодействия игроков, выводит все это на экран

        :keyword screen: выводимое на экран изображение
        :type screen:  pygame.Surface
        :param font: шрифт выводимых цифр
        :type font: pygame.font.Font
        :keyword thorns: рект шипов
        :type thorns: pygame.Rect
        '''
        if self.is_dead():
            self.dead -= 1
            if self.dead == 0:
                self.spawn(**kwargs)
            else:
                self.drawn_respawn_time_on_screen(kwargs['screen'], kwargs['font'])
        else:
            self.handle_movement(**kwargs)
            self.handle_abilities(**kwargs)
            if self.rect.collidelist(kwargs['thorns']) >= 0:
                self.die()
            self.blit_on_screen(kwargs['screen'])
        self.update_abilities(**kwargs)

    def unpush_all_movement_buttons(self):
        '''
        Разжимает все кнопки движения
        '''
        for button in self.movement_buttons.values():
            button.unpressed(self)

    def handle_movement_buttons(self, **kwargs):
        '''
        Зажимает/разжимает кнопки движения в зависимости от зажатых кнопок на клавиатуре

        :keyword events: события, считываемые pygame
        :type events: pygame.event.Event
        '''
        for event in kwargs['events']:
            if event.type == pygame.KEYDOWN:
                button = self.movement_buttons.get(event.key)
                if button is not None:
                    button.pressed(self, **kwargs)
            if event.type == pygame.KEYUP:
                button = self.movement_buttons.get(event.key)
                if button is not None:
                    button.unpressed(self)

    def calculate_velocity(self, **kwargs):
        '''
        Вычисляет текущую скорость игрока, а также уменьшает откат дэша

        :param kwargs: нужен в других используемых здесь методах
        :type kwargs: dict
        '''
        on_ground = self.is_stand(**kwargs)
        if not on_ground:
            self.velocity.y += G_ACCELERATION
        else:
            self.velocity.y = 0
        self.handle_movement_buttons(**kwargs)
        if self.dash != 0:
            mode = 1 if self.dash > 0 else -1
            if self.is_in_dash():
                self.velocity.x -= mode * self.speed * (DASH_POWER / DASH_DURATION)
            self.dash -= mode

    def handle_collision_with_rect(self, dx, dy, rect: pygame.Rect):
        '''
        Просчитывает столкновение игрока с объектами класса pygame.Rect, т.е. уменьшает перемещение игрока за фрейм так, чтобы он не наткнулся на другие объекты

        :param dx: изменение положения игрока за фрейм по х
        :type dx: int
        :param dy: изменение положения игрока за фрейм по y
        :type dy: int
        :param rect: рект, с которым просчитывается столкновение
        :type rect: pygame.Rect
        :returns: измененное мгновенное перемещение по х и по у
        :rtype: tuple
        '''
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

    def handle_collision_with_map_borders(self, dx, dy, **kwargs):
        '''
        Просчитывает столкновение игрока с границами карты

        :param dx: изменение положения игрока за фрейм по х
        :type dx: int
        :param dy: изменение положения игрока за фрейм по y
        :type dy: int
        :keyword area: область игры
        :type area: pygame.Rect
        :returns: измененное мгновенное перемещение по х и по у
        :rtype: tuple
        '''
        area = kwargs['area']
        borders = [
            pygame.Rect(area.left, area.top-1, area.width, 1),
            pygame.Rect(area.left-1, area.top, 1, area.height),
            pygame.Rect(area.left, area.bottom, area.width, 1),
            pygame.Rect(area.right, area.top, 1, area.height),
        ]
        for border in borders:
            dx, dy = self.handle_collision_with_rect(dx, dy, border)
        return dx, dy

    def handle_collisions_with_platforms(self, **kwargs):
        '''
        Просчитывает столкновение игрока с платформами

        :keyword dx: изменение положения игрока за фрейм по х
        :type dx: int
        :keyword dy: изменение положения игрока за фрейм по y
        :type dy: int
        :keyword pllatforms: платформы, с которыми просчитывается столкновение
        :type platforms: list
        :returns: измененное мгновенное перемещение по х и по у
        :rtype: tuple
        '''
        dx, dy = kwargs['dx'], kwargs['dy']
        for platform in kwargs['platforms']:
            dx, dy = self.handle_collision_with_rect(dx, dy, platform)
        return dx, dy

    def handle_collision_with_other_player(self, dx, dy, other: "Player"):
        '''
        Просчитывает столкновение игрока с противником (а также убивает одного из них если игрок в дэше)

        :param dx: изменение положения игрока за фрейм по х
        :type dx: int
        :param dy: изменение положения игрока за фрейм по y
        :type dy: int
        :returns: измененное мгновенное перемещение по х и по у
        :rtype: tuple
        '''
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
        '''
        Просчитывает столкновение игрока с флагом (захват флага при контакте с вражеским, победа при контакте со своим флагом при наличии вражеского)

        :keyword dx: изменение положения игрока за фрейм по х
        :type dx: int
        :keyword dy: изменение положения игрока за фрейм по y
        :type dy: int
        :keyword teams: платформы, с которыми просчитывается столкновение
        :type teams: dict
        :returns: измененное мгновенное перемещение по х и по у
        :rtype: tuple
        '''
        dx, dy = kwargs['dx'], kwargs['dy']
        player_rect = pygame.Rect(self.rect)
        player_rect.move_ip(dx, dy)
        enemy_flag = kwargs['teams']['red' if self.color == 'blue' else 'blue'].flag
        team_flag = kwargs['teams']['red' if self.color == 'red' else 'blue'].flag
        if enemy_flag.is_carried:
            if player_rect.colliderect(team_flag.rect):
                self.winner = True
        else:
            if player_rect.colliderect(enemy_flag.rect):
                enemy_flag.is_carried = True
                self.carried_flag = enemy_flag
        return dx, dy

    def handle_movement(self, **kwargs):
        '''
        Просчитывает мгновенное изменение скорости в зависимости от столкновений

        :param kwargs: нужны для других методов внутри этого
        :type kwargs: dict
        '''
        self.calculate_velocity(**kwargs)
        dx, dy = self.velocity.x, self.velocity.y
        dx, dy = self.handle_collision_with_map_borders(**kwargs, dx=dx, dy=dy)
        dx, dy = self.handle_collisions_with_platforms(**kwargs, dx=dx, dy=dy)
        dx, dy = self.handle_collision_with_other_player(dx, dy, self.opposite(kwargs['teams']))
        dx, dy = self.handle_collision_with_enemy_flag(**kwargs, dx=dx, dy=dy)
        self.rect.move_ip(dx, dy)
        if dy > self.velocity.y:
            self.velocity.y = 0

    def handle_abilities(self, **kwargs):
        '''
        Расчитывает применение способностей

        :keyword events: события, считываемые pygame
        :type events: pygame.event.Event
        '''
        for event in kwargs['events']:
            if event.type == pygame.KEYDOWN:
                button = self.ability_buttons.get(event.key)
                if button is not None:
                    button.pressed(self, **kwargs)
            if event.type == pygame.KEYUP:
                button = self.ability_buttons.get(event.key)
                if button is not None:
                    button.unpressed(self)

    def update_abilities(self, **kwargs):
        '''
        Выводит иконки способностей на экран в зависимости от времени до перезарядки, уменьшает кулдаун

        :keyword area: область игры
        :type area: pygame.Rect
        :keyword screen: выводимое на экран изображение
        :type screen:  pygame.Surface
        '''
        offset = 16 if self.color == 'blue' else kwargs['area'].width - 80
        for button in self.ability_buttons.values():
            if isinstance(button, AbilityButton):
                if button.ability is not None:
                    button.ability.consume_cooldown()
                    button.ability.blit_on(kwargs['screen'], kwargs['area'], offset)
                    offset += 80 if self.color == 'blue' else -80
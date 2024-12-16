"""Выбор способностей перед игрой"""
import pygame

import abilities
import config
import core


class Button:
	"""
	Класс кнопки

	"ivar is_pushed: нажата ли кнопка
	:type is_pushed: bool
	:ivar sprite: спрайт кнопки
	:type sprite: pygame.Surface
	:ivar sprite_pushed: спрайт нажатой кнопки
	:type sprite_pushed: pygame.Surface
	"""
	def __init__(self, sprite: str, sprite_pushed: str):
		"""
		Создание новой кнопки

		:param sprite: путь к спрайту
		:param sprite_pushed: путь к нажатому спрайту
		"""
		self.is_pushed = False
		self.sprite = config.get(sprite)
		self.sprite_pushed = config.get(sprite_pushed)

	def press(self):
		"""Нажатие кнопки"""
		self.is_pushed = True

	def unpress(self):
		"""Отжатие кнопки"""
		self.is_pushed = False

	def get_sprite(self):
		"""Текущий спрайт"""
		return self.sprite_pushed if self.is_pushed else self.sprite


class AbilityButton(Button):
	"""
	Кнопка выбора способностей

	:ivar ability: выбираемая способность
	:type ability: abilities.Ability
	"""
	def __init__(self, id: int, ability: abilities.Ability):
		"""
		Создание новой кнопки для выбора способности

		:param id: id спрайта способности
		:param ability: способность
		"""
		super().__init__(f"ability{id}.png", f"ability{id}_pushed.png")
		self.ability = ability


left_buttons = None
"""Левые кнопки для синего игрока"""
right_buttons = None
"""Правые кнопки для синего игрока"""
i, j = 0, 0
"""Номер выбранной кнопки слева и справа соответственно"""

def load_assets():
	"""
	Загрузка ресурсов
	"""
	global left_buttons, right_buttons
	left_buttons = [
		Button("start.png", "start_pushed.png"),
		AbilityButton(1, abilities.Freeze()),
		AbilityButton(2, abilities.Bomb()),
		AbilityButton(3, abilities.Swap()),
		AbilityButton(4, abilities.Pulling()),
		AbilityButton(5, abilities.Fireball()), 0
	]
	right_buttons = [
		Button("start.png", "start_pushed.png"),
		AbilityButton(1, abilities.Freeze()),
		AbilityButton(2, abilities.Bomb()),
		AbilityButton(3, abilities.Swap()),
		AbilityButton(4, abilities.Pulling()),
		AbilityButton(5, abilities.Fireball()), 0
	]


def run(**kwargs):
	"""
	Обработка текущего окна

	:param kwargs: данные игры
	:return: следующее окно
	"""
	global i, j, left_buttons, right_buttons
	for event in kwargs["events"]:
		if event.type == pygame.KEYDOWN:
			if event.key == 13:
				button = right_buttons[j % 6]
				if j % 6 == 0:
					if button.is_pushed:
						button.unpress()
					else:
						button.press()
				else:
					if button.is_pushed:
						button.unpress()
						right_buttons[6] -= 1
					else:
						if right_buttons[6] < 2:
							right_buttons[6] += 1
							button.press()
			if event.key == 101:
				button = left_buttons[i % 6]
				if i % 6 == 0:
					if button.is_pushed:
						button.unpress()
					else:
						button.press()
				else:
					if button.is_pushed:
						button.unpress()
						left_buttons[6] -= 1
					else:
						if left_buttons[6] < 2:
							left_buttons[6] += 1
							button.press()
			if event.key == 1073741905:
				j+=1
			if event.key == 1073741906:
				j-=1
			if event.key == 115:
				i+=1
			if event.key == 119:
				i-=1
	if left_buttons[0].is_pushed and right_buttons[0].is_pushed:
		red, blue = core.instance.teams['red'].player, core.instance.teams['blue'].player
		blue_abilities = []
		for button in left_buttons:
			if isinstance(button, AbilityButton):
				if button.is_pushed:
					button.ability.set_player(blue, red)
					blue_abilities.append(button.ability)
		blue.set_abilities(blue_abilities)
		red_abilities = []
		for button in right_buttons:
			if isinstance(button, AbilityButton):
				if button.is_pushed:
					button.ability.set_player(red, blue)
					red_abilities.append(button.ability)
		red.set_abilities(red_abilities)
		for button in left_buttons[:6] + right_buttons[:6]:
			button.unpress()
		left_buttons[6], right_buttons[6] = 0, 0
		return "MAPS"
	screen = kwargs["screen"]
	screen.blit(config.get("main_menu_bg.png"), (0, 0))

	array = ((left_buttons, i, 130), (right_buttons, j, 840))
	for buttons in array:
		for n in range(6):
			button = buttons[0][n]
			surf = button.get_sprite()
			surf.set_alpha(255 if button.is_pushed or buttons[1] % 6 == n else 200)
			screen.blit(surf, (buttons[2], 250 if n == 0 else 300 + n * 60))

	pygame.display.flip()
	kwargs["clock"].tick(60)
	return "PREGAME"

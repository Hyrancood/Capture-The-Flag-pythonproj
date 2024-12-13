import pygame
import player, abilities, core
from abilities import Freeze


class Button:
	def __init__(self, sprite: str, sprite_pushed: str):
		self.is_pushed = False
		self.sprite = pygame.image.load(sprite)
		self.sprite_pushed = pygame.image.load(sprite_pushed)

	def press(self):
		self.is_pushed = True

	def unpress(self):
		self.is_pushed = False

	def get_sprite(self):
		return self.sprite_pushed if self.is_pushed else self.sprite


class AbilityButton(Button):
	def __init__(self, id: int, ability: abilities.Ability):
		super().__init__(f"assets/ability{id}.png", f"assets/ability{id}_pushed.png")
		self.ability = ability



background = pygame.image.load("assets/main_menu_bg.png")
left_buttons = [
	Button("assets/start.png", "assets/start_pushed.png"),
	AbilityButton(1, abilities.Freeze()),
	AbilityButton(2, abilities.Bomb()),
	AbilityButton(3, abilities.Swap()),
	AbilityButton(4, abilities.Pulling()),
	AbilityButton(5, abilities.Fireball()),
	0
]
right_buttons = [
	Button("assets/start.png", "assets/start_pushed.png"),
	AbilityButton(1, abilities.Freeze()),
	AbilityButton(2, abilities.Bomb()),
	AbilityButton(3, abilities.Swap()),
	AbilityButton(4, abilities.Pulling()),
	AbilityButton(5, abilities.Fireball()),
	0
]
i, j = 0, 0
#номер выбранной кнопки слева и справа соответственно

def run(**kwargs):
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
	screen.blit(background, (0, 0))

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

"""Главное меню"""
import pygame

import config
import core

i = 0
"""Указатель кнопки по вертикали"""
j = 0
"""Указатель кнопки по горизонтали"""
NEXT = ["PREGAME", "REPLAYS"]
"""Следующее окно"""

def run(**kwargs):
	"""
	Обработка текущего окна

	:param kwargs: данные игры
	:return: следующее окно
	"""
	global i, j
	for event in kwargs["events"]:
		if event.type == pygame.KEYDOWN:
			if event.key == 13 or event.unicode == '\r':
				if j % 2 == 0:
					return NEXT[i % 2]
				else:
					core.instance.should_write_replay = not core.instance.should_write_replay
			if event.key in (9, 1073741905, 1073741906) or event.unicode == '\t':
				i += 1
			if event.key in (1073741903, 1073741904):
				j += 1
	screen = kwargs["screen"]
	screen.blit(config.get("main_menu_bg.png"), (0, 0))
	play_button = config.get("play.png")
	replays_button = config.get("replays.png")
	rec_button = config.get("rec_on.png") if core.instance.should_write_replay else config.get("rec_off.png")
	if i % 2 == 0 and j % 2 == 0:
		play_button.set_alpha(255)
		replays_button.set_alpha(200)
		rec_button.set_alpha(200)
	elif i % 2 == 1 and j % 2 == 0:
		play_button.set_alpha(200)
		replays_button.set_alpha(255)
		rec_button.set_alpha(200)
	else:
		play_button.set_alpha(200)
		replays_button.set_alpha(200)
		rec_button.set_alpha(255)
	screen.blit(play_button, (261, 144))
	screen.blit(replays_button, (261, 384))
	screen.blit(rec_button, (1050, 144))
	pygame.display.flip()
	kwargs["clock"].tick(60)
	return "MAIN"
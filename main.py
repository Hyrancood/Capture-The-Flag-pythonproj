import pygame
import config


i = 0
NEXT = ["PREGAME", "REPLAYS"]


def run(**kwargs):
	global i
	for event in kwargs["events"]:
		if event.type == pygame.KEYDOWN:
			if event.key == 13 or event.unicode == '\r':
				return NEXT[i % 2]
			if event.key in (9, 1073741905, 1073741906) or event.unicode == '\t':
				i += 1
	screen = kwargs["screen"]
	screen.blit(config.get("main_menu_bg.png"), (0, 0))
	play_button = config.get("play.png")
	replays_button = config.get("replays.png")
	if i % 2 == 0:
		play_button.set_alpha(255)
		replays_button.set_alpha(200)
	else:
		play_button.set_alpha(200)
		replays_button.set_alpha(255)
	screen.blit(play_button, (261, 144))
	screen.blit(replays_button, (261, 384))
	pygame.display.flip()
	kwargs["clock"].tick(60)
	return "MAIN"
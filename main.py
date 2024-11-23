import pygame

background = pygame.image.load("assets/main_menu_bg.png")
play_button_original = pygame.image.load("assets/play.png")
replays_button_original = pygame.image.load("assets/replays.png")
i = 0
NEXT = ["PREGAME", "REPLAYS"]

def run(**kwargs):
	global i
	for event in kwargs["events"]:
		if event.type == pygame.KEYDOWN:
			print(f"KEYDOWN: {event}")
			if event.key == 13 or event.unicode == '\r':
				return NEXT[i % 2]
			if event.key == 9 or event.unicode == '\t':
				i += 1
			if event.key == 1073741905:
				i += 1
			if event.key == 1073741906:
				i -= 1
	screen = kwargs["screen"]
	screen.blit(background, (0, 0))
	play_button = play_button_original.copy()
	replays_button = replays_button_original.copy()
	if i % 2 == 0:
		play_button.set_alpha(255)
		replays_button.set_alpha(200)
	else:
		play_button.set_alpha(200)
		replays_button.set_alpha(255)
	screen.blit(play_button, (261, 144))
	screen.blit(replays_button, (261, 384))
	#screen.fill("blue")
	pygame.display.flip()
	kwargs["clock"].tick(60)
	return "MAIN"
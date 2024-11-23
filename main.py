import pygame


def run(**kwargs):
	for event in kwargs["events"]:
		if event.type == pygame.KEYDOWN:
			print(f'Keydown: {event}')
			if event.key == 13:
				print("a")
				return "GAME"
	screen = kwargs["screen"]
	screen.fill("blue")
	pygame.display.flip()
	kwargs["clock"].tick(60)
	return "MAIN"
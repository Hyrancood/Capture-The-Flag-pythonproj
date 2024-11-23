import pygame
import main, maps, replays, pregame, game


USE = main.run
MODES = {
	"MAIN": main.run,
	"REPLAYS": replays.run,
	"MAPS": maps.run,
	"PREGAME": pregame.run,
	"GAME": game.run,
}


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((1280, 720))
	clock = pygame.time.Clock()
	running = True

	while running:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				running = False
		USE = MODES[USE(**{"screen":screen,"clock":clock, "events":events})]
	pygame.quit()
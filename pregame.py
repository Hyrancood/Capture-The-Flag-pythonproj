import pygame

background = pygame.image.load("assets/main_menu_bg.png")
buttons1=[0]*6
buttons2=[0]*6
buttons1[0] = pygame.image.load("assets/start.png")
buttons2[0] = pygame.image.load("assets/start.png")
for _ in range(1,6):
	buttons1[_] = pygame.image.load("assets/ability.png")
	buttons2[_] = pygame.image.load("assets/ability.png")
#start_button_1 = pygame.image.load("assets/start.png")
#start_button_2 = pygame.image.load("assets/start.png")
#ability_button_1_1 = pygame.image.load("assets/ability.png")
#ability_button_1_2 = pygame.image.load("assets/ability.png")
#ability_button_1_3 = pygame.image.load("assets/ability.png")
#ability_button_1_4 = pygame.image.load("assets/ability.png")
#ability_button_1_5 = pygame.image.load("assets/ability.png")
#ability_button_2_1 = pygame.image.load("assets/ability.png")
#ability_button_2_2 = pygame.image.load("assets/ability.png")
#ability_button_2_3 = pygame.image.load("assets/ability.png")
#ability_button_2_4 = pygame.image.load("assets/ability.png")
#ability_button_2_5 = pygame.image.load("assets/ability.png")

i, j = 0, 0
NEXT = ["GAME", "MAPS"]
ispushed1=[0]*6
ispushed2=[0]*6

def run(**kwargs):
	global i
	global j
	for event in kwargs["events"]:
		if event.type == pygame.KEYDOWN:
			if event.key == 13:
				if  j%6 == 0:
					if  ispushed2[0]==0:
						buttons2[0] = pygame.image.load("assets/start_pushed.png")
						ispushed2[0]=1
					else:
						buttons2[0] = pygame.image.load("assets/start.png")
						ispushed2[0] = 0
				else:
					if  ispushed2[j%6]==0 and sum(ispushed2[1:])<=1:
						buttons2[j%6] = pygame.image.load("assets/ability_pushed.png")
						ispushed2[j%6]=1
					else:
						buttons2[j%6] = pygame.image.load("assets/ability.png")
						ispushed2[j%6] = 0
			if event.key == 101:
				if i % 6 == 0:
					if ispushed1[0] == 0:
						buttons1[0] = pygame.image.load("assets/start_pushed.png")
						ispushed1[0] = 1
					else:
						buttons1[0] = pygame.image.load("assets/start.png")
						ispushed1[0] = 0
				else:
					if ispushed1[i % 6] == 0 and sum(ispushed1[1:]) <= 1:
						buttons1[i % 6] = pygame.image.load("assets/ability_pushed.png")
						ispushed1[i % 6] = 1
					else:
						buttons1[i % 6] = pygame.image.load("assets/ability.png")
						ispushed1[i % 6] = 0
			if event.key == 1073741905:
				j+=1
			if event.key == 1073741906:
				j-=1
			if event.key == 115:
				i+=1
			if event.key == 119:
				i-=1
	if ispushed1[0]==1 and ispushed2[0]==1:
		return NEXT[0]
	screen = kwargs["screen"]
	screen.blit(background, (0, 0))

	buttons1[i%6].set_alpha(200)
	for _ in range(i+1,i+6):
		buttons1[_%6].set_alpha(255)

	buttons2[j % 6].set_alpha(200)
	for _ in range(j + 1, j + 6):
		buttons2[_ % 6].set_alpha(255)

	screen.blit(buttons1[0], (120, 300))
	screen.blit(buttons2[0], (860, 300))
	for _ in range(1,6):
		screen.blit(buttons1[_], (120, 350+_*60))
	for _ in range(1,6):
		screen.blit(buttons2[_], (860, 350+_*60))
	pygame.display.flip()
	kwargs["clock"].tick(60)
	return "PREGAME"
import pygame

background = pygame.image.load("assets/main_menu_bg.png")
current_buttons1=[0]*6
current_buttons2=[0]*6
buttons1=[0]*6
buttons2=[0]*6
current_buttons1[0] = pygame.image.load("assets/start.png")
current_buttons1[1] = pygame.image.load("assets/ability1.png")
current_buttons1[2] = pygame.image.load("assets/ability2.png")
current_buttons1[3] = pygame.image.load("assets/ability3.png")
current_buttons1[4] = pygame.image.load("assets/ability4.png")
current_buttons1[5] = pygame.image.load("assets/ability5.png")
current_buttons2[0] = pygame.image.load("assets/start.png")
current_buttons2[1] = pygame.image.load("assets/ability1.png")
current_buttons2[2] = pygame.image.load("assets/ability2.png")
current_buttons2[3] = pygame.image.load("assets/ability3.png")
current_buttons2[4] = pygame.image.load("assets/ability4.png")
current_buttons2[5] = pygame.image.load("assets/ability5.png")

buttons1[0] = pygame.image.load("assets/start_pushed.png")
buttons1[1] = pygame.image.load("assets/ability1_pushed.png")
buttons1[2] = pygame.image.load("assets/ability2_pushed.png")
buttons1[3] = pygame.image.load("assets/ability3_pushed.png")
buttons1[4] = pygame.image.load("assets/ability4_pushed.png")
buttons1[5] = pygame.image.load("assets/ability5_pushed.png")
buttons2[0] = pygame.image.load("assets/start_pushed.png")
buttons2[1] = pygame.image.load("assets/ability1_pushed.png")
buttons2[2] = pygame.image.load("assets/ability2_pushed.png")
buttons2[3] = pygame.image.load("assets/ability3_pushed.png")
buttons2[4] = pygame.image.load("assets/ability4_pushed.png")
buttons2[5] = pygame.image.load("assets/ability5_pushed.png")

i, j = 0, 0
#номер выбранной кнопки слева и справа соответственно

NEXT = ["MAPS"]
ispushed1=[0]*6
ispushed2=[0]*6

def run(**kwargs):
	global i
	global j
	for event in kwargs["events"]:
		if event.type == pygame.KEYDOWN:
			if event.key == 13:
				if j%6==0:
					if  ispushed2[0]==0:
						current_buttons2[0], buttons2[0] = buttons2[0], current_buttons2[0]
						ispushed2[0]=1
					else:
						current_buttons2[0], buttons2[0] = buttons2[0], current_buttons2[0]
						ispushed2[0] = 0
				else:
					if  ispushed2[j%6]==0:
						if sum(ispushed2[1:])<=1:
							current_buttons2[j%6], buttons2[j%6] = buttons2[j%6], current_buttons2[j%6]
							ispushed2[j%6]=1
					else:
						current_buttons2[j%6], buttons2[j%6] = buttons2[j%6], current_buttons2[j%6]
						ispushed2[j%6] = 0
			if event.key == 101:
				if i%6==0:
					if  ispushed1[0]==0:
						current_buttons1[0], buttons1[0] = buttons1[0], current_buttons1[0]
						ispushed1[0]=1
					else:
						current_buttons1[0], buttons1[0] = buttons1[0], current_buttons1[0]
						ispushed1[0] = 0
				else:
					if  ispushed1[i%6]==0:
						if sum(ispushed1[1:])<=1:
							current_buttons1[i%6], buttons1[i%6] = buttons1[i%6], current_buttons1[i%6]
							ispushed1[i%6]=1
					else:
						current_buttons1[i%6], buttons1[i%6] = buttons1[i%6], current_buttons1[i%6]
						ispushed1[i%6] = 0
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

	current_buttons1[i%6].set_alpha(200)
	for _ in range(i+1,i+6):
		current_buttons1[_%6].set_alpha(255)

	current_buttons2[j % 6].set_alpha(200)
	for _ in range(j + 1, j + 6):
		current_buttons2[_ % 6].set_alpha(255)

	screen.blit(current_buttons1[0], (130, 250))
	screen.blit(current_buttons2[0], (840, 250))
	for _ in range(1,6):
		screen.blit(current_buttons1[_], (130, 300+_*60))
	for _ in range(1,6):
		screen.blit(current_buttons2[_], (840, 300+_*60))
	pygame.display.flip()
	kwargs["clock"].tick(60)
	return "PREGAME"

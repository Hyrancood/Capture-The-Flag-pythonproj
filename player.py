import vector
import pygame

class Player():
    def __init__(self,chosen_color):
        self.color=chosen_color
        self.in_air=0
        self.g_acceleration=1
        if self.color=='blue':
            movement_buttons = {1073741903:'right', 1073741904:'left', 1073741906:'up'}
        else:
            movement_buttons = {100:'right', 97:'left', 119:'up'}
        self.rect=pygame.Rect(0,0,32,64)
        self.first_ability=None
        self.second_ability=None
        self.x=0
        self.y=0
        self.speed=1
        self.velocity=vector.Vector()
    def set_abilities(self,abilities):
        for i1 in range(len(abilities)):
            if abilities[i1] == 1:
                self.first_ability=i1
                for i2 in range(i1+1,len(abilities)):
                    if abilities[i2] == 1:
                        self.second_ability=i2
    def set_position(self,x_set,y_set):
        self.x=x_set
        self.y=y_set
    def opposite(self):
        if self.color=='red':
            return 'blue'
        else: return 'red'
    def update(self,**kwargs):
        self.handle_events(kwargs['events'])
        self.handle_movement(**kwargs)
    def handle_movement(self,**kwargs):
        for arg in kwargs:
            if movement_buttons.get(arg)=='right':
                self.velocity.x+=self.speed
            if movement_buttons.get(arg)=='left':
                self.velocity.x-=self.speed
            if movement_buttons.get(arg)=='up':
                self.velocity.x+=self.speed
        #проверка на нахождение в воздухе
        #if in_air: self.in_air+=1
        #else: self.in_air=0
        self.velocity.y-=self.in_air*self.g_acceleration
        self.x+=self.velocity.x
        self.y+=self.velocity.y
        self.velocity.x=0
        self.velocity.y=0





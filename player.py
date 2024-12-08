import vector
import pygame

class Player():
    def __init__(self,chosen_color):
        self.color=chosen_color
        if self.color=='blue':
            movement_buttons={}
        else:
            movement_buttons={}
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
    def handle_movement(self,**kwargs): pass




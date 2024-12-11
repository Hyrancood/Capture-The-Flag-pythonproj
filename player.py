import vector
import pygame

G_ACCELERATION = 0.2


class Player():
    def __init__(self,chosen_color):
        self.color=chosen_color
        self.in_air=0
        if self.color=='red':
            self.movement_buttons = {1073741903:'right', 1073741904:'left', 1073741906:'up'}
        else:
            self.movement_buttons = {100:'right', 97:'left', 119:'up'}
        self.rect=pygame.Rect(0,0,32,64)
        self.first_ability=None
        self.second_ability=None
        self.speed=3.7
        self.velocity=vector.Vector()

    def set_abilities(self,abilities):
        for i1 in range(len(abilities)):
            if abilities[i1] == 1:
                self.first_ability=i1
                for i2 in range(i1+1,len(abilities)):
                    if abilities[i2] == 1:
                        self.second_ability=i2

    def set_position(self,x_set,y_set):
        self.rect.move(x_set, y_set)

    def opposite(self):
        if self.color=='red':
            return 'blue'
        else: return 'red'

    def is_on_ground(self, platforms):
        test_pos = [self.rect.bottomleft, self.rect.midbottom, self.rect.bottomright]
        return any(any(platform.collidepoint((pos[0], pos[1]+1)) for pos in test_pos) for platform in platforms)


    def update(self,**kwargs):
        #self.handle_events(kwargs['events'])
        self.handle_movement(**kwargs)

    def handle_movement(self,**kwargs):
        on_ground = self.is_on_ground(kwargs['platforms'])
        if not on_ground:
            self.velocity.y += G_ACCELERATION
        else:
            self.velocity.y = 0
        for event in kwargs['events']:
            if event.type == pygame.KEYDOWN:
                if self.movement_buttons.get(event.key)=='right':
                    self.velocity.x+=self.speed
                if self.movement_buttons.get(event.key)=='left':
                    self.velocity.x-=self.speed
                if self.movement_buttons.get(event.key)=='up' and on_ground:
                    self.velocity.y-=self.speed*2.3
            if event.type == pygame.KEYUP:
                if self.movement_buttons.get(event.key)=='right':
                    self.velocity.x-=self.speed
                if self.movement_buttons.get(event.key)=='left':
                    self.velocity.x+=self.speed
                #if self.movement_buttons.get(event.key)=='up':
                #    self.velocity.y = 0
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        #print(f'{self.color}: x:{self.x} y: {self.y}, vel_x:{self.velocity.x} vel_y:{self.velocity.y}')





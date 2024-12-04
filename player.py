import vector
class Player():
    def __init__(self):
        self.first_ability=None
        self.second_ability=None
        self.x=0
        self.y=0
        self.velocity=vector.Vector()
        self.rect=pygame.Rect()
    def set_abilities(self,abilities):
        for i1 in range(len(abilities)):
            if abilities[i1] == 1:
                self.first_ability=i1
                for i2 in range(i1+1,len(abilities)):
                    if abilities[i2] == 1:
                        self.second_ability=i2
    def set_start_position(self,x_start,y_start):
        self.x=x_start
        self.y=y_start


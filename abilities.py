class Abilities:
    def swap(self,p1,p2):
        if p1.distance(p2)<=100 and p1.cooldown['swap']==0:
            p1.rect, p2.rect = p2.rect, p1.rect
            p1.cooldown['swap']=600

    def freeze_activate(self,p1,p2):
        if p1.distance(p2)<=200 and p1.cooldown['freeze']==0:
            p1.speed/=2
            p1.cooldown['freeze']=900
    
    def freeze_deactivate(self,p2):
        p2.speed*=2
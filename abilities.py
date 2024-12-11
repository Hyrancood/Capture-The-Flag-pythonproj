class Freeze:
    def activate(self,p1,p2):
        if ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**0.5<=200:
            p2.speed/=2
    def deactivate(self,p2):
        p2.speed*=2

'''
Final Project
'''
from collections import Counter
from math import floor
from ggame import App, Color, LineStyle, Sprite, RectangleAsset, CircleAsset, EllipseAsset, PolygonAsset, ImageAsset, MouseEvent, Frame

red = Color(0xff0000, 1.0)
green = Color(0x00ff00, 1.0)
black = Color(0x000000, 1.0)
white=Color(0xffffff,1.0)
yellow=Color(0xffff00,1.0)

thinline = LineStyle(1, black)
noline=LineStyle(0,white)

class Background(App):
    def __init__(self,width,height):
        super().__init__(width,height)
        background=RectangleAsset(width, height, noline, black)
        bg=Sprite(background, (0,0))

class Pacman(Sprite):
    #pacman=CircleAsset(5,noline,yellow)
    pacman=RectangleAsset(20,10,noline,yellow)
    def __init__(self,position):
        super().__init__(Pacman.pacman,position)
        self.vx=1
        self.vy=1
        self.vr=0.01
        
    def step(self):
        self.x+=self.vx
        self.y+=self.vy
        self.r+=self.vr
        
        

myapp=Background(700,500) #Needs to go first so sprites show on top of it

Pacman((100,100))
myapp.run()








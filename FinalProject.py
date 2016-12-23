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



class Pacman(Sprite):
    pacman=CircleAsset(10,noline,yellow)
    #pacman=RectangleAsset(20,10,noline,yellow)
    def __init__(self,position):
        super().__init__(Pacman.pacman,position)
        self.position=position
        self.vx=0
        self.vy=0
        self.vr=0
        self.moving=0
        self.movingframe=1
        
        '''
        When keys are pressed
        '''
        
        PacmanGame.listenKeyEvent("keydown","right arrow", self.rightmoving)
        PacmanGame.listenKeyEvent("keydown","left arrow",self.leftmoving)
        PacmanGame.listenKeyEvent("keydown","down arrow",self.downmoving)
        PacmanGame.listenKeyEvent("keydown","up arrow",self.upmoving)
        '''
        When keys are released
        '''

    '''
    When keys are pressed they do these things
    '''
    
    def rightmoving(self,event):
            self.vx=1
            self.vy=0
            
    def leftmoving(self,event):
            self.vx=-1
            self.vy=0
            
    def downmoving(self,event):
            self.vy=1
            self.vx=0
            
    def upmoving(self,event):
            self.vy=-1
            self.vx=0
            
    '''
    When keys are released they do these things
    '''
    
    def step(self):
        self.x+=self.vx
        self.y+=self.vy
        self.rotation+=self.vr
    
    #def collision(self,position):
     #   if self.position==(200,y):
       #     self.vx=0

class PacmanGame(App):
    def __init__(self,width,height):
        super().__init__(width,height)
        background=RectangleAsset(width, height, noline, black)
        bg=Sprite(background, (0,0))
        
    def step(self):
        for pman in self.getSpritesbyClass(Pacman):
            pman.step()
        
        
class OtherSprites(Sprite):
    def __init__(self):
        wall=RectangleAsset(10,200,noline,white)
        wallsprite=Sprite(wall, (200,25))
        

myapp=PacmanGame(700,500) #Needs to go first so sprites show on top of it

Pacman((100,100))
OtherSprites()
myapp.run()








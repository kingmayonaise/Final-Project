#import pygame, random
#from pygame.locals import *

import random
from ggame import App, Color, LineStyle, Sprite, LineAsset, RectangleAsset, CircleAsset, PolygonAsset, ImageAsset, Frame

red = Color(0xff0000, 1.0)
green = Color(0x00ff00, 1.0)
black = Color(0x000000, 1.0)
white=Color(0xffffff,1.0)
yellow=Color(0xffff00,1.0)

thinline = LineStyle(1, black)
noline=LineStyle(0,white)

   
cLevel=0.0
cLeveli=int(cLevel)
   
cWidth=int(round(12*(1+cLevel*0.4),0))
cHeight=int(round(9*(1+cLevel*0.4),0))
cCellSize=16

aCellWallH=LineAsset(cCellSize,0,thinline)
aCellWallV=LineAsset(0,cCellSize,thinline)

    
def incGlobals():
    global cLevel
    global cLeveli
    
             
    global cWidth
    global cHeight
    global cCellSize

    cLevel+=1
    cLeveli=int(cLevel)
    
    cWidth=int(round(12*(1+cLevel*0.4),0))
    cHeight=int(round(9*(1+cLevel*0.4),0))


class Layout(object):
    def __init__(self, pScreen):
        self.dimX=cWidth #20 #40
        self.dimY=cHeight #10 #30
        self.cellSize=cCellSize
        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]
        self.totalCells = self.dimX*self.dimY # 40 * 30
        #self.mLayer = pygame.Surface(pScreen.get_size())
        #self.mLayer = self.mLayer.convert_alpha()
        #self.mLayer.fill((0, 0, 0, 0))
        
        #self.sLayer = pygame.Surface(pScreen.get_size())
        #self.sLayer = self.sLayer.convert_alpha()
        #self.sLayer.fill((0, 0, 0, 0))

        self.currentCell = random.randint(0, self.totalCells-1)

    def myLocation(self):
        return self.currentCell
     
class Maze(Layout):
    
    def __init__(self, pScreen):
        super(Maze,self).__init__(pScreen)
        self.mazeArray = []
        self.ghostArray=[]
        self.ghostLocations=[]
        self.bubbleArray=[]
        self.cellStack = []
        self.visitedCells = 1
        self.score=0
        self.mScreen=pScreen
        
        self.bubbleArray=random.sample(range(1, self.totalCells-1), 1)
        
        for y in range(self.dimY): # 80 wide + 60 tall
            #pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*self.cellSize), (self.dimX*self.cellSize, y*self.cellSize))
            for x in range(self.dimX):
                self.mazeArray.append(0)
                if ( y == 0 ):
                    pass
                    #pygame.draw.line(self.mLayer, (0,0,0,255), (x*self.cellSize,0), (x*self.cellSize,self.dimY*self.cellSize))
        while(self.visitedCells < self.totalCells):
            x = int(self.currentCell % self.dimX)
            y = int(self.currentCell / self.dimX)
            neighbors = []
            for i in range(4):
                nx = x + self.compass[i][0]
                ny = y + self.compass[i][1]
                if ((nx >= 0) and (ny >= 0) and (nx < self.dimX) and (ny < self.dimY)):
                    if (self.mazeArray[(ny*self.dimX+nx)] & 0x000F) == 0:
                        nidx = ny*self.dimX+nx
                        neighbors.append((nidx,1<<i))
            if len(neighbors) > 0:
                idx = random.randint(0,len(neighbors)-1)
                nidx,direction = neighbors[idx]
                dx = x*self.cellSize
                dy = y*self.cellSize
                if direction & 1:
                    self.mazeArray[nidx] |= (4)
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx,dy+1),(dx,dy+self.cellSize-1))
                elif direction & 2:
                    self.mazeArray[nidx] |= (8)
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy+self.cellSize),(dx+self.cellSize-1,dy+self.cellSize))
                elif direction & 4:
                    self.mazeArray[nidx] |= (1)
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx+self.cellSize,dy+1),(dx+self.cellSize,dy+self.cellSize-1))
                elif direction & 8:
                    self.mazeArray[nidx] |= (2)
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy),(dx+self.cellSize-1,dy))
                self.mazeArray[self.currentCell] |= direction
                self.cellStack.append(self.currentCell)
                self.currentCell = nidx
                self.visitedCells = self.visitedCells + 1
            else:
                self.currentCell = self.cellStack.pop()
                
        for i in range(cLeveli):     
            ghost1=Ghost(self.mScreen,self.getMazeArray(), self.getCellStack())
            self.addGhost(ghost1)
        
    def drawBubbles(self):
        for bubbleCell in self.bubbleArray:
            dx = (bubbleCell % self.dimX)*self.cellSize
            dy = (bubbleCell / self.dimX)*self.cellSize
            #pygame.draw.circle(self.sLayer, (0,0,255,200), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/4)

    def drawGhosts(self):
        for g in self.ghostArray:
            gCell=g.myLocation()
            dx = (gCell % self.dimX)*self.cellSize
            dy = (gCell / self.dimX)*self.cellSize
            #pygame.draw.rect(self.sLayer, (0,255,0,255), Rect(dx+self.cellSize/4,dy+self.cellSize/4,self.cellSize/2,self.cellSize/2))
            
    def drawPacman(self):
        pCell=self.Pacman.myLocation()
        dx = (pCell % self.dimX)*self.cellSize
        dy = (pCell / self.dimX)*self.cellSize
        if self.Pacman.getState()=='Playing':
            pass
            #pygame.draw.circle(self.sLayer, (250,240,0,250), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/2-1)
        elif self.Pacman.getState()=='Lost':
            pass
            #pygame.draw.circle(self.sLayer, (211,211,211,250), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/2-1)
        elif self.Pacman.getState()=='Won':
            pass
            #pygame.draw.circle(self.sLayer, (0,255,255,250), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/2-1)
            
            
    def getMazeArray(self):
        return self.mazeArray[:]

    def getCellStack(self):
        return self.cellStack[:]
    
    def addGhost(self, pGhost):
        self.ghostArray.append(pGhost)

    def addPacman(self, pPacman):
        self.Pacman=pPacman

                    
    def draw(self,screen):
        #self.sLayer.fill((0, 0, 0, 0))

        self.drawBubbles()
        self.drawGhosts()                
        self.drawPacman()        
        
        #screen.blit(self.sLayer, (0,0))
        #screen.blit(self.mLayer, (0,0))
        
    def checkCollisions(self):
        self.ghostLocations=[]
        ghostLocation=0
        pCell=self.Pacman.myLocation()

        for g in self.ghostArray:
            g.update()
            ghostLocation=g.myLocation()
            if ghostLocation==self.totalCells-1:
                self.ghostArray.remove(g)
                ghost1=Ghost(self.mScreen,self.getMazeArray(), self.getCellStack())
                self.addGhost(ghost1)
            else:
                self.ghostLocations.append(ghostLocation)
        
        if pCell in self.ghostLocations:
            self.Pacman.setState('Lost')
            return
         
        if pCell in self.bubbleArray:
            self.score +=1
            self.bubbleArray.remove(pCell)
            if len(self.bubbleArray)==0:
                self.Pacman.setState('Won')

class Ghost(Layout):
        
    def __init__(self, pScreen, mArray, cStack):
        super(Ghost,self).__init__(pScreen)
        self.mazeArray = mArray
        self.cellStack=cStack
        
    def update(self):
        if self.currentCell == (self.totalCells-1): # have we reached the exit?            
            return
        moved = False
        while(moved == False):
            x = self.currentCell % self.dimX
            y = self.currentCell / self.dimX
            neighbors = []
            directions = self.mazeArray[self.currentCell] & 0xF
            for i in range(4):
                if (directions & (1<<i)) > 0:
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]
                    if ((nx >= 0) and (ny >= 0) and (nx < self.dimX) and (ny < self.dimY)):              
                        nidx = ny*self.dimX+nx
                        if ((self.mazeArray[nidx] & 0xFF00) == 0): # make sure there's no backtrack
                            neighbors.append((nidx,1<<i))
            if len(neighbors) > 0:
                idx = random.randint(0,len(neighbors)-1)
                nidx,direction = neighbors[idx]
                if direction & 1:
                    self.mazeArray[nidx] |= (4 << 12)
                elif direction & 2:
                    self.mazeArray[nidx] |= (8 << 12)
                elif direction & 4:
                    self.mazeArray[nidx] |= (1 << 12)
                elif direction & 8:
                    self.mazeArray[nidx] |= (2 << 12)
                self.mazeArray[self.currentCell] |= direction << 8
                self.cellStack.append(self.currentCell)
                self.currentCell = nidx
                moved = True
            else:
                self.mazeArray[self.currentCell] &= 0xF0FF # not a solution
                self.currentCell = self.cellStack.pop()
                                

class Pacman(Layout):
        
    def __init__(self, pScreen, mArray, cStack):
        super(Pacman,self).__init__(pScreen)
        self.mazeArray = mArray
        self.cellStack=cStack
        self.state='Playing'
        
    def update(self, uDirection):
        
        if self.state=='Lost':
            return
        
        x = self.currentCell % self.dimX
        y = self.currentCell / self.dimX
        dx = x*self.cellSize
        dy = y*self.cellSize
        
        neighbors = []
        directions = self.mazeArray[self.currentCell] & 0xF
        for i in xrange(4):
            if (directions & (1<<i)) > 0:
                nx = x + self.compass[i][0]
                ny = y + self.compass[i][1]
                
                if ((nx >= 0) and (ny >= 0) and (nx < self.dimX) and (ny < self.dimY)): 
                    nidx = ny*self.dimX+nx
                    nX=(nidx % self.dimX)*self.cellSize
                    nY=(nidx / self.dimX)*self.cellSize
                     
                    if (uDirection==K_UP) and (nY<dy):
                        neighbors.append((nidx,1<<i))
                                           
                    elif (uDirection==K_DOWN) and (nY>dy):
                        neighbors.append((nidx,1<<i))
                        
                    elif (uDirection==K_RIGHT) and (nX>dx):
                        neighbors.append((nidx,1<<i))
                        
                    elif (uDirection==K_LEFT) and (nX<dx):
                        neighbors.append((nidx,1<<i))
                     
                         
        if len(neighbors) > 0:
            nidx,direction = neighbors[0]
            if direction & 1:
                self.mazeArray[nidx] |= (4 << 12)
            elif direction & 2:
                self.mazeArray[nidx] |= (8 << 12)
            elif direction & 4:
                self.mazeArray[nidx] |= (1 << 12)
            elif direction & 8:
                self.mazeArray[nidx] |= (2 << 12)
             
            self.mazeArray[self.currentCell] |= direction << 8
            self.cellStack.append(self.currentCell)
            self.currentCell = nidx
            
    def getState(self):
        return self.state

    def setState(self,pState):
        self.state=pState


class MazeGame(App):


    def __init__(self, width, height):
        super().__init__(width, height)
        bg_asset = RectangleAsset(width, height, noline, black)
        bg = Sprite(bg_asset, (0,0))
        
    def step(self)
        gState='Play'
        while gState=='Play':
            incGlobals()       
            #pygame.init()        
            screen = 1 #pygame.display.set_mode((cWidth*cCellSize, cHeight*cCellSize))
            #pygame.display.set_caption('Labyrinth: level '+str(cLeveli))
            #pygame.mouse.set_visible(0)
            #background = pygame.Surface(screen.get_size())
            #background = background.convert()
            #background.fill((255, 255, 255))
            
            newMaze = Maze(screen)
            myPacman=Pacman(screen,newMaze.getMazeArray(), newMaze.getCellStack())
            newMaze.addPacman(myPacman)
        
            #screen.blit(background, (0, 0))
            #pygame.display.flip()
            #clock = pygame.time.Clock()
            while 1:
                #clock.tick(2)
                #screen.blit(background, (0, 0))
                #for event in pygame.event.get():
                #    if event.type == QUIT:
                #        return
                #    elif event.type == KEYDOWN and event.key in (K_UP,K_DOWN,K_RIGHT,K_LEFT):
                #        myPacman.update(event.key)
                #    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                #        return
                if myPacman.getState() =='Playing':
                    newMaze.checkCollisions()
                
                newMaze.draw(screen)
                #pygame.display.flip()
                if myPacman.getState()=='Won':
                    #pygame.display.quit()
                    #pygame.quit()
                    break
                else:
                    break
                
            break

if __name__ == '__main__': main()
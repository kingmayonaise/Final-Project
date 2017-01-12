#import pygame, random
#from pygame.locals import *

import random
from ggame import App, Color, LineStyle, Sprite, LineAsset, RectangleAsset, CircleAsset, PolygonAsset, Frame, KeyEvent

red = Color(0xff0000, 1.0)
green = Color(0x00ff00, 1.0)
blue = Color(0x0000ff, 1.0)
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

aCellWallH = LineAsset(cCellSize,0,thinline)
aCellWallV = LineAsset(0,cCellSize,thinline)
aBubble    = CircleAsset(cCellSize/4,noline,blue)
aGhost     = RectangleAsset(cCellSize/2,cCellSize/2,noline,green)
aRunner    = CircleAsset(cCellSize/2-1,noline,yellow)
    
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
    compass = [(-1,0),(0,1),(1,0),(0,-1)]
    
    def __init__(self):
        self.dimX=cWidth #20 #40
        self.dimY=cHeight #10 #30
        self.cellSize=cCellSize
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
    
    def __init__(self):
        super(Maze,self).__init__()
        self.mazeArray = []
        self.ghostArray=[]
        self.ghostLocations=[]
        self.bubbleArray=[]
        self.cellStack = []
        self.visitedCells = 1
        self.score=0
        self.mazeDict={}
        
        self.bubbleArray=random.sample(range(1, self.totalCells-1), 1)

        bg_asset = RectangleAsset(cWidth*cCellSize, cHeight*cCellSize, thinline, white)
        bg = Sprite(bg_asset, (0,0))

        
        for y in range(self.dimY): # 80 wide + 60 tall
            for x in range(self.dimX):
                self.mazeDict['H:'+str(x)+':'+str(y)]=Sprite(aCellWallH,(x*self.cellSize, y*self.cellSize))
            #pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*self.cellSize), (self.dimX*self.cellSize, y*self.cellSize))
            for x in range(self.dimX):
                self.mazeArray.append(0)
                if ( y == 0 ):
                    for yi in range(self.dimY):
                        self.mazeDict['V:'+str(x)+':'+str(yi)]=Sprite(aCellWallV,(x*self.cellSize, yi*self.cellSize))
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
                    self.mazeDict['V:'+str(x)+':'+str(y)].destroy()
                    del self.mazeDict['V:'+str(x)+':'+str(y)]
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx,dy+1),(dx,dy+self.cellSize-1))
                elif direction & 2:
                    self.mazeArray[nidx] |= (8)
                    self.mazeDict['H:'+str(x)+':'+str(y+1)].destroy()
                    del self.mazeDict['H:'+str(x)+':'+str(y+1)]
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy+self.cellSize),(dx+self.cellSize-1,dy+self.cellSize))
                elif direction & 4:
                    self.mazeArray[nidx] |= (1)
                    self.mazeDict['V:'+str(x+1)+':'+str(y)].destroy()
                    del self.mazeDict['V:'+str(x+1)+':'+str(y)]
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx+self.cellSize,dy+1),(dx+self.cellSize,dy+self.cellSize-1))
                elif direction & 8:
                    self.mazeArray[nidx] |= (2)
                    self.mazeDict['H:'+str(x)+':'+str(y)].destroy()
                    del self.mazeDict['H:'+str(x)+':'+str(y)]
                    
                    #pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy),(dx+self.cellSize-1,dy))
                self.mazeArray[self.currentCell] |= direction
                self.cellStack.append(self.currentCell)
                self.currentCell = nidx
                self.visitedCells = self.visitedCells + 1
            else:
                self.currentCell = self.cellStack.pop()
        
        for i in range(cLeveli):
            
            self.ghost1=Ghost(self.getMazeArray(), self.getCellStack())
            self.ghostArray.append(self.ghost1)
        
        self.drawBubbles()
        
    def drawBubbles(self):
        for bubbleCell in self.bubbleArray:
            
            dx = int(bubbleCell % self.dimX)*self.cellSize+self.cellSize/2
            dy = int(bubbleCell / self.dimX)*self.cellSize+self.cellSize/2
            Sprite(aBubble, (dx,dy))
            #pygame.draw.circle(self.sLayer, (0,0,255,200), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/4)

    def runGhosts(self):
        self.ghost1.update()
        #for g in self.ghostArray:
        #print('inside run')
        #    print (self.ghostArray)
        #    print(g)
            #g.update()
        #pygame.draw.rect(self.sLayer, (0,255,0,255), Rect(dx+self.cellSize/4,dy+self.cellSize/4,self.cellSize/2,self.cellSize/2))
            
    def drawRunner(self):
        
        dx = int(self.currentCell % self.dimX)*self.cellSize
        dy = int(self.currentCell / self.dimX)*self.cellSize
        if self.Runner.getState()=='Playing':
            pass
            #pygame.draw.circle(self.sLayer, (250,240,0,250), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/2-1)
        elif self.Runner.getState()=='Lost':
            pass
            #pygame.draw.circle(self.sLayer, (211,211,211,250), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/2-1)
        elif self.Runner.getState()=='Won':
            pass
            #pygame.draw.circle(self.sLayer, (0,255,255,250), (dx+self.cellSize/2,dy+self.cellSize/2),self.cellSize/2-1)
            
            
    def getMazeArray(self):
        return self.mazeArray[:]

    def getCellStack(self):
        return self.cellStack[:]
    
    def addRunner(self, pRunner):
        self.Runner=pRunner

                    
    def draw(self):
        #self.sLayer.fill((0, 0, 0, 0))

        self.drawBubbles()
        self.drawGhosts()                
        self.drawRunner()        
        
        #screen.blit(self.sLayer, (0,0))
        #screen.blit(self.mLayer, (0,0))
        
    def checkCollisions(self):
        runnerSprite=self.Runner.getSprite()
        ghostSprite=self.ghost1.getSprite()
        
        if runnerSprite.collidingWith(ghostSprite):
            print ('collding')
        else:
            print ('lucky')
 
    
        """self.ghostLocations=[]
        ghostLocation=0
        pCell=self.Runner.myLocation()

        for g in self.ghostArray:
            g.update()
            ghostLocation=g.myLocation()
            if ghostLocation==self.totalCells-1:
                self.ghostArray.remove(g)
                ghost1=Ghost(self.getMazeArray(), self.getCellStack())
                self.addGhost(ghost1)
            else:
                self.ghostLocations.append(ghostLocation)
        
        if pCell in self.ghostLocations:
            self.Runner.setState('Lost')
            return
         
        if pCell in self.bubbleArray:
            self.score +=1
            self.bubbleArray.remove(pCell)
            if len(self.bubbleArray)==0:
                self.Runner.setState('Won')
        """
class Ghost(Layout):
        
    def __init__(self,mArray, cStack):
        super(Ghost,self).__init__()
        self.mazeArray = mArray
        self.cellStack=cStack

        dx = int(self.currentCell % self.dimX)*self.cellSize+int(self.cellSize/4)
        dy = int(self.currentCell / self.dimX)*self.cellSize+int(+self.cellSize/4)
        self.gImage=Sprite(aGhost,(dx,dy))


    def update(self):
        if self.currentCell == (self.totalCells-1): # have we reached the exit?            
            return
        moved = False
        while(moved == False):
            x = int(self.currentCell % self.dimX)
            y = int(self.currentCell / self.dimX)
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

                                
        dx = int(self.currentCell % self.dimX)*self.cellSize+int(self.cellSize/4)
        dy = int(self.currentCell / self.dimX)*self.cellSize+int(+self.cellSize/4)
        self.gImage.x=dx
        self.gImage.y=dy
        
    def getSprite(self):
        return self.gImage

class Runner(Layout):
        
    def __init__(self, mArray, cStack):
        super(Runner,self).__init__()
        self.mazeArray = mArray
        self.cellStack=cStack
        self.state='Playing'
        dx = int(self.currentCell % self.dimX)*self.cellSize+self.cellSize/2
        dy = int(self.currentCell / self.dimX)*self.cellSize+self.cellSize/2
        self.rImage=Sprite(aRunner, (dx, dy))
        
    def update(self, uDirection):
        
        if self.state=='Lost':
            return
        
        x = int(self.currentCell % self.dimX)
        y = int(self.currentCell / self.dimX)
        dx = x*self.cellSize
        dy = y*self.cellSize
        
        neighbors = []
        directions = self.mazeArray[self.currentCell] & 0xF
        for i in range(4):
            if (directions & (1<<i)) > 0:
                nx = x + self.compass[i][0]
                ny = y + self.compass[i][1]
                
                if ((nx >= 0) and (ny >= 0) and (nx < self.dimX) and (ny < self.dimY)): 
                    nidx = ny*self.dimX+nx
                    nX=int(nidx % self.dimX)*self.cellSize
                    nY=int(nidx / self.dimX)*self.cellSize
                     
                    if (uDirection=='up') and (nY<dy):
                        neighbors.append((nidx,1<<i))
                                           
                    elif (uDirection=='down') and (nY>dy):
                        neighbors.append((nidx,1<<i))
                        
                    elif (uDirection=='right') and (nX>dx):
                        neighbors.append((nidx,1<<i))
                        
                    elif (uDirection=='left') and (nX<dx):
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

        dx = int(self.currentCell % self.dimX)*self.cellSize+self.cellSize/2
        dy = int(self.currentCell / self.dimX)*self.cellSize+self.cellSize/2
        self.rImage.x=dx
        self.rImage.y=dy

            
    def getState(self):
        return self.state

    def setState(self,pState):
        self.state=pState
        
    def getSprite(self):
        return self.rImage


class MazeGame(App):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.startRun()
        self.steps=0
        self.listenKeyEvent('keydown', 'escape', self.stopRun)
        keys=["left arrow", "right arrow", "up arrow", "down arrow"]
        commands = ["left", "right", "up", "down"]
        self.keymap = dict(zip(keys, commands))
        [self.listenKeyEvent("keydown", k, self.runnerRuns) for k in keys]
        #[self.listenKeyEvent("keyup", k, self.controlup) for k in keys]
        
    def startRun(self):
        
        incGlobals()
        self.newMaze = Maze()
        self.myRunner=Runner(self.newMaze.getMazeArray(), self.newMaze.getCellStack())
        self.newMaze.addRunner(self.myRunner)

    def step(self):
        self.steps+=1
        if ((self.steps % 25) == 0):
            self.newMaze.runGhosts()
        self.newMaze.checkCollisions()
            
    def runnerRuns(self, evt):
        self.myRunner.update(self.keymap[evt.key])
        evt.consumed=True
        
            
    def stopRun(self,evt):
        print (evt)
        evt.consumed=True


myapp = MazeGame(600,600)
myapp.run()
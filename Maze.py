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

cCellSize=16

aCellWallH = LineAsset(cCellSize,0,thinline)
aCellWallV = LineAsset(0,cCellSize,thinline)
aBubble    = CircleAsset(cCellSize/4,noline,blue)
aGhost     = RectangleAsset(cCellSize/2,cCellSize/2,noline,red)
aRunner    = CircleAsset(cCellSize/2-1,noline,yellow)

compass = [(-1,0),(0,1),(1,0),(0,-1)]

cLevel=0.0
cLeveli=int(cLevel)
   
cWidth=0
cHeight=0
cTotalCells=0


    
def incGlobals(start=0):
    global cLevel
    global cLeveli
    global cWidth
    global cHeight
    global cTotalCells
    
    cLevel+=1
    cLeveli=int(cLevel)
    
    cWidth=int(round(12*(1+cLevel*0.4),0))
    cHeight=int(round(9*(1+cLevel*0.4),0))
    cTotalCells=cWidth*cHeight

class Trophy(Sprite):
        
    def __init__(self,trophyCell):
        x = int(trophyCell % cWidth)*cCellSize+cCellSize/2
        y = int(trophyCell / cWidth)*cCellSize+cCellSize/2
        super().__init__(aBubble, (x, y))

class Maze():
    
    def __init__(self):
        self.mazeArray = []
        self.ghostArray=[]
        self.ghostLocations=[]
        self.bubbleArray=[]
        self.cellStack = []
        self.visitedCells = 1
        self.score=0
        self.mazeDict={}
        self.currentCell = 0       
        self.bubbleArray=random.sample(range(1, cTotalCells-1), 1)

        bg_asset = RectangleAsset(cWidth*cCellSize, cHeight*cCellSize, thinline, white)
        bg = Sprite(bg_asset, (0,0))

        
        for y in range(cHeight):
            for x in range(cWidth):
                self.mazeDict['H:'+str(x)+':'+str(y)]=Sprite(aCellWallH,(x*cCellSize, y*cCellSize))
            for x in range(cWidth):
                self.mazeArray.append(0)
                if ( y == 0 ):
                    for yi in range(cHeight):
                        self.mazeDict['V:'+str(x)+':'+str(yi)]=Sprite(aCellWallV,(x*cCellSize, yi*cCellSize))
        while(self.visitedCells < cTotalCells):
            x = int(self.currentCell % cWidth)
            y = int(self.currentCell / cWidth)
            neighbors = []
            for i in range(4):
                nx = x + compass[i][0]
                ny = y + compass[i][1]
                if ((nx >= 0) and (ny >= 0) and (nx < cWidth) and (ny < cHeight)):
                    if (self.mazeArray[(ny*cWidth+nx)] & 0x000F) == 0:
                        nidx = ny*cWidth+nx
                        neighbors.append((nidx,1<<i))
            if len(neighbors) > 0:
                idx = random.randint(0,len(neighbors)-1)
                nidx,direction = neighbors[idx]
                dx = x*cCellSize
                dy = y*cCellSize
                if direction & 1:
                    self.mazeArray[nidx] |= (4)
                    self.mazeDict['V:'+str(x)+':'+str(y)].destroy()
                    del self.mazeDict['V:'+str(x)+':'+str(y)]
                elif direction & 2:
                    self.mazeArray[nidx] |= (8)
                    self.mazeDict['H:'+str(x)+':'+str(y+1)].destroy()
                    del self.mazeDict['H:'+str(x)+':'+str(y+1)]
                elif direction & 4:
                    self.mazeArray[nidx] |= (1)
                    self.mazeDict['V:'+str(x+1)+':'+str(y)].destroy()
                    del self.mazeDict['V:'+str(x+1)+':'+str(y)]
                elif direction & 8:
                    self.mazeArray[nidx] |= (2)
                    self.mazeDict['H:'+str(x)+':'+str(y)].destroy()
                    del self.mazeDict['H:'+str(x)+':'+str(y)]
                    
                self.mazeArray[self.currentCell] |= direction
                self.cellStack.append(self.currentCell)
                self.currentCell = nidx
                self.visitedCells = self.visitedCells + 1
            else:
                self.currentCell = self.cellStack.pop()
        
        for i in range(cLeveli):
            self.ghost1=Ghost(self.getMazeArray(), self.getCellStack())
            self.ghostArray.append(self.ghost1)
        

        for bubbleCell in self.bubbleArray:
            Trophy (bubbleCell)
            
            
    def runGhosts(self):
        self.ghost1.update()
        #for g in self.ghostArray:
        #print('inside run')
        #    print (self.ghostArray)
        #    print(g)
            #g.update()
        #pygame.draw.rect(self.sLayer, (0,255,0,255), Rect(dx+cCellSize/4,dy+cCellSize/4,cCellSize/2,cCellSize/2))
            
    def drawRunner(self):
        
        dx = int(self.currentCell % cWidth)*cCellSize
        dy = int(self.currentCell / cWidth)*cCellSize
        if self.Runner.getState()=='Playing':
            pass
            #pygame.draw.circle(self.sLayer, (250,240,0,250), (dx+cCellSize/2,dy+cCellSize/2),cCellSize/2-1)
        elif self.Runner.getState()=='Lost':
            pass
            #pygame.draw.circle(self.sLayer, (211,211,211,250), (dx+cCellSize/2,dy+cCellSize/2),cCellSize/2-1)
        elif self.Runner.getState()=='Won':
            pass
            #pygame.draw.circle(self.sLayer, (0,255,255,250), (dx+cCellSize/2,dy+cCellSize/2),cCellSize/2-1)
            
            
    def getMazeArray(self):
        return self.mazeArray[:]

    def getCellStack(self):
        return self.cellStack[:]
    
    def addRunner(self, pRunner):
        self.Runner=pRunner

    def checkCollisions(self):

        if len(self.Runner.collidingWithSprites(Ghost))>0:
            self.Runner.setState('Lost')
            print ('lost')

        if len(self.Runner.collidingWithSprites(Trophy))>0:
            self.score +=1
            self.bubbleArray.remove(pCell)
            if len(self.bubbleArray)==0:
                self.Runner.setState('Won')
            print ('won')
            
            
    def selfDestruct(self):
        for k in self.mazeDict:
            self.mazeDict[k].destroy()

class Ghost(Sprite):
        
    def __init__(self,mArray, cStack):
        self.mazeArray = mArray
        self.cellStack=cStack
        self.currentCell = random.randint(0, cTotalCells-1)

        dx = int(self.currentCell % cWidth)*cCellSize+int(cCellSize/4)
        dy = int(self.currentCell / cWidth)*cCellSize+int(+cCellSize/4)
        super().__init__(aGhost, (dx, dy))


    def update(self):
        if self.currentCell == (cTotalCells-1): # have we reached the exit?            
            return
        moved = False
        while(moved == False):
            x = int(self.currentCell % cWidth)
            y = int(self.currentCell / cWidth)
            neighbors = []
            directions = self.mazeArray[self.currentCell] & 0xF
            for i in range(4):
                if (directions & (1<<i)) > 0:
                    nx = x + compass[i][0]
                    ny = y + compass[i][1]
                    if ((nx >= 0) and (ny >= 0) and (nx < cWidth) and (ny < cHeight)):              
                        nidx = ny*cWidth+nx
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

                                
        dx = int(self.currentCell % cWidth)*cCellSize+int(cCellSize/4)
        dy = int(self.currentCell / cWidth)*cCellSize+int(+cCellSize/4)
        self.x=dx
        self.y=dy
    
        
class Runner(Sprite):
        
    def __init__(self, mArray, cStack):
        self.mazeArray = mArray
        self.cellStack=cStack
        self.state='Playing'
        self.currentCell = random.randint(0, cTotalCells-1)        
        dx = int(self.currentCell % cWidth)*cCellSize+cCellSize/2
        dy = int(self.currentCell / cWidth)*cCellSize+cCellSize/2
        super().__init__(aRunner, (dx, dy))

        
    def update(self, uDirection):
        
        if self.state=='Lost':
            return
        
        x = int(self.currentCell % cWidth)
        y = int(self.currentCell / cWidth)
        dx = x*cCellSize
        dy = y*cCellSize
        
        neighbors = []
        directions = self.mazeArray[self.currentCell] & 0xF
        for i in range(4):
            if (directions & (1<<i)) > 0:
                nx = x + compass[i][0]
                ny = y + compass[i][1]
                
                if ((nx >= 0) and (ny >= 0) and (nx < cWidth) and (ny < cHeight)): 
                    nidx = ny*cWidth+nx
                    nX=int(nidx % cWidth)*cCellSize
                    nY=int(nidx / cWidth)*cCellSize
                     
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

        dx = int(self.currentCell % cWidth)*cCellSize+cCellSize/2
        dy = int(self.currentCell / cWidth)*cCellSize+cCellSize/2
        self.x=dx
        self.y=dy

            
    def getState(self):
        return self.state

    def setState(self,pState):
        self.state=pState
        
    def getSprite(self):
        return self.rImage

    def myLocation(self):
        return self.currentCell

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
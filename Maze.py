import ggame, random
from ggame.locals import *

class Maze:
	def __init__(self, mazeLayer):
		self.mazeArray = []
		self.state = 'idle'
		self.mLayer = mazeLayer
		self.mLayer.fill((0, 0, 0, 0)) # fill it with black translucent
		for y in xrange(60):
			pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*8), (640, y*8))
			for x in xrange(80):
				self.mazeArray.append(0x0000)
				if ( y == 0 ):
					pygame.draw.line(self.mLayer, (0, 0, 0, 255), (x*8, 0), (x*8, 480))
		self.totalCells = 4800
		self.cellStack = []

	def update(self):
		if self.state == 'idle':
			pass
		elif self.state == 'create':
			pass # start creating!
	
	def draw(self, screen):
		screen.blit(self.mLayer, (0, 0))

def main():
	pygame.init()
	screen = pygame.display.set_mode((640,480))
	pygame.display.set_caption('Tig Maze!')
	pygame.mouse.set_visible(0)

	background = pygame.surface(screen.get_size())
	background = background.convert()
	background.fill((255,255,255))

	mazeLayer = pygame.surface(screen.get_size())
	mazeLayer = mazeLayer.convert_alpha() # give it some alpha values
	mazeLayer.fill((0,0,0,0,))

	newMaze = Maze(mazeLayer)

	screen.blit(background, (0,0))
	pygame.display.flip()
	clock = pygame.time.Clock()
	
	while 1:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return
		newMaze.update()

		screen.blit(background, (0,0))
		newMaze.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()
import math
from AV_GameObject import GameObject

class Olivia(GameObject):
	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.basey = y
		self.loadImages()
		self.speed = 1

	def update(self,ticks):
		self.x = self.x - self.speed
		self.y = self.basey + math.sin(self.x * 1.0 / 100) * 20
		if self.x <  0 - self.width:
			self.x = self.windowWidth
			return True
		else:
			return False

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/olivia.png")
		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]	
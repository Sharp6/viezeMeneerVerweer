import math
from AV_GameObject import GameObject

class Olivia(GameObject):
	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.basey = y
		self.loadImages()
		self.speed = 1
		self.destinationCelebration = None

	def update(self,ticks):
		self.x = self.x - self.speed
		self.y = self.basey + math.sin(self.x * 1.0 / 100) * 20

		if(self.destinationCelebration is not None):
			if(self.destinationCelebration.update(ticks)):
				self.destinationCelebration = None

		if self.x <  0 - self.width:
			self.destinationCelebration = DestinationCelebration(10,self.basey,self.pygame,self.surface,self.windowWidth,self.windowHeight,ticks)
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

class DestinationCelebration(GameObject):
	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth,creationTick):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.creationTick = creationTick
		self.font = self.pygame.font.Font("assets/font.ttf", 50)
		self.text = self.font.render("+10!", 1, (10, 10, 10))
		self.pos = self.text.get_rect()
		self.scorePos.x = self.x
		self.scorePos.y = self.y

		self.interval = 5000

	def update(self,ticks):
		if ticks - self.creationTick > self.interval:
			return True
		else:
			return False

	def draw(self):
		self.surface.blit(self.text,self.pos)
		if(self.destinationCelebration is not None):
			self.destinationCelebration.draw()

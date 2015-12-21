import random
from AV_GameObject import GameObject

class Decor():
	def __init__(self,pygame,surface,windowWidth,windowHeight):
		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.clouds = []
		self.lastCloudCreated = 0
		self.cloudInterval = 4000

	def update(self,ticks):
		self.addClouds(ticks)
		self.updateClouds(ticks)

	def draw(self):
		for cloud in self.clouds:
			cloud.draw()

	def addClouds(self,ticks):
		if ticks - self.lastCloudCreated > self.cloudInterval:
			self.clouds.append(Cloud(self.windowWidth,random.randint(0,self.windowHeight), random.randint(1,3), self.pygame, self.surface,self.windowWidth,self.windowHeight))
			self.lastCloudCreated = ticks

	def updateClouds(self,ticks):
		for idx, cloud in enumerate(self.clouds):
			if cloud.x > 0 - cloud.width:
				cloud.update(ticks)
			else:
				del self.clouds[idx]

class Cloud(GameObject):
	def __init__(self,x,y,speed,pygame,surface,windowWidth,windowHeight):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		
		self.speed = 1
		self.speed = speed

		self.loadImages()
		self.setInitialPosition()
	
	def setInitialPosition(self):
		self.x -= self.width / 2

	def update(self,ticks):
		self.x -= self.speed

	def draw(self):
		self.surface.blit(self.image,(self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/cloud.png")
		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]
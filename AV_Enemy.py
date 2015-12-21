import random,math
from pygame.locals import Rect
from AV_GameObject import GameObject

class Enemy(GameObject):

	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.basey = y
		self.beginX = x
		
		self.loadImages()
		self.setInitialPosition()

		self.speed = 3
		self.fallSpeed = 9
		self.isHit = False

		self.broom = None
		self.landingAnimation = None
		
	def setInitialPosition(self):
		self.x -= self.width / 2
	
	def update(self,ticks):
		if self.isHit:
			if self.y > self.windowHeight + self.height:
				if (self.landingAnimation is None):
					self.landingAnimation = Landing(self.x,self.windowHeight-40,self.pygame,self.surface,self.windowWidth,self.windowHeight)
				else:
					if(self.landingAnimation.update(ticks)):
						self.x = self.beginX
						self.basey = random.randint(0,self.windowHeight)
						self.landingAnimation = None
						self.isHit = False
			else:
				self.y += self.fallSpeed
				self.broom.update(ticks)
		else:
			self.broom = None
			self.x -= self.speed
			self.y = self.basey + math.sin(self.x * 1.0 / 30) * 100

			if self.x < -self.width:
				self.x = self.beginX
				return True
			else:
				return False

	def draw(self):
		if self.isHit:
			self.surface.blit(self.fallingImage, (self.x, self.y))
			self.broom.draw()
			if(self.landingAnimation is not None): 
				self.landingAnimation.draw()
		else:	
			self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/enemy.png")
		self.fallingImage = self.pygame.image.load("assets/enemy_falling.png");
		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]

	def registerHit(self):
		if not self.isHit:
			self.broom = Broom(self.x,self.y,self.pygame,self.surface,self.windowHeight,self.windowWidth)
		self.isHit = True

class Landing(GameObject):
	def __init__(self,x,y,pygame,surface,windowWidth,windowHeight):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.x = x	
		self.pygame = pygame
		self.surface = surface
		self.windowHeight = windowHeight
		self.windowWidth = windowWidth

		self.image = None
		self.frameWidth = 175
		self.frameHeight = 250
		self.framesStartX = 0
		self.framesStartY = 0

		self.landingTick = None
		self.landingAnimationInterval = 50
		self.numberOfLandingAnimationFrames = 13
		self.currentFrameNumber = 0

		self.width = None
		self.height = None
		self.loadImages()
		self.y = self.windowHeight - (self.frameHeight - 10)

	def update(self,ticks):
		if self.landingTick is None:
			self.landingTick = ticks
		else:
			frameNumber = (ticks - self.landingTick) / self.landingAnimationInterval
			if (ticks - self.landingTick) / self.landingAnimationInterval < self.numberOfLandingAnimationFrames:
				self.currentFrameNumber = frameNumber
			else:
				return True
		return False

	def draw(self):
		frameX = self.currentFrameNumber * self.frameWidth + self.framesStartX
		frameY = self.framesStartY
		if frameX > self.width:
			frameY = frameY + (frameX / self.width) * self.frameHeight
			frameX = frameX % self.width
		frame = Rect(frameX, frameY, self.frameWidth, self.frameHeight)
		self.surface.blit(self.image, (self.x,self.y), frame)

	def loadImages(self):
		self.image = self.pygame.image.load("assets/dust.png")

		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]


class Broom(GameObject):
	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.x = x
		self.y = y
		self.pygame = pygame
		self.surface = surface
		self.windowHeight = windowHeight
		self.windowWidth = windowWidth

		self.loadImages()
		
		self.xSpeed = 3
		self.ySpeed = 9

	def update(self,ticks):
		self.x = self.x + self.xSpeed
		self.y = self.y + self.ySpeed

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/broom.png")

		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]
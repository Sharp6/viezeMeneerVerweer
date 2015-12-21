import random,math
from pygame.locals import Rect
from AV_GameObject import GameObject

class Enemy(GameObject):

	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.basey = y
		self.y = y
		self.beginX = x
		
		self.loadImages()
		self.setInitialPosition()

		self.speed = 3
		self.strategies = [ "SINUS", "STRAIGHT" ]
		self.strategy = None
		self.angle = None

		self.setStrategy()

		self.font = self.pygame.font.Font("assets/christmasFont.ttf", 20)
		self.strategyText = None
		self.strategyTextPos = None

		self.updateStrategyText()

		self.fallSpeed = 9
		self.isHit = False

		self.broom = None
		self.landingAnimation = None
		
	def setInitialPosition(self):
		self.x -= self.width / 2

	def setStrategy(self):
		self.strategy = self.strategies[random.randint(0,len(self.strategies)-1)]
		#self.strategy = "STRAIGHT"
		self.basey = random.randint(0,self.windowHeight)
		self.angle = random.randint(-2,2)
		self.y = self.basey

		treshold = 10

		if((self.basey - self.windowHeight / 2) > treshold):
			if self.angle > 0:
				self.angle = self.angle * -1
		elif((self.basey - self.windowHeight / 2) < treshold * -1):
			if self.angle < 0:
				self.angle = self.angle * -1

		print "Strategy: " + str(self.strategy) + ", angle: " + str(self.angle) + ", basey: " + str(self.basey)

	def updateStrategyText(self):
		self.strategyText = self.font.render(str(self.strategy) + " " + str(self.angle), 1, (10, 10, 10))
		self.strategyTextPos = self.strategyText.get_rect()
		self.strategyTextPos.centerx = self.x - self.width/2
		self.strategyTextPos.centery = self.y - self.height/2
	
	def update(self,ticks):
		self.updateStrategyText()
		if self.isHit:
			if self.y > self.windowHeight + self.height:
				if (self.landingAnimation is None):
					self.landingAnimation = Landing(self.x,self.windowHeight-40,self.pygame,self.surface,self.windowWidth,self.windowHeight)
				else:
					if(self.landingAnimation.update(ticks)):
						self.x = self.beginX
						self.landingAnimation = None
						self.isHit = False
						self.setStrategy()
			else:
				self.y += self.fallSpeed
				self.broom.update(ticks)
		else:
			self.broom = None
			self.x -= self.speed

			if self.strategy == "SINUS":
				self.y = self.basey + math.sin(self.x * 1.0 / 30) * 100
			elif self.strategy == "STRAIGHT":
				self.y = self.y + self.angle
			else:
				self.y = self.basey

			if self.x < -self.width:
				self.x = self.beginX
				return True
			else:
				return False

	def draw(self):
		self.surface.blit(self.strategyText, self.strategyTextPos)
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
		
		self.loadImages()
		
		self.xSpeed = random.randint(-2,4)
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
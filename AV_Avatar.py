import random, math
import projectiles

class GameObject():
	def __init__(x,y,pygame,surface,windowWidth,windowHeight):
		self.x = x
		self.y = y
		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight

class Player(GameObject):
	def __init__(self,x,y,pygame,surface,windowWidth,windowHeight):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)

		self.firing = False
		self.bullets = []
		self.bulletSpeed = 10

		self.offsetTimer = 400
		self.lastOffsetChange = 0
		self.offset = 0
		self.offsetRange = 5

		self.loadImages()
		self.setInitialPosition()

	def setInitialPosition(self):
		self.x += 10
		self.y -= self.height / 2

	def loadImages(self):
		self.image = self.pygame.image.load("assets/player_marie.png")
		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]

	def draw(self,ticks):
		self.drawBullets()
		# check offset
		if ticks - self.lastOffsetChange > self.offsetTimer:
			self.offset += 1
			self.offset = self.offset % 2
			self.lastOffsetChange = ticks

		self.surface.blit(self.image,(self.x,self.y + self.offset * self.offsetRange))

	def drawBullets(self):
		for idx, b in enumerate(self.bullets):
			b.move()
			b.draw()

			if b.x > self.windowWidth:
				if(idx < len(self.bullets)):
					del self.bullets[idx]

	def checkForHit(self, thingToCheckAgainst):
		bulletsToRemove = []
		isHit = False

		for idx, b in enumerate(self.bullets):
			if b.x > thingToCheckAgainst.x and b.x < thingToCheckAgainst.x + thingToCheckAgainst.width:
				if b.y + b.height > thingToCheckAgainst.y and b.y < thingToCheckAgainst.y + thingToCheckAgainst.height:
					thingToCheckAgainst.registerHit()
					bulletsToRemove.append(idx)
					isHit = True

		for usedBullet in bulletsToRemove:
			if(idx < len(self.bullets)):
				del self.bullets[usedBullet]

		return isHit

	def setPositionAbsolute(self,pos):
		self.y = pos[1] - self.height / 2

	def setPositionRelative(self,amount):
		self.y = self.y - amount
		if self.y < 0:
			self.y = 0
		if self.y > self.windowHeight - self.height:
			self.y = self.windowHeight - self.height

	def fire(self):
		if len(self.bullets) < 3:
			self.bullets.append(projectiles.Bullet(self.x + self.width / 2, self.y, self.pygame, self.surface, self.bulletSpeed))			

class Enemy():
	x = 0
	y = 0
	basey = 0.0
	image = None
	fallingImage = None
	pygame = None
	surface = None
	width = 0
	height = 0
	beginX = 500
	windowHeight = 0
	windowWidth = 0
	broom = None

	speed = 3
	fallSpeed = 9

	isHit = False

	def move(self):
		if self.isHit:
			if self.y > self.windowHeight + self.height:
				self.x = self.beginX
				self.basey = random.randint(0,self.windowHeight)
				self.isHit = False
			else:
				self.y += self.fallSpeed
				self.broom.move()
		else:
			self.broom = None
			self.x -= self.speed
			self.y = self.basey + math.sin(self.x * 1.0 / 30) * 100

			if self.x < -self.width:
				self.x = self.beginX

	def draw(self):
		if self.isHit:
			self.surface.blit(self.fallingImage, (self.x, self.y))
			self.broom.draw()
		else:	
			self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/enemy.png")
		self.fallingImage = self.pygame.image.load("assets/enemy_falling.png");

	def registerHit(self):
		if not self.isHit:
			self.broom = Broom(self.x,self.y,self.pygame,self.surface,self.windowHeight,self.windowWidth)
		self.isHit = True

	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		self.x = x
		self.basey = y
		self.pygame = pygame
		self.surface = surface
		self.beginX = x
		self.windowHeight = windowHeight
		self.windowWidth = windowWidth
		self.loadImages()

		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]

		self.x -= self.width / 2

class Broom():
	x = 0
	y = 0
	image = None
	pygame = None
	surface = None
	width = 0
	height = 0
	windowWidth = 500
	windowHeight = 0

	xSpeed = 3
	ySpeed = 9

	def move(self):
		self.x = self.x + self.xSpeed
		self.y = self.y + self.ySpeed

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/broom.png")

	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		self.x = x
		self.y = y
		self.pygame = pygame
		self.surface = surface
		self.windowHeight = windowHeight
		self.windowWidth = windowWidth
		self.loadImages()

		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]
		

class Olivia():
	x = 0
	y = 0
	basey = 0
	image = None
	pygame = None
	surface = None
	width = 0
	height = 0
	windowWidth = 500
	windowHeight = 0

	speed = 1

	def move(self):
		self.x = self.x - self.speed
		self.y = self.basey + math.sin(self.x * 1.0 / 100) * 20
		if self.x <  0 - self.width:
			self.x = self.windowWidth

		
	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/olivia.png")

	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		self.x = x
		self.basey = y
		self.y = y
		self.pygame = pygame
		self.surface = surface
		self.windowHeight = windowHeight
		self.windowWidth = windowWidth
		self.loadImages()

		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]

class Cloud():
	x = 0
	y = 0
	image = None
	pygame = None
	surface = None
	width = 0
	height = 0

	speed = 1

	def move(self):
		self.x -= self.speed

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/cloud.png")

	def __init__(self,x,y,speed,pygame,surface):
		self.x = x
		self.y = y
		self.speed = speed
		self.pygame = pygame
		self.surface = surface
		self.loadImages()

		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]

		self.x -= self.width / 2


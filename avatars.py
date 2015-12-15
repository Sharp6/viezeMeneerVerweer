import random, math
import projectiles

class Player():
	x = 0
	y = 0
	image = None
	pygame = None
	surface = None
	width = 0
	height = 0
	windowWidth = 0

	firing = False
	bullets = []
	bulletSpeed = 10

	offsetTimer = 400
	lastOffsetChange = 0
	offset = 0
	offsetRange = 5

	def loadImages(self):
		self.image = self.pygame.image.load("assets/player.png")

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
				del self.bullets[idx]

	def checkForHit(self, thingToCheckAgainst):
		bulletsToRemove = []

		for idx, b in enumerate(self.bullets):
			if b.x > thingToCheckAgainst.x and b.x < thingToCheckAgainst.x + thingToCheckAgainst.width:
				if b.y + b.height > thingToCheckAgainst.y and b.y < thingToCheckAgainst.y + thingToCheckAgainst.height:
					thingToCheckAgainst.registerHit()
					bulletsToRemove.append(idx)

		for usedBullet in bulletsToRemove:
			del self.bullets[usedBullet]

	def setPosition(self,pos):
		self.y = pos[1] - self.height / 2

	def moveY(self,amount):
		self.y = self.y + amount

	def fire(self):
		self.bullets.append(projectiles.Bullet(self.x + self.width / 2, self.y, self.pygame, self.surface, self.bulletSpeed))		

	def __init__(self,x,y,pygame,surface,windowWidth):
		self.x = x
		self.y = y
		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.loadImages()


		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]

		self.x += self.width + 10
		self.y -= self.height / 2

class Enemy():
	x = 0
	y = 0
	basey = 0.0
	image = None
	pygame = None
	surface = None
	width = 0
	height = 0
	beginX = 500
	windowHeight = 0

	speed = 3
	fallSpeed = 5

	isHit = False

	def move(self):
		if self.isHit:
			if self.y > self.windowHeight + self.height:
				self.x = self.beginX
				self.isHit = False
			else:
				self.y += self.fallSpeed
		else:
			self.x -= self.speed
			self.y = self.basey + math.sin(self.x * 1.0 / 30) * 100

			if self.x < -self.width:
				self.x = self.beginX

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def loadImages(self):
		self.image = self.pygame.image.load("assets/enemy.png")

	def registerHit(self):
		self.isHit = True

	def __init__(self,x,y,pygame,surface,windowHeight):
		self.x = x
		self.basey = y
		self.pygame = pygame
		self.surface = surface
		self.beginX = x
		self.windowHeight = windowHeight
		self.loadImages()

		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]

		self.x -= self.width / 2

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


from AV_GameObject import GameObject
from AV_Bullet import Bullet

class Player(GameObject):
	def __init__(self,x,y,pygame,surface,windowWidth,windowHeight):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)

		self.firing = False
		self.bullets = []
		self.bulletSpeed = 10

		self.yOffset = y
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

	def update(self,ticks):
		if ticks - self.lastOffsetChange > self.offsetTimer:
			self.offset += 1
			self.offset = self.offset % 2
			self.lastOffsetChange = ticks
		self.yOffset = self.y + self.offset * self.offsetRange

		for idx, b in enumerate(self.bullets):
			b.update(ticks)
			if b.x > self.windowWidth:
				if(idx < len(self.bullets)):
					del self.bullets[idx]

	def draw(self):
		self.drawBullets()
		self.surface.blit(self.image,(self.x,self.yOffset))

	def drawBullets(self):
		for idx, b in enumerate(self.bullets):
			b.draw()

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
			self.bullets.append(Bullet(self.x + self.width / 2, self.y, self.pygame, self.surface, self.windowWidth, self.windowHeight,self.bulletSpeed))			

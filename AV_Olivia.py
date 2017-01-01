import math, random
from AV_GameObject import GameObject

class Olivia(GameObject):
	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.basey = y
		self.loadImages()
		self.speed = 1
		self.destinationCelebration = None

		self.soundCounter = 0

	def update(self,ticks):
		self.x = self.x - self.speed
		self.y = self.basey + math.sin(self.x * 1.0 / 100) * 20

		if(self.destinationCelebration is not None):
			if(self.destinationCelebration.update(ticks)):
				self.destinationCelebration = None

		if self.x <  0 - self.width:
			self.destinationCelebration = DestinationCelebration(10,self.basey,self.pygame,self.surface,self.windowWidth,self.windowHeight,ticks,self.soundCounter)
			self.soundCounter = self.soundCounter + 1
			if(self.soundCounter == 5):
				self.soundCounter = 0
			self.x = self.windowWidth
			return True
		else:
			return False

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))
		if(self.destinationCelebration is not None):
			self.destinationCelebration.draw()

	def loadImages(self):
		self.image = self.pygame.image.load("assets/olivia.png")
		dimensions = self.image.get_rect().size
		self.width  = dimensions[0]
		self.height = dimensions[1]	

class DestinationCelebration(GameObject):
	def __init__(self,x,y,pygame,surface,windowHeight,windowWidth,creationTick,soundCounter):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeight)
		self.creationTick = creationTick
		self.font = self.pygame.font.Font("assets/font.ttf", 50)
		self.text = self.font.render("+10!", 1, (250, 255, 10))
		self.pos = self.text.get_rect()
		self.pos.x = self.x
		self.pos.y = self.y

		self.loadSounds()
		self.geluktSounds[soundCounter].play()

		self.interval = 5000

	def update(self,ticks):
		if ticks - self.creationTick > self.interval:
			return True
		else:
			if ticks - self.creationTick > 1000:
				self.pos.y = self.pos.y - 2
			return False

	def loadSounds(self):
		gelukt1 = self.pygame.mixer.Sound('assets/sounds/joepie_depoepie.wav')
		gelukt2 = self.pygame.mixer.Sound('assets/sounds/joepie_jeej.wav')
		gelukt3 = self.pygame.mixer.Sound('assets/sounds/joepie_klapklapklap.wav')
		gelukt4 = self.pygame.mixer.Sound('assets/sounds/joepie_yesgelukt.wav')
		gelukt5 = self.pygame.mixer.Sound('assets/sounds/joepie_yesyesyes.wav')

		self.geluktSounds = [ gelukt1, gelukt2, gelukt3, gelukt4, gelukt5 ]

	def draw(self):
		self.surface.blit(self.text,self.pos)
		

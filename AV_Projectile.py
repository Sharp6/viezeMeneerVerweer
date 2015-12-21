import AV_GameObject

class Bullet(GameObject):
	def __init__(self,x,y,pygame,surface,windowWidth,windowHeigth,speed):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeigth)
		self.x = x
		self.y = y
		self.pygame = pygame
		self.surface = surface
	
		self.speed = speed

		self.loadImages()
		self.setInitialPosition()
		
	def setInitialPosition(self):
		self.y += self.height / 2

	def loadImages(self):
		self.image = self.pygame.image.load("assets/christmas.png")
		dimensions = self.image.get_rect().size
		self.width = dimensions[0]
		self.height = dimensions[1]

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def update(self, ticks):
		self.x += self.speed	
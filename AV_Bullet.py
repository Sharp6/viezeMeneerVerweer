from AV_GameObject import GameObject

class Bullet(GameObject):
	def __init__(self,x,y,pygame,surface,windowWidth,windowHeigth,speed):
		GameObject.__init__(self,x,y,pygame,surface,windowWidth,windowHeigth)
	
		self.speed = speed

		self.loadImages()
		self.setInitialPosition()
		
	def setInitialPosition(self):
		self.y += self.height / 2

	def loadImages(self):
		self.image = self.pygame.image.load("assets/apple.png")
		dimensions = self.image.get_rect().size
		self.width = dimensions[0] / 5
		self.height = dimensions[1] / 5
		self.image = self.pygame.transform.scale(self.image, (self.width,self.height))

	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))

	def update(self, ticks):
		self.x += self.speed
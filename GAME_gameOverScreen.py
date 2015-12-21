class GameOver():
	def __init__(self,pygame,surface,windowWidth,windowHeight,inputDevice,fsm):
		self.fsm = fsm
		self.nextState = None

		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.input = inputDevice

		self.font = self.pygame.font.Font("assets/font.ttf", 20)
		self.textColor = (10, 10, 10)
		
		self.background = None
		self.loadImages()

		self.score = 0

	def enter(self):
		print "Entering Game Over screen."

	def exit(self):
		print "Exiting Game Over screen."

	def update(self,ticks):
		buttonState = self.input.getButtonState()
		if buttonState:
			self.fsm.changeState(self.nextState)

	def draw(self):
		self.surface.blit(self.background)
		self.drawScore()

	def loadImages(self):
		self.background = self.pygame.image.load("assets/menu.png")

	def drawScore(self):
		scoreText = self.font.render("Uw score: " + str(self.score), 1, self.textColor)
		scorePos = scoreText.get_rect()
		scorePos.centerx = self.windowWidth/2
		scorePos.centery = 100

		self.surface.blit(scoreText,scorePos)

	def setScore(self,score):
		self.score = score
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
		self.textColor = (33, 149, 255)
		
		self.background = None
		self.loadImages()
		self.loadSounds()

		self.score = 0

	def enter(self):
		print "Entering Game Over screen."
		self.gevonden.play()

	def exit(self):
		print "Exiting Game Over screen."

	def update(self,ticks):
		buttonState = self.input.getButtonState()
		if buttonState:
			self.fsm.changeState(self.nextState)

	def draw(self):
		self.surface.blit(self.background, (0,0))
		self.drawScore()

	def loadImages(self):
		self.background = self.pygame.image.load("assets/menu.png")

	def loadSounds(self):
		self.gevonden = self.pygame.mixer.Sound('assets/sounds/vm_gevonden.wav')

	def drawScore(self):
		scoreText = self.font.render("De VIEZE MENEER is aan onze voorraad snoepjes geraakt!", 1, self.textColor)
		scoreText2 = self.font.render("Gelukkig hebben we er nog " + str(self.score) + " kunnen redden.", 1, self.textColor)
		scoreText3 = self.font.render("Probeer nog eens om er nog meer op te kunnen peuzelen!", 1, self.textColor)
		scorePos = scoreText.get_rect()
		scorePos.centerx = self.windowWidth/2
		scorePos.centery = 100
		scorePos2 = scoreText2.get_rect()
		scorePos2.centerx = self.windowWidth/2
		scorePos2.centery = 150
		scorePos3 = scoreText3.get_rect()
		scorePos3.centerx = self.windowWidth/2
		scorePos3.centery = 200

		self.surface.blit(scoreText,scorePos)
		self.surface.blit(scoreText2,scorePos2)
		self.surface.blit(scoreText3,scorePos3)

	def setScore(self,score):
		self.score = score
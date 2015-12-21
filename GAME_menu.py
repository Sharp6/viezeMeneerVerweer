class Menu():
	def __init__(self,pygame,surface,windowWidth,windowHeight,inputDevice,fsm):
		self.fsm = fsm
		self.nextState = None

		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.input = inputDevice

		self.loadImages()

	def enter(self):
		print "Entering MENU state."

	def exit(self):
		print "Exiting MENU state."

	def update(self,ticks):
		buttonState = self.input.getButtonState()
		if buttonState:
			self.fsm.changeState(self.nextState)

	def draw(self):
		self.surface.blit(self.background, (0,0))

	def loadImages(self):
		self.background = self.pygame.image.load("assets/menu.png")
class Menu():
	def __init__(self,pygame,surface,windowWidth,windowHeight,inputDevice,fsm):
		self.fsm = fsm
		self.nextState = None

		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.input = inputDevice

		self.menuItemLabels = [ "Speler", "Moeilijk", "Start!" ]
		self.currentMenuItem = 2
		self.menuPosX = self.windowWidth / 2
		self.menuPosY = 20
		self.menuSpacing = 80

		self.selectionBoxWidth = 300
		self.selectionBoxHeight = 30

		self.font = self.pygame.font.Font("assets/christmasFont.ttf", 20)

		self.loadImages()

		self.tickOfLastCommand = 0
		self.commandInterval = 1000

	def enter(self):
		print "Entering MENU state."

	def exit(self):
		print "Exiting MENU state."

	def update(self,ticks):
		buttonState = self.input.getButtonState()
		position = self.input.getPosition()
		if(abs(position)>15):
			if(ticks - self.tickOfLastCommand > self.commandInterval):
				self.tickOfLastCommand = ticks
				if position < 0:
					self.decreaseSelection()
				else:
					self.increaseSelection()
		if buttonState:
			self.fsm.changeState(self.nextState)

	def draw(self):
		self.surface.blit(self.background, (0,0))
		self.drawSelectionBox(self.currentMenuItem)
		self.drawLabels()

	def loadImages(self):
		self.background = self.pygame.image.load("assets/menu.png")

	def drawLabels(self):
		for label in self.menuItemLabels:
			self.drawLabel(label)

	def drawLabel(self,label):
		labelText = self.font.render(str(label), 1, (10, 10, 10))
		labelPos = labelText.get_rect()
		labelPos.centerx = self.menuPosX
		labelPos.centery = self.menuPosY + self.menuItemLabels.index(label) * self.menuSpacing
		self.surface.blit(labelText,labelPos)

	def drawSelectionBox(self,label):
		self.pygame.draw.rect(self.surface,(10,250,10),(self.windowWidth/2-self.selectionBoxWidth/2,self.menuPosY + label * self.menuSpacing - 5, self.selectionBoxWidth,self.selectionBoxHeight))

	def increaseSelection(self):
		self.currentMenuItem = self.currentMenuItem + 1
		self.currentMenuItem = self.currentMenuItem % len(self.menuItemLabels)

	def decreaseSelection(self):
		self.currentMenuItem = self.currentMenuItem - 1
		if self.currentMenuItem < 0:
			self.currentMenuItem = len(self.menuItemLabels) - 1
class Menu():
	def __init__(self,pygame,surface,windowWidth,windowHeight,inputDevice,fsm):
		self.fsm = fsm
		self.nextState = None

		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.input = inputDevice

		self.menuItemLabels = [ "Speler", "Moeilijkheid", "Start!" ]
		self.currentMenuItem = 0
		self.menuPosX = self.windowWidth / 2
		self.menuPosY = 20
		self.menuSpacing = 100
		self.menuPaddingY = 30

		self.playerLabels = [ "LOTTE", "MARIE" ]
		self.currentPlayer = 0

		self.difficultyLabels = [ "Makkelijk", "Moeilijk", "Moeilijkst" ]
		self.currentDifficulty = 0

		self.selectionBoxWidth = 300
		self.selectionBoxHeight = 30

		self.font = self.pygame.font.Font("assets/font.ttf", 20)
		self.textColor = (10, 10, 10)

		self.verhaal = None

		self.loadImages()
		self.loadSounds()

		self.tickOfLastCommand = 0
		self.commandInterval = 700

	def enter(self):
		print "Entering MENU state."
		self.verhaal.play()

	def exit(self):
		print "Exiting MENU state."
		# DIRTY inter-state communication
		self.fsm.game.setPlayer(self.playerLabels[self.currentPlayer])
		self.fsm.game.setDifficulty(self.currentDifficulty)

	def update(self,ticks):
		buttonState = self.input.getButtonState()
		position = self.input.getPosition()
		if(abs(position)>5):
			if(ticks - self.tickOfLastCommand > self.commandInterval):
				self.tickOfLastCommand = ticks
				if position < 0:
					self.increaseSelection()
				else:
					self.decreaseSelection()
		if buttonState:
			if(ticks - self.tickOfLastCommand > self.commandInterval):
				self.tickOfLastCommand = ticks
				if self.currentMenuItem == 2:
					self.fsm.changeState(self.nextState)
				elif self.currentMenuItem == 0:
					self.changePlayer()
				elif self.currentMenuItem == 1:
					self.changeDifficulty()

	def draw(self):
		self.surface.blit(self.background, (0,0))
		self.drawSelectionBox(self.currentMenuItem)
		self.drawMenu()

	def loadImages(self):
		self.background = self.pygame.image.load("assets/menu.png")

	def loadSounds(self):
		self.verhaal = self.pygame.mixer.Sound('assets/sounds/intro.wav')

	def drawMenu(self):
		self.drawLabels()
		self.drawPlayer()
		self.drawDifficulty()

	def drawLabels(self):
		for label in self.menuItemLabels:
			self.drawLabel(label)

	def drawLabel(self,label):
		labelText = self.font.render(str(label), 1, self.textColor)
		labelPos = labelText.get_rect()
		labelPos.centerx = self.menuPosX
		labelPos.centery = self.menuPosY + self.menuItemLabels.index(label) * self.menuSpacing

		self.surface.blit(labelText,labelPos)

	def drawSelectionBox(self,label):
		self.pygame.draw.rect(self.surface,(33, 149, 255),(self.windowWidth/2-self.selectionBoxWidth/2,self.menuPosY + label * self.menuSpacing - (self.selectionBoxHeight/2), self.selectionBoxWidth,self.selectionBoxHeight))

	def increaseSelection(self):
		self.currentMenuItem = self.currentMenuItem + 1
		self.currentMenuItem = self.currentMenuItem % len(self.menuItemLabels)

	def decreaseSelection(self):
		self.currentMenuItem = self.currentMenuItem - 1
		if self.currentMenuItem < 0:
			self.currentMenuItem = len(self.menuItemLabels) - 1

	def drawPlayer(self):
		playerText = self.font.render(str(self.playerLabels[self.currentPlayer]), 1, (33, 149, 255))
		playerPos = playerText.get_rect()
		playerPos.centery = self.menuPosY + self.menuItemLabels.index("Speler") * self.menuSpacing + self.menuPaddingY
		playerPos.centerx = self.menuPosX

		self.surface.blit(playerText,playerPos)

	def drawDifficulty(self):
		difficultyText = self.font.render(str(self.difficultyLabels[self.currentDifficulty]), 1, (33, 149, 255))
		difficultyPos = difficultyText.get_rect()
		difficultyPos.centery = self.menuPosY + self.menuItemLabels.index("Moeilijkheid") * self.menuSpacing + self.menuPaddingY
		difficultyPos.centerx = self.menuPosX

		self.surface.blit(difficultyText,difficultyPos)

	def changePlayer(self):
		self.currentPlayer = self.currentPlayer+1
		self.currentPlayer = self.currentPlayer % len(self.playerLabels)

	def changeDifficulty(self):
		self.currentDifficulty = self.currentDifficulty + 1
		self.currentDifficulty = self.currentDifficulty % len(self.difficultyLabels)

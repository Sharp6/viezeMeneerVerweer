import AV_Enemy, AV_Player, AV_Olivia, AV_Decor

class ViezeMeneerVerweer():
	def __init__(self,pygame,surface,windowWidth,windowHeight,inputDevice,fsm):
		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight

		# Input
		self.input = inputDevice

		# FSM
		self.fsm = fsm
		self.nextState = None

		# Player
		self.player = None

		# Difficulty
		self.difficulty = None

	def enter(self):
		print "Entering Vieze Meneer Verweer"
		# Avatars
		self.player = AV_Player.Player(0, self.windowHeight / 2, self.pygame, self.surface, self.windowWidth, self.windowHeight, self.player)
		self.enemy = AV_Enemy.Enemy(self.windowWidth, self.windowHeight / 2, self.pygame, self.surface, self.windowHeight, self.windowWidth)
		self.olivia = AV_Olivia.Olivia(self.windowWidth, 10, self.pygame, self.surface, self.windowHeight, self.windowWidth)

		# Score
		self.score = 0
		self.font = self.pygame.font.Font("assets/font.ttf", 36)
		self.scoreText = self.font.render(str(self.score), 1, (10, 10, 10))
		self.scorePos = self.scoreText.get_rect()
		self.scorePos.centerx = self.windowWidth / 2

		# Decor 
		self.decor = AV_Decor.Decor(self.pygame,self.surface,self.windowWidth,self.windowHeight)

		# Set difficulty
		self.enemy.speed = self.difficulty + 2

	def exit(self):
		print "Exit Vieze Meneer Verweer"

	def update(self,ticks):
		buttonState = self.input.getButtonState()
		if buttonState and self.input.isDown is False:
			self.player.fire()
			# This is dirty
			self.input.isDown = True
		elif not(buttonState) and self.input.isDown is True:
			self.input.isDown = False

		# TODO: check input type for calling relative or absolute positioning
		self.player.setPositionRelative(self.input.getPosition())

		self.player.update(ticks)
		if(self.enemy.update(ticks)):
			self.fsm.changeState(self.nextState)
		if self.player.checkForHit(self.enemy):
			self.increaseScore()
		if self.olivia.update(ticks):
			self.increaseScore(10)
		self.decor.update(ticks)


	def increaseScore(self, points = 1):
		self.score = self.score + points
		self.scoreText = self.font.render(str(self.score), 1, (10, 10, 10))

	def drawScore(self):
		self.surface.blit(self.scoreText, self.scorePos)

	def draw(self):
		self.surface.fill((200,200,250))
		self.decor.draw()
		self.drawScore()
		self.olivia.draw()
		self.enemy.draw()
		self.player.draw()

	def setPlayer(self,player):
		self.player = player

	def setDifficulty(self,difficulty):
		self.difficulty = difficulty

	
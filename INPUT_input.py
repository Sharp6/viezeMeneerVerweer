import inputs

class Input():
	def __init__(self,pygame,type,windowWidth,windowHeight):
		self.pygame = pygame
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.type = type
		self.isDown = False

		if type == "gpio":
			self.joystick = inputs.joystick()

	def getPosition(self):
		if self.type == "mouse":
			position = self.pygame.mouse.get_pos()
			positionRelative = -((position[1] - self.windowHeight/2) / 10)
			return positionRelative
		elif self.type == "gpio":
			return self.joystick.checkY()/ 10

	def getButtonState(self):
		if self.type == "mouse":
			states = self.pygame.mouse.get_pressed()
			return states[0]
		elif self.type == "gpio":
			return self.joystick.checkA()

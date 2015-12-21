import random, math

class GameObject():
	def __init__(self,x,y,pygame,surface,windowWidth,windowHeight):
		self.x = x
		self.y = y
		self.pygame = pygame
		self.surface = surface
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
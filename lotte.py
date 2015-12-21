import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import INPUT_input
import GAME_viezeMeneerVerweer
from GAME_menu import Menu
from GAME_gameOverScreen import GameOver

class Manager():

	def __init__(self):
		self.pygame = pygame

		self.windowWidth = 800
		self.windowHeight = 480
		self.inputDevice = INPUT_input.Input(self.pygame,"mouse",self.windowWidth,self.windowHeight)

		self.pygame.init()
		self.pygame.font.init()
		self.surface = self.pygame.display.set_mode((self.windowWidth,self.windowHeight))
		#pygame.mixer.init()

		self.clock = self.pygame.time.Clock()

		#pygame.display.set_caption('Lotte en Marie')
		#textFont = pygame.font.SysFont("monospace", 50)

		self.currentState = None

		self.game = GAME_viezeMeneerVerweer.ViezeMeneerVerweer(self.pygame,self.surface,self.windowWidth,self.windowHeight,self.inputDevice,self)
		self.menu = Menu(self.pygame,self.surface,self.windowWidth,self.windowHeight,self.inputDevice,self)
		self.gameOver = GameOver(self.pygame,self.surface,self.windowWidth,self.windowHeight,self.inputDevice,self)

		self.menu.nextState = self.game
		self.game.nextState = self.gameOver
		self.gameOver.nextState = self.menu

		self.changeState(self.menu)

	def update(self,ticks):
		if (self.currentState != None):
			self.currentState.update(ticks)
			self.currentState.draw()

		for event in GAME_EVENTS.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.quitProgam()

			if event.type == GAME_GLOBALS.QUIT:
				self.quitProgam()

		self.pygame.display.update()
		self.clock.tick(40)

	def changeState(self, newState):
		if(self.currentState != None):
			self.currentState.exit()

		self.currentState = newState
		self.currentState.enter()

	def quitProgam(self):
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	manager = Manager()

	while True:
		manager.update(GAME_TIME.get_ticks())

		

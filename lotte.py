import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import avatars
import inputs

windowWidth = 800
windowHeight = 480

pygame.init()
pygame.font.init()
surface = pygame.display.set_mode((windowWidth,windowHeight))

pygame.display.set_caption('Lotte en Marie')
textFont = pygame.font.SysFont("monospace", 50)

gameStarted = False
gameOver = False
gameStartedTime = 0
gameFinishedTime = 0

# Mouse variables
mousePosition = (0,0)
mouseStates = None
mouseDown = False

#GPIO
gpioButtonState = None
gpioButtonDown = False
joystick = inputs.joystick()

# Avatars
player = avatars.Player(0, windowHeight / 2, pygame, surface, windowWidth)
enemy = avatars.Enemy(windowWidth, windowHeight / 2, pygame, surface, windowHeight)

# Clouds
clouds = []
lastCloudCreated = 0
cloudInterval = 2000

#pygame.mixer.init()

def updateGame():
	global mouseDown, gpioButtonDown, gpioButtonState, gameOver
	gpioButtonState = joystick.checkA()

	if gpioButtonState and gpioButtonDown is False:
		player.fire()
		gpioButtonDown = True
	elif not(gpioButtonState) and gpioButtonDown is True:
		gpioButtonDown = False

	if mouseStates[0] is 1 and mouseDown is False:
		player.fire()
		mouseDown = True
	elif mouseStates[0] is 0 and mouseDown is True:
		mouseDown = False

	#player.setPosition(mousePosition)
	player.moveY(joystick.checkY() / 10)
	enemy.move()
	player.checkForHit(enemy)
	addClouds()
	updateClouds()

def addClouds():
	global lastCloudCreated

	if GAME_TIME.get_ticks() - lastCloudCreated > cloudInterval:
		clouds.append(avatars.Cloud(windowWidth, random.randint(0,windowHeight), random.randint(1,3), pygame, surface))
		lastCloudCreated = GAME_TIME.get_ticks()

def updateClouds():
	for idx, cloud in enumerate(clouds):
		if cloud.x > 0 - cloud.width:
			cloud.move()
		else:
			del clouds[idx]

def drawGame(ticks):
	#surface.blit(background, (0,0))
	surface.fill((200,200,250))
	for cloud in clouds:
		cloud.draw()
	enemy.draw()
	player.draw(ticks)

def quitGame():
	pygame.quit()
	sys.exit()

while True:
	timeTick = GAME_TIME.get_ticks()
	mousePosition = pygame.mouse.get_pos()
	mouseStates = pygame.mouse.get_pressed()

	if gameStarted is True and gameOver is False:
		updateGame()
		drawGame(timeTick)

	elif gameStarted is False:
		# draw startscreen
		gameStarted = True

	elif gameStarted is True and gameOver is True:
		# draw gameover screen
		gameStarted = False

	for event in GAME_EVENTS.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()

	pygame.display.update()

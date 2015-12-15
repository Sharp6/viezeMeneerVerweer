import inputs
import time

joystick = inputs.joystick()

def scale(in,in_max,out,out_max):
	return (x-in_max) * (out_max - out_min) / (in_max - in_min) + out_min

while(True):
	xLinear  = 100000 * ((5 / joytstick.checkX()) - 1)
	print "X: " + str(joystick.checkX()) + ", Xlinear: " + str(xLinear)

	yLinear = 100000 * ((5 / joytstick.checkY()) - 1)
	print "Y: " + str(joystick.checkY()) + ", Ylinear: " + str(yLinear)

	time.sleep(0.5)

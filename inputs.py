import RPi.GPIO as GPIO

class joystick():

	#MCP3008
	clockpin = 18
	misopin = 23
	mosipin = 24
	cspin = 25

	# JOYSTICK
	vertical_adc = 1;
	horizontal_adc = 0;

	last_read = 0       # this keeps track of the last potentiometer value
	tolerance = 5       # to keep from being jittery we'll only change
	                    # volume when the pot has moved more than 5 'counts'

	
	def __init__(self):
		GPIO.setmode(GPIO.BCM)

		# SLIDE SWITCH
		GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# PUSHBUTTONS
		GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		# set up the SPI interface pins
		GPIO.setup(self.mosipin, GPIO.OUT)
		GPIO.setup(self.misopin, GPIO.IN)
		GPIO.setup(self.clockpin, GPIO.OUT)
		GPIO.setup(self.cspin, GPIO.OUT)

	def readadc(self, adcnum):
	  if ((adcnum > 7) or (adcnum < 0)):
			return -1
	  GPIO.output(self.cspin, True)

	  GPIO.output(self.clockpin, False)  # start clock low
	  GPIO.output(self.cspin, False)     # bring CS low

	  commandout = adcnum
	  commandout |= 0x18  # start bit + single-ended bit
	  commandout <<= 3    # we only need to send 5 bits here

	  for i in range(5):
	    if (commandout & 0x80):
				GPIO.output(self.mosipin, True)
	    else:
				GPIO.output(self.mosipin, False)
	    commandout <<= 1
	    GPIO.output(self.clockpin, True)
	    GPIO.output(self.clockpin, False)

	  adcout = 0
	  # read in one empty bit, one null bit and 10 ADC bits
	  for i in range(12):
			GPIO.output(self.clockpin, True)
			GPIO.output(self.clockpin, False)
			adcout <<= 1
			if (GPIO.input(self.misopin)):
				adcout |= 0x1

	  GPIO.output(self.cspin, True)
	  
	  adcout >>= 1       # first bit is 'null' so drop it
	  return adcout

	def checkSwitch(self):
		if not(GPIO.input(13)):
			return "1"
		elif not(GPIO.input(16)):
			return "2"
		elif not(GPIO.input(19)):
			return "3"
		elif not(GPIO.input(20)):
			return "4"
		elif not(GPIO.input(21)):
			return "5"

	def checkA(self):
		return GPIO.input(5)

	def checkB(self):
		return GPIO.input(6)

	def checkX(self):
                xLinear = round(100000.0 * ((1024.0 / self.readadc(self.horizontal_adc)) - 1.0))
                xScaled = int(self.scale(xLinear, 98,134000,0,200) + 100)
                return xScaled

	def checkY(self):
                yLinear = round(100000.0 * ((1024.0 / self.readadc(self.vertical_adc)) - 1.0))
                yScaled = int(abs(self.scale(yLinear,98,138000,0,200)) - 100)
                return yScaled

	def scale(self,x,in_min,in_max,out_min,out_max):
		return (x-in_max) * (out_max - out_min) / (in_max - in_min) + out_min

	def close(self):
		GPIO.cleanup()


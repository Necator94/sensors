import Adafruit_BBIO.PWM as PWM
import time
while True:
#	PWM.start("P9_14", 50, 2500, 1)
	time.sleep(3)
	PWM.stop("P9_14")

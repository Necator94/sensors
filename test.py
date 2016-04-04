import Adafruit_BBIO.GPIO as GPIO
import time

#x-band 
GPIO.setup("P8_12", GPIO.IN)    	# out pin
#GPIO.setup("P8_14", GPIO.OUT)  	# EN  pin unused
#GPIO.output("P8_14", GPIO.HIGH)   	# 1 to EN unused
GPIO.setup("P8_16", GPIO.OUT)    	# LED  pin 

#pir
GPIO.setup("P8_11", GPIO.IN)  		# out pin
#GPIO.setup("P8_13", GPIO.OUT) 		# Vss  pin unused
#GPIO.output("P8_13", GPIO.HIGH)	# 1 to Vss unused

while True:
	if GPIO.input("P8_12") :
    		GPIO.output("P8_16", GPIO.HIGH)
		print("HIGH")
#		time.sleep(2)
	else:
		GPIO.output("P8_16", GPIO.LOW)
   		print("LOW")





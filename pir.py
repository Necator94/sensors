import Adafruit_BBIO.GPIO as GPIO
import time
 
GPIO.setup("P8_11", GPIO.IN)     # out pin
GPIO.setup("P8_13", GPIO.OUT)     # Vss  pin 

GPIO.setup("P8_16", GPIO.OUT)     # LED  pin 

GPIO.output("P8_13", GPIO.HIGH)
while True:
	if GPIO.input("P8_11"):
    		GPIO.output("P8_16", GPIO.HIGH)
		print("HIGH")
	#time.sleep(2)
	else:
		GPIO.output("P8_16", GPIO.LOW)
   		print("LOW")

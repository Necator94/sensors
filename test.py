import Adafruit_BBIO.GPIO as GPIO
import time
 
GPIO.setup("P8_12", GPIO.IN)     # out pin
GPIO.setup("P8_14", GPIO.OUT)     # EN  pin 
GPIO.setup("P8_16", GPIO.OUT)     # LED  pin 

GPIO.output("P8_14", GPIO.HIGH)
while True:
	if GPIO.input("P8_12"):
    		GPIO.output("P8_16", GPIO.HIGH)
		print("HIGH")
		time.sleep(1)
	else:
		GPIO.output("P8_16", GPIO.LOW)
   		print("LOW")

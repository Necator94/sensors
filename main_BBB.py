import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import Adafruit_BBIO.GPIO as GPIO
import time
from collections import Counter
import threading
import Queue
import sys
import thread
import os

print 'program starting'
print "________________"

def xband_pir(pin, cycles, outData, outTime, name):
	cycles = cycles * 350
	print name, 'started'
	GPIO.setup(pin[0], GPIO.IN)	    	# out pin
	GPIO.setup(pin[1], GPIO.OUT)    	# LED  pin 

	data = []
	rowTime = []
	time_ = []
	i = 0

	while i < cycles:
		if GPIO.input(pin[0]) :
    			GPIO.output(pin[1], GPIO.HIGH)
    			#print "motion detected" + name
			flag = 1
		else:
			GPIO.output(pin[1], GPIO.LOW)
			flag = 0

		data.append(flag)
		rowTime.append(time.time())
		time_.append(rowTime[i] - rowTime[0])
		i += 1
	print name, 'finished'
        outData.put(data)
	outTime.put(time_)


# 0 - out pin     1 - LED pin
xBandPins = {0 : 'P8_8', 1 : 'P8_10'}	
pirPins = {0 : 'P8_7', 1 : 'P8_12' }

xBandData = Queue.Queue()
xBandTime = Queue.Queue()
pirData = Queue.Queue()
pirTime = Queue.Queue()

xBandThread = threading.Thread(target = xband_pir, args = (xBandPins, int(sys.argv[1]), xBandData, xBandTime, 'xBand'))
pirThread = threading.Thread(target = xband_pir, args = (pirPins, int(sys.argv[1]), pirData, pirTime, 'pir'))

xBandThread.start()
pirThread.start()

xBandThread.join()
pirThread.join()

xBandData_ = xBandData.get()
xBandTime_ = xBandTime.get()
pirData_ = pirData.get()
pirTime_ = pirTime.get()

file = open("row_data" + "_" + sys.argv[2] + ".txt", "w")
for index in range(len(xBandData_)):
    file.write(str(xBandData_[index]) + " " + str(xBandTime_[index]) + " " + str(pirData_[index])+ " " + str(pirTime_[index]) + "\n")
file.close()





















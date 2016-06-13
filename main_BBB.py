#!/usr/bin/env python
#import matplotlib
#matplotlib.use("AGG")
#import matplotlib.pyplot as plt
import Adafruit_BBIO.GPIO as GPIO
import time
from collections import Counter
import threading
import Queue
import sys
import thread
import os

# 0 - out pin     1 - LED pin
xBandPins = {0 : 'P8_12', 1 : 'P8_11'}	
pirPins = {0 : 'P8_14', 1 : 'P8_13' }

print 'program starting'
print "________________"


GPIO.setup(xBandPins[0], GPIO.IN)	    	
GPIO.setup(xBandPins[1], GPIO.OUT)  

GPIO.setup(pirPins[0], GPIO.IN)	    	
GPIO.setup(pirPins[1], GPIO.OUT)    	

def xband_pir(pin, cycles, outData, name):
	
	window = int(sys.argv[2])
	temp = []
	temp_time = []
	transform_time = []
	if name == 'PIR sensor':
		sleepTime = 0.001
	if name == 'X-Band detector':
		sleepTime = 0
	cycles = cycles * 350
	print name, 'started'
	data = []
	data.append([])
	data.append([])
	i = 0
	startTime = time.time()
	f = open('test.txt', 'w')
	while i < cycles:
		check = GPIO.input(pin[0])
		#print check
		data[0].append(check)	
		t_time = time.time() - startTime
		#print t_time
		data[1].append(t_time)
#___________________________________________________
# frequency transformation
		if len(temp) < window:
			temp.append(check)
			temp_time.append(t_time)
			#print '+'
			
		else:
			#print '-'
			temp.append(check)
			temp_time.append(t_time)
			for n, element in enumerate(temp):
				if element > temp[n - 1] and n > 0:
					#print n, element
					transform_time.append(temp_time[n])
			#print len(transform_time), 'len'
					
			for n, element in enumerate(transform_time):
				#print transform_time[n], n
				if n > 0:	
					al = 1/(transform_time[n] - transform_time[n-1])
					if al > 30:
						print al
						GPIO.output(pin[1], GPIO.HIGH)
					else:
						GPIO.output(pin[1], GPIO.LOW)
			temp = []
			temp_time = []
			transform_time = []

		i += 1
	print name, 'finished'
	outData.put(data)


#_________________________________________________
#convolutional transformation
'''			
		if len(data[0]) < window:
			temp.append(check)
			sum_value = sum(temp)
		else:
			temp.append(check)
			del temp[0]
			sum_value = sum(temp)
		#print sum_value
		if sum_value > int(sys.argv[3]):
			GPIO.output(pin[1], GPIO.HIGH)
			print sum_value
		else:
			GPIO.output(pin[1], GPIO.LOW)
		f.write(str(temp) + '\n'+ str(sum_value) + '\n')
		i += 1
		time.sleep(sleepTime)
	
	print name, 'finished'
	outData.put(data)

'''








xBandData_queue = Queue.Queue()
#pirData_queue = Queue.Queue()

xBandThread = threading.Thread(target = xband_pir, args = (xBandPins, int(sys.argv[1]), xBandData_queue, 'X-Band detector'))
#pirThread = threading.Thread(target = xband_pir, args = (pirPins, int(sys.argv[1]), pirData_queue, 'PIR sensor'))

xBandThread.start()
#pirThread.start()

xBandThread.join()
#pirThread.join()

xBandData = xBandData_queue.get()
#pirData = pirData_queue.get()

'''
mean = []
for i in range(len(xBandData[1])):
	if i != 0:
		mean.append(xBandData[1][i] -  xBandData[1][i-1])
mean = sum(mean) / len(mean)
print mean
'''
'''
file = open("row_data" + "_" + sys.argv[2] + ".txt", "w")
s = ' '
for index in range(len(xBandData[0])):
    file.write(str(xBandData [0] [index]) + s + str(xBandData [1] [index])  + "\n")
file.close()
'''
'''+ s + str(pirData [0] [index]) + s + str(pirData [1] [index])'''


















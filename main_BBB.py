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

def xband_pir(pin, cycles, out_raw_data, out_fr_trans_graph, name):
	#window = int(sys.argv[2])
	periods = []
	temp = []
	temp.append([])
	temp.append([])
	fr_trans_graph = []
	fr_trans_graph.append([])
	fr_trans_graph.append([])
	raw_data = []
	raw_data.append([])
	raw_data.append([])
	t_time = 0

#	slide_window = []

	print name, 'started'
	
	startTime = time.time()
	while t_time < cycles:
		check = GPIO.input(pin[0])
		t_time = time.time() - startTime
		raw_data[0].append(check)	
		raw_data[1].append(t_time)
#___________________________________________________
# frequency transformation
		temp[0].append(check)
		temp[1].append(t_time)
		if len(temp[0]) > 1 and temp[0][-1] > temp[0][-2]:
			periods.append(temp[1][-2]) 
			if len(periods) > 1:
				freq = 1/(periods[-1] - periods[-2])
				fr_trans_graph[0].append(temp[1][-2])
				fr_trans_graph[1].append(freq)
				if freq > 20:
					GPIO.output(pin[1], GPIO.HIGH)
				else:
					GPIO.output(pin[1], GPIO.LOW)
				#print freq, periods[-1], len(periods)
				del periods[0]
			del temp[0][:-1]
			del temp[1][:-1]
	print name, 'finished'
	out_raw_data.put(raw_data)
	out_fr_trans_graph.put(fr_trans_graph)


xBand_raw_data_queue = Queue.Queue()
xBand_fr_transform_queue = Queue.Queue()
#pirData_queue = Queue.Queue()

xBandThread = threading.Thread(target = xband_pir, args = (xBandPins, int(sys.argv[1]), xBand_raw_data_queue, xBand_fr_transform_queue, 'X-Band detector'))
#pirThread = threading.Thread(target = xband_pir, args = (pirPins, int(sys.argv[1]), pirData_queue, 'PIR sensor'))

xBandThread.start()
#pirThread.start()

xBandThread.join()
#pirThread.join()

xBand_raw_data = xBand_raw_data_queue.get()
xBand_fr_transform = xBand_fr_transform_queue.get()
#pirData = pirData_queue.get()

file = open("plot_data" + "_"  + ".txt", "w")
s = ' '
for index in range(len(xBand_fr_transform[0])):
    file.write(str(xBand_fr_transform[0][index]) + s + str(xBand_fr_transform[1][index]) + "\n")
file.close()




















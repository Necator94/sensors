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
import math
import numpy as np


#sys.argv[1] - time duration of the experiment
#sys.argv[2] - frequency criteria of movment detection
#sys.argv[3] - standard deviation criteria of movement detection

# 0 - out pin     1 - LED pin
xBandPins = {0 : 'P8_12', 1 : 'P8_11'}	
pirPins = {0 : 'P8_14', 1 : 'P8_13' }

print 'program starting'
print "________________"

GPIO.setup(xBandPins[0], GPIO.IN)	    	
GPIO.setup(xBandPins[1], GPIO.OUT)  

GPIO.setup(pirPins[0], GPIO.IN)	    	
GPIO.setup(pirPins[1], GPIO.OUT)    	

def xband(pin, out_raw_data, out_fr_trans_graph, out_detect_signal,  name):

	duration = float(sys.argv[1])
	fr_level = float(sys.argv[2])
	std_level = float(sys.argv[3])
	periods = []
	
	temp = []
	for i in range(2): temp.append([])
	fr_trans_graph = []
	for i in range(2): fr_trans_graph.append([])
	raw_data = []
	for i in range(2): raw_data.append([])
	detect_signal = []
	for i in range(4): detect_signal.append([])

	t_time = 0
	slide_window = []
	st_dev = 0
	mean_vol = 0

	print name, 'started'
	startTime = time.time()
	
	while t_time < duration:
		check = GPIO.input(pin[0])
		t_time = time.time() - startTime
		raw_data[0].append(t_time)	
		raw_data[1].append(check)

# frequency transformation
		temp[0].append(check)
		temp[1].append(t_time)
		if len(temp[0]) > 1 and temp[0][-1] > temp[0][-2]:
			periods.append(temp[1][-2]) 
			if len(periods) > 1:
				freq = 1/(periods[-1] - periods[-2])
				fr_trans_graph[0].append(temp[1][-2])
				fr_trans_graph[1].append(freq)
				slide_window.append(freq)
				
				if len(slide_window) > 3:
					slide_window = [] 

				if len(slide_window) == 3: 
					st_dev = np.std(slide_window)			# standard deviation
					mean_vol = np.mean(slide_window)

				if mean_vol > fr_level and st_dev < std_level:
					GPIO.output(pin[1], GPIO.HIGH)
					detect_signal[0].append(t_time)
					detect_signal[1].append(1)
					detect_signal[2].append(mean_vol)
					detect_signal[3].append(st_dev)
				else:
					GPIO.output(pin[1], GPIO.LOW)
					detect_signal[0].append(t_time)
					detect_signal[1].append(0)
					detect_signal[2].append(mean_vol)
					detect_signal[3].append(st_dev)
				del periods[0]
			del temp[0][:-1]
			del temp[1][:-1]

	print name, 'finished'
	out_raw_data.put(raw_data)
	out_fr_trans_graph.put(fr_trans_graph)
	out_detect_signal.put(detect_signal)


xBand_raw_data_queue = Queue.Queue()
xBand_fr_transform_queue = Queue.Queue()
xBand_detect_signal_queue = Queue.Queue()
#pirData_queue = Queue.Queue()

xBandThread = threading.Thread(target = xband, args = 	(xBandPins, xBand_raw_data_queue, xBand_fr_transform_queue, xBand_detect_signal_queue, 'X-Band detector'))
#pirThread = threading.Thread(target = xband_pir, args = (pirPins, int(sys.argv[1]), pirData_queue, 'PIR sensor'))

xBandThread.start()
#pirThread.start()

xBandThread.join()
#pirThread.join()

xBand_raw_data = xBand_raw_data_queue.get()
xBand_fr_transform = xBand_fr_transform_queue.get()
xBand_detect_signal = xBand_detect_signal_queue.get()
#pirData = pirData_queue.get()

file = open("plot_data" + "_"  + ".txt", "w")
file.write("row_data" + '\n')
s = ' '
for index in range(len(xBand_raw_data[0])): file.write(str(xBand_raw_data[0][index]) + s + str(xBand_raw_data[1][index]) + "\n")
file.write("/end_of_row_data" + '\n')

file.write("xBand_fr_transform" + '\n')
for index in range(len(xBand_fr_transform[0])): file.write(str(xBand_fr_transform[0][index]) + s + str(xBand_fr_transform[1][index]) + "\n")
file.write("/end_of_xBand_fr_transform" + '\n')

file.write("xBand_detect_signal" + '\n')
for index in range(len(xBand_detect_signal[0])):
    file.write(str(xBand_detect_signal[0][index]) + s + str(xBand_detect_signal[1][index]) + s + str(xBand_detect_signal[2][index]) + s + str(xBand_detect_signal[3][index]) +"\n")
file.write("/end_of_xBand_detect_signal" + '\n')

file.close()



















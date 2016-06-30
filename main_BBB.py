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
#sys.argv[2] - mean frequency criteria of movment detection
#sys.argv[3] - standard deviation criteria of movement detection

# 0 - out pin     1 - LED pin
xBandPins = {'signal_pin' : 'P8_12', 'LED_pin' : 'P8_11'}	
#pir1Pins = {'signal_pin' : 'P8_14', 'LED_pin' : 'P8_13' }
pir1Pins = {'signal_pin' : 'P8_15', 'LED_pin' : 'P8_13' }
pir2Pins = {'signal_pin' : 'P8_17', 'source_pin' : 'P8_18' }

if len(sys.argv) < 3:
	exp_parameter = {'duration' : 30,'fr_level' : 20,'std_level' : 15}
	print '______________________________________________'
	print "parameters are set by default:%stime duration = %i s%sfr_level = %i%sstd_level = %i%s" % ('\n',exp_parameter['duration'],'\n',exp_parameter['fr_level'],'\n',exp_parameter['std_level'],'\n')
else:
	exp_parameter = {'duration' : int(sys.argv[1]),'fr_level' : int(sys.argv[2]),'std_level' : int(sys.argv[3])}
	print '______________________________________________'
	print "parameters are set manually:%stime duration = %is%sfr_level = %i%sstd_level = %i%s" % ('\n',exp_parameter['duration'],'\n',exp_parameter['fr_level'],'\n',exp_parameter['std_level'],'\n')
print 'Program starting...'


GPIO.setup(xBandPins['signal_pin'], GPIO.IN)	    	
#GPIO.setup(xBandPins['LED_pin'], GPIO.OUT)  

GPIO.setup(pir1Pins['signal_pin'], GPIO.IN)	    	
#GPIO.setup(pirPins['LED_pin'], GPIO.OUT)    	

GPIO.setup(pir2Pins['signal_pin'], GPIO.IN)
GPIO.setup(pir2Pins['source_pin'], GPIO.OUT)
GPIO.output(pir2Pins['source_pin'], GPIO.HIGH)	

def xband(gpio_pins, out_raw_data, out_fr_trans_graph, out_detect_signal, exp_parameter):

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

	print 'X-Band started'
	startTime = time.time()
	
	while t_time < exp_parameter['duration'] :
		check = GPIO.input(gpio_pins['signal_pin'])
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

				if mean_vol > exp_parameter['fr_level'] and st_dev <  exp_parameter['std_level']:
					#GPIO.output(gpio_pins['LED_pin'], GPIO.HIGH)
					detect_signal[0].append(t_time)
					detect_signal[1].append(True)
					detect_signal[2].append(mean_vol)
					detect_signal[3].append(st_dev)
				else:
					#GPIO.output(gpio_pins['LED_pin'], GPIO.LOW)
					detect_signal[0].append(t_time)
					detect_signal[1].append(False)
					detect_signal[2].append(mean_vol)
					detect_signal[3].append(st_dev)
				del periods[0]
			del temp[0][:-1]
			del temp[1][:-1]

	print 'X-Band finished'
	out_raw_data.put(raw_data)
	out_fr_trans_graph.put(fr_trans_graph)
	out_detect_signal.put(detect_signal)


def pir(gpio_pins, out_detect_signal, exp_parameter, name):
	t_time = 0
	detect_signal = []
	for i in range(2): detect_signal.append([])
	print name, 'started'

	startTime = time.time()
	while t_time < exp_parameter['duration'] :
		check = GPIO.input(gpio_pins['signal_pin']) 
		t_time = time.time() - startTime
		detect_signal[0].append(t_time)
		detect_signal[1].append(check)	
		time.sleep(0.1)
	print name, 'finished'
	out_detect_signal.put(detect_signal)

xBand_raw_data_queue = Queue.Queue()
xBand_fr_transform_queue = Queue.Queue()
xBand_detect_signal_queue = Queue.Queue()
pir1_detect_signal_queue = Queue.Queue()
pir2_detect_signal_queue = Queue.Queue()


xBandThread = threading.Thread(target = xband, args = 	(xBandPins, xBand_raw_data_queue, xBand_fr_transform_queue, xBand_detect_signal_queue, exp_parameter))
pir1Thread = threading.Thread(target = pir, args = (pir1Pins, pir1_detect_signal_queue, exp_parameter, 'pir1'))
pir2Thread = threading.Thread(target = pir, args = (pir2Pins, pir2_detect_signal_queue, exp_parameter, 'pir2'))

xBandThread.start()
pir1Thread.start()
pir2Thread.start()

xBandThread.join()
pir1Thread.join()
pir2Thread.join()

xBand_raw_data = xBand_raw_data_queue.get()
xBand_fr_transform = xBand_fr_transform_queue.get()
xBand_detect_signal = xBand_detect_signal_queue.get()
pir1_detect_signal = pir1_detect_signal_queue.get()
pir2_detect_signal = pir2_detect_signal_queue.get()

file = open("plot_data" + "_"  + ".txt", "w")
file.write("exp_parameter" + '\n')
s = ' '
file.write(str(exp_parameter['duration']) + s + str(exp_parameter['fr_level']) + s + str(exp_parameter['std_level']) + '\n')
file.write("/end_of_exp_parameter" + '\n')

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

file.write("pir1_detect_signal" + '\n')
for index in range(len(pir1_detect_signal[0])):
    file.write(str(pir1_detect_signal[0][index]) + s + str(pir1_detect_signal[1][index]) +"\n")
file.write("/end_of_pir1_detect_signal" + '\n')

file.write("pir2_detect_signal" + '\n')
for index in range(len(pir2_detect_signal[0])):
    file.write(str(pir2_detect_signal[0][index]) + s + str(pir2_detect_signal[1][index]) +"\n")
file.write("/end_of_pir2_detect_signal" + '\n')

file.close()



















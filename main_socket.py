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
import socket

#args[0] - time duration
#args[1] - distance for experiment

print 'program starting'
print "________________"

def xband_pir(pin, cycles, outData, outTime, name):
	t_ex1 = time.time()
	t_ex2 = 1
	print name, 'started'
		
	GPIO.setup(pin[0], GPIO.IN)	    	# out pin
	GPIO.setup(pin[1], GPIO.OUT)    	# LED  pin 

	data = []
	rowTime = []
	time_ = []
	i = 0

	while time.time() - t_ex1 < cycles:
		if GPIO.input(pin[0]) :
			GPIO.output(pin[1], GPIO.HIGH)
			flag = 1
		else:
			GPIO.output(pin[1], GPIO.LOW)
			flag = 0

		data.append(flag)
		rowTime.append(time.time())
		time_.append(rowTime[i] - rowTime[0])
		i += 1
	
	print name, 'finished', "  time = ", time.time() - t_ex1
	outData.put(data)
	outTime.put(time_)


# 0 - out pin     1 - LED pin
xBandPins = {0 : 'P8_8', 1 : 'P8_10'}	
pirPins = {0 : 'P8_7', 1 : 'P8_12' }

xBandData = Queue.Queue()
xBandTime = Queue.Queue()
pirData = Queue.Queue()
pirTime = Queue.Queue()

#socket part
#*******************
HOST = ''   
PORT = 5566

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'
 



while True:
	s.listen(10)
	print 'Socket now listening'
	conn, addr = s.accept()
	#now keep talking with the client
	data = conn.recv(64)
	print data 
	#*******************
	args = data.split()    
	if args[0] == 'exit':
		print 'exit'
		break
	elif len(args) < 2:
		print '2 args are required'
		break

	xBandThread = threading.Thread(target = xband_pir, args = (xBandPins, int(args[0]), xBandData, xBandTime, 'xBand'))
	pirThread = threading.Thread(target = xband_pir, args = (pirPins, int(args[0]), pirData, pirTime, 'pir'))

	xBandThread.start()
	pirThread.start()
#	conn.sendto('started', addr)
	xBandThread.join()
	pirThread.join()
#	conn.sendto('finished', addr)
	conn.close()

	GPIO.cleanup()

	xBandData_ = xBandData.get()
	xBandTime_ = xBandTime.get()
	pirData_ = pirData.get()
	pirTime_ = pirTime.get()

	file = open("row_data_" + args[1] + ".txt", "w")
	if len(xBandData_) < len (pirData_):
		length = len(xBandData_)
	else:
		length = len(pirData_)
		
	for index in range(length):
		file.write(str(xBandData_[index]) + " " + str(xBandTime_[index]) + " " + str(pirData_[index])+ " " + str(pirTime_[index]) + "\n")
	file.close()

	
s.close()
print "socket closed"




















import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import Adafruit_BBIO.GPIO as GPIO
import time
from Adafruit_I2C import Adafruit_I2C as bus
from collections import Counter
import threading
import Queue
import sys
import thread
import os

locations = {
0:  '0-352mm', 
1:  '353-705mm', 
2:  '706-1057mm', 
3:  '1058-1410mm', 
4:  '1411-1763mm',
5:  '1764-2116mm', 
6:  '2117-2369mm', 
7:  '2370-2622mm', 
8:  '2623-2875mm', 
9:  '2876-3228mm', 
10: '3229-3581mm', 
11: '3582-3934mm', 
12: '3934-4287mm',
13: '4288-4640mm',
14: '4641-4993mm',
15: '4994-5346mm',
16: '5347-5599mm',
17: '5600-5852mm',
18: '5853-6105mm',
19: '6106-6358mm',
20: '6359-6611mm',
21: '6612-6864mm',
22: '6865-7117mm',
23: '7117-7370mm',
24: '7371-7623mm',
25: '7624-7876mm',
26: '7877-8129mm',
27: '8130-8382mm',
28: '8383-8635mm',
29: '8636-8888mm',
30: '8889-9141mm',
31: '9142-9394mm',
}

def find_majority(k):
        myMap = {}
        maximum = ( '', 0 ) # (occurring element, occurrences)
        for n in k:
                if n in myMap: myMap[n] += 1
                else: myMap[n] = 1
       		# Keep track of maximum on the go
                if myMap[n] > maximum[1]: maximum = (n,myMap[n])
        return maximum

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


def srf08 (pin, cycles, outData, outTime, name, location):
	print name, 'started'
	GPIO.setup(pin[1], GPIO.OUT)    	 
	i2c = bus(0x70)
	bus.write8(i2c, 2, 255)
	bus.write8(i2c, 1, 0)
	window = []
	data = []
	time_ = []
	rowTime = []	
	Location = []
	i = 0

	while i < cycles:
		bus.write8(i2c, 0, 84)
		time.sleep(0.07)
		ranging_result = []
		n = 4
	
		while n < 36 :
			ranging_result.append(bus.readU8(i2c, n)) 
			n += 1
		for index, element in enumerate(ranging_result) :		
     			if element == 255 and len(window) == 15:
				window.insert(0, index)
				del window[-1]
				break		
			elif element == 255 and len(window) < 15:
				window.append(index)
				break
		majority = find_majority(window)
		print majority[0]
#		Location.append(locations[majority[0]])	
		if len(window) - majority[1] > 2 :
			GPIO.output(pin[1], GPIO.HIGH)
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
	location.put(Location)

# 0 - out pin     1 - LED pin
xBandPins = {0 : 'P8_8', 1 : 'P8_10'}	
pirPins = {0 : 'P8_7', 1 : 'P8_12' }
srf08Pins = {1: 'P8_14'}

xBandData = Queue.Queue()
xBandTime = Queue.Queue()
pirData = Queue.Queue()
pirTime = Queue.Queue()
srf08Data = Queue.Queue()
srf08Time = Queue.Queue()
srfDistance = Queue.Queue()

xBandThread = threading.Thread(target = xband_pir, args = (xBandPins, int(sys.argv[1]), xBandData, xBandTime, 'xBand'))
pirThread = threading.Thread(target = xband_pir, args = (pirPins, int(sys.argv[1]), pirData, pirTime, 'pir'))
srf08Thread = threading.Thread(target = srf08, args = (srf08Pins, int(sys.argv[1]), srf08Data, srf08Time, 'sfr08', srfDistance))

xBandThread.start()
pirThread.start()
srf08Thread.start()

xBandThread.join()
pirThread.join()
srf08Thread.join()

xBandData_ = xBandData.get()
xBandTime_ = xBandTime.get()
pirData_ = pirData.get()
pirTime_ = pirTime.get()
srf08Data_ = srf08Data.get()
srf08Time_ = srf08Time.get()
#srfDistance_ = srfDistance.get()

file = open("xBandData.txt", "w")
for index in range(len(xBandData_)):
    file.write(str(xBandData_[index]) + " " + str(xBandTime_[index]) + "\n")
file.close()

file = open("pirData.txt", "w")
for index in range(len(pirData_)):
    file.write(str(pirData_[index])+ " " + str(pirTime_[index]) + "\n")
file.close()

file = open("srf08Data.txt", "w")
for index in range(len(srf08Data_)):
    file.write(str(srf08Data_[index])+ " " + str(srf08Time_[index]) + "\n")
file.close()
'''
file = open("srf08Distance.txt", "w")
for index in range(len(srf08Data_)):
    file.write(str(srfDistance_[index]) + "\n")
file.close()
'''
'''
if sys.argv[2] == 'on':
	plt.figure(1)
	plt.subplots_adjust(hspace=.4)

	#srf08
	plt.subplot(311)
	plt.plot(srf08Time_, srf08Data_, 'g')
	plt.axis([0,10,0,1.5])
	plt.ylabel('Motion status')
	plt.title('Ultrasonic SRF08 sensor')

	#pir
	plt.subplot(312)
	plt.plot(pirTime_, pirData_, 'r')
	plt.axis([0,10,0,1.5])
	plt.ylabel('Motion status')
	plt.title('PIR sensor')
	
	#x-band
	plt.subplot(313)
	plt.plot(xBandTime_, xBandData_, 'b')
	plt.axis([0,10,0,1.5])
	plt.ylabel('Motion status')
	plt.xlabel('Time, s')
	plt.title('X-band motion sensor')

	plt.savefig("BBBPlot.svg")

	os.system("scp xBandData.txt pirData.txt srf08Data.txt sensorsPlot.svg srf08Distance.txt ivan@10.33.21.174:/home/ivan/sensors/")
'''




















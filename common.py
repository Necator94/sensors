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
	window = [32] * 15
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
     			if element == 255:
				window.insert(0, index)
				del window[-1]
				break		
	
		majority = find_majority(window)
		if len(window) - majority[1] > 2:
		#	print 'motion detected', locations[majority[0]]	
    			GPIO.output(pin[1], GPIO.HIGH)
			flag = 1
		else:
			GPIO.output(pin[1], GPIO.LOW)
			flag = 0
		Location.append(majority)
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
#print srfDistance_
'''
#srf08
locations = {
0:  '0-0.35m    	(0-352mm)', 
1:  '0.35-0.7m  	(353-705mm)', 
2:  '0.7-1m     	(706-1057mm)', 
3:  '1-1.4m     	(1058-1410mm)', 
4:  '1.41-1.76m 	(1411-1763mm)',
5:  '1.76-2.11m 	(1764-2116mm)', 
6:  '2.11-2.36m 	(2117-2369mm)', 
7:  '2.37-2.62m 	(2370-2622mm)', 
8:  '2.62-2.87m 	(2623-2875mm)', 
9:  '2.87-3.22m 	(2876-3228mm)', 
10: '3.22-3.58m 	(3229-3581mm)', 
11: '3.58-3.93m 	(3582-3934mm)', 
12: '3.93-4.28m 	(3934-4287mm)',
13: '4.28-4.64m 	(4288-4640mm)',
14: '4.64-4.99m 	(4641-4993mm)',
15: '4.99-5.34m 	(4994-5346mm)',
16: '5.34-5.59m 	(5347-5599mm)',
17: '5.6-5.85m  	(5600-5852mm)',
18: '5.85-6.1m  	(5853-6105mm)',
19: '6.1-6.35m  	(6106-6358mm)',
20: '6.35-6.61m 	(6359-6611mm)',
21: '6.61-6.86m 	(6612-6864mm)',
22: '6.86-7.11m 	(6865-7117mm)',
23: '7.11-7.37m 	(7117-7370mm)',
24: '7.37-7.62m 	(7371-7623mm)',
25: '7.62-7.87m 	(7624-7876mm)',
26: '7.87-8.12m 	(7877-8129mm)',
27: '8.13-8.38m 	(8130-8382mm)',
28: '8.38-8.63m 	(8383-8635mm)',
29: '8.63-8.88m 	(8636-8888mm)',
30: '8.88-9.14m 	(8889-9141mm)',
31: '9.14-9.39m  	(9142-9394mm)',
32: 'None'
}
'''

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

plt.savefig("sensorsPlot.svg")

os.system("scp xBandData.txt pirData.txt srf08Data.txt sensorsPlot.svg ivan@10.33.21.174:/home/ivan/sensors")






















import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})
import random
import numpy as np
import math
#sys.argv[1] - number of file e.g. *.txt
#sys.argv[2] - comment to plot, e.g. low sensetivity
#sys.argv[3] - path to save file

xBandData = []
xBandTime = []
pirData = []
pirTime = []

row_data = open("row_data_" + sys.argv[1] + ".txt", "r")
for line in row_data:
	string = line.split()
<<<<<<< HEAD
	xBandData.append(string[0])
	xBandTime.append(string[1])
	#pirData.append(string[2])
	#pirTime.append(string[3])	
=======
	xBandData.append(float(string[0]))
	xBandTime.append(float(string[1]))
	pirData.append(float(string[2]))
	pirTime.append(float(string[3]))	
>>>>>>> 96f1f8c403b5dfa5f7258352ab753b402c90221f
row_data.close()
ideal = []
#ideal motion
ideal_space_time = np.linspace(0, 30, num=30000)

for i,element in enumerate(ideal_space_time):
	if i <= 5000:
		ideal.append(0)
	if i > 5000 and i <= 15000:
		ideal.append(1)
	if i > 15000 and i <= 20000:
		ideal.append(0)
	if i > 20000 :
		ideal.append(1)

# demodulation 1
dm1Array = []
dm1time = []
for i, element in enumerate(xBandData):
	if element > xBandData[i - 1]:
		dm1time.append(xBandTime[i])
		
for i, element in enumerate(dm1time):
	if i > 0:
		dm1Array.append(1/(dm1time[i] - dm1time[i-1]))

dm1time.insert(0,0)
dm1Array.insert(0,0)
dm1Array.append(0)

# estimation level for dm1
levelDm = []
level = max(dm1Array) * 20 / 100
for i in enumerate(dm1Array):
	levelDm.append(level)

#demodulation 2
dm2Array = []
halfArray = []
dm2time = []
window = int(sys.argv[4])
a = 0
for i, element in enumerate(xBandData):
	if i == window:
		for n, l in enumerate (xBandData[i-window : i+window]):
			if l == 1:
				a += l
		dm2Array.append(a)
		dm2time.append(xBandTime[i])
	if i > window and i < len(xBandData) - window:
		a = a - xBandData[i - window] + xBandData [i + window]
		dm2Array.append(a)
		dm2time.append(xBandTime[i])

# / add lie 1
for i, element in enumerate(dm2Array [ : window]):
	halfArray.insert(0, dm2Array[i] - 300)
	dm2time.insert(i,(xBandTime[i]))
dm2Array = halfArray + dm2Array 
#  add lie 2
halfArray = []
for i, element in enumerate(dm2Array [ len(dm2Array) - window : ]):
	halfArray.insert(0, dm2Array[len(dm2Array) - window + i] - 200)
	dm2time.append(xBandTime[len(xBandTime) - window + i ])
dm2Array = dm2Array + halfArray 
# / add lie 2
temp = []
mean = []
# mean
for i, element in enumerate(dm2Array):
	temp.append(element)
	if i % 2000 == 0:
		mean.append(sum(temp)/len(temp))
		temp = []
temp = []
stDev = []
st = []
q = []
# standart deviation
for i, element in enumerate(dm2Array[:50]):
	mm = sum(dm2Array[:50])/len(dm2Array[:50])
	temp.append(element-mm)
s = (sum(temp))/len(temp)
l = math.sqrt(s)
print s

		#st = []
		#q.append(l)

# estimation level for dm2
level = (max(dm2Array) * 95 / 100)
levelDm2 = []
for i in enumerate(dm2Array):
	levelDm2.append(level)

plt.figure(1)
plt.subplots_adjust(hspace = .4)

tl = 0
<<<<<<< HEAD
th = 5
'''
if int (sys.argv[1]) < 2 :
	plt.suptitle("Sensors response for " + sys.argv[1] + " meter, " + sys.argv[2], fontsize = 18)
else:
	plt.suptitle("Sensors response for " + sys.argv[1] + " meters, " + sys.argv[2], fontsize = 18)
'''

gs1 = GridSpec(1, 1)
gs1.update(left=0.03, right=0.98, wspace=0)
'''
pir = plt.subplot(gs1[0])
pir.plot(pirTime, pirData, 'r')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.title('PIR sensor')
'''
xband = plt.subplot(gs1[0])
=======
th = 30

plt.suptitle("Sensors response for " + sys.argv[1] + " meters, " + sys.argv[2], fontsize = 15)

gs1 = GridSpec(6, 1)
gs1.update(left=0.05, right=0.98, wspace=0)

idp = plt.subplot(gs1[0])
idp.plot(ideal_space_time,ideal ,'r', linewidth=3.5)
plt.ylabel('Motion status')
plt.axis([tl,th,0,1.1])
plt.title('Ideal motion, (a)')

pir = plt.subplot(gs1[1])
pir.plot(pirTime, pirData, 'm')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.title('PIR detector signal, (b)')

xband = plt.subplot(gs1[2])
>>>>>>> 96f1f8c403b5dfa5f7258352ab753b402c90221f
xband.plot(xBandTime, xBandData, 'b')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.title('X-band detector signal, (c)')

dm = plt.subplot(gs1[3])
dm.plot( dm1time,dm1Array, 'k', linewidth=2)
dm.plot( dm1time,levelDm,'r--', linewidth=2)
plt.ylabel('Motion status')
plt.title('Frequency demodulation X-band detector signal, (d)')

dm1 = plt.subplot(gs1[4])
dm1.plot( dm2time, dm2Array, 'g',linewidth=2)
dm1.plot( dm2time, levelDm2, 'r--',linewidth=2)
plt.ylabel('Motion status')
plt.xlabel('Time, s')
<<<<<<< HEAD
plt.title('X-band motion sensor')
'''
if int (sys.argv[1]) < 10 :
	plt.savefig(sys.argv[3] + "0" + sys.argv[1] + "_meters.png")
else :
	plt.savefig(sys.argv[3] + sys.argv[1] + "_meters.png")
	'''
=======
plt.title('Convolutional demodulation X-band detector signal, (e)')

m = plt.subplot(gs1[5])
m.plot(l)



plt.savefig(sys.argv[3] + sys.argv[1] + ".png")

>>>>>>> 96f1f8c403b5dfa5f7258352ab753b402c90221f
plt.show()
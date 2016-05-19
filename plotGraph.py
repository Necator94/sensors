import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})
import random
import numpy as np
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
	xBandData.append(float(string[0]))
	xBandTime.append(float(string[1]))
	pirData.append(float(string[2]))
	pirTime.append(float(string[3]))	
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
period = []
time_ = []
for i, element in enumerate(xBandData):
	if element > xBandData[i - 1]:
		time_.append(xBandTime[i])
		
for i, element in enumerate(time_):
	if i > 0:
		period.append(1/(time_[i] - time_[i-1]))

time_.insert(0,0)
period.insert(0,0)
period.append(0)
# /demodulation 1


#demodulation 2

new = []
test = []
new_time = []
window = int(sys.argv[4])
a = 0
for i, element in enumerate(xBandData):
	if i == window:
		for n, l in enumerate (xBandData[i-window : i+window]):
			if l == 1:
				a += l
		new.append(a)
		new_time.append(xBandTime[i])
	if i > window and i < len(xBandData) - window:
		a = a - xBandData[i - window] + xBandData [i + window]
		new.append(a)
		new_time.append(xBandTime[i])
# /demodulation 2
# / add lie 1
for i, element in enumerate(new [ : window]):
	test.insert(0, new[i] - 300)
	new_time.insert(i,(xBandTime[i]))

new = test + new 
#  add lie 2
test = []

for i, element in enumerate(new [ len(new) - window : ]):
	test.insert(0, new[len(new) - window + i] - 200)
	
	new_time.append(xBandTime[len(xBandTime) - window + i ])

new = new + test 
# / add lie 2

plt.figure(1)
plt.subplots_adjust(hspace = .4)



tl = 0
th = 30

plt.suptitle("Sensors response for " + sys.argv[1] + " meters, " + sys.argv[2], fontsize = 15)
#srf08
gs1 = GridSpec(5, 1)
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
xband.plot(xBandTime, xBandData, 'b')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.title('X-band detector signal, (c)')


dm = plt.subplot(gs1[3])
dm.plot( time_,period, 'k',linewidth=2)
plt.ylabel('Motion status')
plt.title('Frequency demodulation X-band detector signal, (d)')

dm1 = plt.subplot(gs1[4])
dm1.plot( new_time, new, 'g',linewidth=2)
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('Convolutional demodulation X-band detector signal, (e)')


plt.savefig(sys.argv[3] + sys.argv[1] + ".png")

plt.show()
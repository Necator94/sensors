import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})

#sys.argv[1] - distance to motion
#sys.argv[2] - comment to plot, e.g. X-band sensetivity
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

plt.figure(1)
plt.subplots_adjust(hspace = .4)

tl = 0
th = 30

plt.suptitle("Sensors response for " + sys.argv[1] + ", " + sys.argv[2], fontsize = 15)
#srf08
gs1 = GridSpec(3, 1)
gs1.update(left=0.03, right=0.98, wspace=0)

pir = plt.subplot(gs1[0])
pir.plot(pirTime, pirData, 'r')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.title('PIR sensor')

xband = plt.subplot(gs1[1])
xband.plot(xBandTime, xBandData, 'b')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')

plt.title('X-band motion sensor')

dm = plt.subplot(gs1[2])
dm.plot( time_,period, 'r')
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('PIR sensor')
#plt.savefig(sys.argv[3] + sys.argv[1] + ".png")

plt.show()
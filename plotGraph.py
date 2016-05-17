import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})

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

# demodulation
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
# /demodulation

plt.figure(1)
plt.subplots_adjust(hspace = .4)

tl = 0
th = 30

plt.suptitle("Sensors response for " + sys.argv[1] + " meters, " + sys.argv[2], fontsize = 15)
#srf08
gs1 = GridSpec(3, 1)
gs1.update(left=0.04, right=0.98, wspace=0)

pir = plt.subplot(gs1[0])
pir.plot(pirTime, pirData, 'r')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.title('PIR detector')
plt.xlabel('(a)')

xband = plt.subplot(gs1[1])
xband.plot(xBandTime, xBandData, 'b')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.xlabel('(b)')
plt.title('X-band detector')

dm = plt.subplot(gs1[2])
dm.plot( time_,period, 'b')
plt.ylabel('Motion status')
plt.xlabel('Time, s'+ '\n'+'(c)')

plt.title('Demodulated signal for X-band detector ')
plt.savefig(sys.argv[3] + sys.argv[1] + ".png")

plt.show()
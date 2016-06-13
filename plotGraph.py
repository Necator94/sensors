import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})

#sys.argv[1] - number of experiment
#sys.argv[2] - X-band sensetivity
#sys.argv[3] - path to saved file

xBandData = []
xBandTime = []
pirData = []
pirTime = []

row_data = open("row_data_" + sys.argv[1] + ".txt", "r")
for line in row_data:
	string = line.split()
	xBandData.append(string[0])
	xBandTime.append(string[1])
	#pirData.append(string[2])
	#pirTime.append(string[3])	
row_data.close()

plt.figure(1)
plt.subplots_adjust(hspace = .4)

tl = 0
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
xband.plot(xBandTime, xBandData, 'b')
plt.axis([tl,th,0,1.1])
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('X-band motion sensor')
'''
if int (sys.argv[1]) < 10 :
	plt.savefig(sys.argv[3] + "0" + sys.argv[1] + "_meters.png")
else :
	plt.savefig(sys.argv[3] + sys.argv[1] + "_meters.png")
	'''
plt.show()
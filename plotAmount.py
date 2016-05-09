import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})

# sys.argv[1] - amount of datafiles in folder + 1
# sys.argv[2] - comment to graph after subtitle


i = 1
while i < int(sys.argv[1]) :

	xBandData = []
	xBandTime = []
	pirData = []
	pirTime = []

	row_data = open("row_data_" + str(i) + ".txt", "r")
	for line in row_data:
		string = line.split()
		xBandData.append(string[0])
		xBandTime.append(string[1])
		pirData.append(string[2])
		pirTime.append(string[3])	
	row_data.close()
	
	plt.figure(i)
	plt.subplots_adjust(hspace = .4)

	tl = 0
	th = 30

	if i < 2 :
		plt.suptitle("Sensors response for " +str(i) + " meter, " + sys.argv[2], fontsize = 15)
	else:
		plt.suptitle("Sensors response for " +str(i) + " meters, " + sys.argv[2], fontsize = 15)
	#srf08
	gs1 = GridSpec(2, 1)
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
	plt.xlabel('Time, s')
	plt.title('X-band motion sensor')

	if i < 10 :
		plt.savefig("0" + str(i) + "_meters.png")
	else :
		plt.savefig(str(i) + "_meters.png")
	#plt.show()
	plt.close()
	
	i += 1
	




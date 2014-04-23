import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})

xBandData_ = []
xBandTime_ = []
pirData_ = []
pirTime_ = []
srf08Data_ = []
srf08Time_ = []
srfDistance_ = []
i = 1
while i < int(sys.argv[1]) :

	xBandtxt = open("xBandData" + "_" + str(i) + ".txt", "r")
	for line in xBandtxt:
		xBandData,xBandTime = line.split()
		xBandData_.append(xBandData)
		xBandTime_.append(xBandTime)		
	xBandtxt.close()

	pirtxt = open("pirData" + "_" + str(i) + ".txt", "r")
	for line in pirtxt:
	    	pirData,pirTime = line.split()
		pirData_.append(pirData)
		pirTime_.append(pirTime)		
	pirtxt.close()

	srf08txt = open("srf08Data" + "_" + str(i) + ".txt", "r")
	for line in srf08txt:
		srf08Data,srf08Time = line.split()
		srf08Data_.append(srf08Data)
		srf08Time_.append(srf08Time)
	srf08txt.close()
'''
	srf08Distancetxt = open("srf08Distance" + "_" + str(i) + ".txt", "r")
	for line in srf08Distancetxt:
		srfDistance_.append(line)		
	srf08Distancetxt.close()
'''
	plt.figure(i)
	plt.subplots_adjust(hspace = .4)

	tl = 0
	th = 30

	if i < 2 :
		plt.suptitle("Sensors response for " +str(i) + " meter, " + sys.argv[2], fontsize = 15)
	else:
		plt.suptitle("Sensors response for " +str(i) + " meters, " + sys.argv[2], fontsize = 15)
	#srf08
	gs1 = GridSpec(3, 3)
	gs1.update(left=0.03, right=0.98, wspace=0)

	pir = plt.subplot(gs1[1,:])
	pir.plot(pirTime_, pirData_, 'r')
	plt.axis([tl,th,0,1.1])
	plt.ylabel('Motion status')
	plt.title('PIR sensor')

	srf08 = plt.subplot(gs1[:1, :])
	srf08.plot(srf08Time_, srf08Data_, 'g')
	plt.axis([tl,th,0,1.1])
	plt.ylabel('Motion status')
	plt.title('Ultrasonic SRF08 sensor')

	xband = plt.subplot(gs1[-1, :])
	xband.plot(xBandTime_, xBandData_, 'b')
	plt.axis([tl,th,0,1.1])
	plt.ylabel('Motion status')
	plt.xlabel('Time, s')
	plt.title('X-band motion sensor')

	if i < 10 :
		plt.savefig("/home/necator/Dropbox/experiments/night_experiment/" + "0" + str(i) + "_meters.png")
	else :
		plt.savefig("/home/necator/Dropbox/experiments/night_experiment/" + str(i) + "_meters.png")
	plt.close()
	
	i += 1
	#plt.show()




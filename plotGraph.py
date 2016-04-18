import matplotlib
import matplotlib.pyplot as plt


xBandData_ = []
xBandTime_ = []
pirData_ = []
pirTime_ = []
srf08Data_ = []
srf08Time_ = []
srfDistance_ = []

xBandtxt = open("xBandData.txt", "r")
for line in xBandtxt:
	xBandData,xBandTime = line.split()
	xBandData_.append(xBandData)
	xBandTime_.append(xBandTime)		
xBandtxt.close()

pirtxt = open("pirData.txt", "r")
for line in pirtxt:
    	pirData,pirTime = line.split()
	pirData_.append(pirData)
	pirTime_.append(pirTime)		
pirtxt.close()

srf08txt = open("srf08Data.txt", "r")
for line in srf08txt:
	srf08Data,srf08Time = line.split()
	srf08Data_.append(srf08Data)
	srf08Time_.append(srf08Time)
srf08txt.close()

srf08Distancetxt = open("srf08Distance.txt", "r")
for line in srf08Distancetxt:
	srfDistance_.append(line)		
srf08Distancetxt.close()

plt.figure(1)
#plt.subplots_adjust(hspace = .4)

tl = 0
th = 30
#srf08
plt.subplot(311)
plt.plot(srf08Time_, srf08Data_, 'g')
plt.scatter(srf08Time_, srf08Data_)

for k in xrange(len(srfDistance_)):
	if float(srf08Data_[k]) != 0:
    		plt.text(srf08Time_[k],float(srf08Data_[k]) + 0.1, srfDistance_[k], rotation='vertical', fontsize=8, horizontalalignment='left',verticalalignment='bottom',)

plt.axis([tl,th,0,1.5])
plt.ylabel('Motion status')
plt.title('Ultrasonic SRF08 sensor')

#pir
plt.subplot(312)
plt.plot(pirTime_, pirData_, 'r')
plt.axis([tl,th,0,1.5])
plt.ylabel('Motion status')
plt.title('PIR sensor')

#x-band
plt.subplot(313)
plt.plot(xBandTime_, xBandData_, 'b')
plt.axis([tl,th,0,1.5])
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('X-band motion sensor')

plt.show()
plt.savefig("Plot.svg")

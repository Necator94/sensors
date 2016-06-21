import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (25.0,13.0)})
import random
import numpy as np
import math



xBand_raw_time = []
xBand_raw_data = []
xBand_fr_transform_time = []
xBand_fr_transform_data = []

xBand_detect_time = []
xBand_detect_status = []
xBand_detect_mean = []
xBand_detect_std = []

raw_data_flag = 'foo bar'
xBand_fr_transform_flag = 'foo bar'
xBand_detect_signal_flag = 'foo bar'

plot_data = open("plot_data_" + ".txt", "r")
for line in plot_data:

	if line == "row_data\n" : 
		raw_data_flag = True 
		continue
	if line == "/end_of_row_data\n" : 
		raw_data_flag = False
		continue
	if raw_data_flag == True: 
		string = line.split()
		xBand_raw_time.append(string[0])
		xBand_raw_data.append(string[1])

	if line == "xBand_fr_transform\n" : 
		xBand_fr_transform_flag = True 
		continue
	if line == "/end_of_xBand_fr_transform\n" : 
		xBand_fr_transform_flag = False
		continue
	if xBand_fr_transform_flag == True: 
		string = line.split()
		xBand_fr_transform_time.append(string[0])
		xBand_fr_transform_data.append(string[1])
	
	if line == "xBand_detect_signal\n" : 
		xBand_detect_signal_flag = True 
		continue
	if line == "/end_of_xBand_detect_signal\n" : 
		xBand_detect_signal_flag = False
		continue
	if xBand_detect_signal_flag == True: 
		string = line.split()
		xBand_detect_time.append(string[0])
		xBand_detect_status.append(string[1])
		xBand_detect_mean.append(string[2])
		xBand_detect_std.append(string[3])


gs1 = GridSpec(2, 2)
gs1.update(left=0.03, right=0.98, wspace=0.1)

raw_plt = plt.subplot(gs1[0])
raw_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
raw_plt.plot(xBand_raw_time, xBand_raw_data, 'b')
plt.axis([0,10,0,1.1])							#limits can be taken from metadata
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('Raw X-Band detector signal')


fr_tr_plt = plt.subplot(gs1[1])
fr_tr_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
fr_tr_plt.plot(xBand_fr_transform_time, xBand_fr_transform_data, 'b',linewidth=2)
plt.ylabel('Movement intensity')
plt.xlabel('Time, s')
plt.title('Frequency transformation graph')


mean_allocation = []
mean_allocation.append([]) 
mean_allocation.append([])
for i in range(len(xBand_detect_mean)):
	if xBand_detect_mean[i] > 40:
		print xBand_detect_mean[i]
		mean_allocation[0].append(xBand_detect_time[i])
		mean_allocation[1].append(xBand_detect_mean[i])
		print len(mean_allocation[1])

gs2 = GridSpec(2, 2)
gs2.update(left=0.03, right=0.98, wspace=0.1)

levelDm = []									# estimation level for mean value
level = 30   									#from metadata
for i in enumerate(xBand_detect_mean):
	levelDm.append(level)
detect_plt = plt.subplot(gs2[2])
detect_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
detect_plt.plot(xBand_detect_time, xBand_detect_mean, 'k', linestyle='-', linewidth=3, label="mean value of the signal")
detect_plt.plot(xBand_detect_time, levelDm,'k',linestyle='--',linewidth=2, label="criteria of estimation")
plt.legend(loc='upper left', frameon=False)
plt.ylabel('Mean value of frequency')
plt.xlabel('Time, s')
plt.title('Mean values graph')

detect_plt = plt.subplot(gs2[3])
detect_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
detect_plt.plot(xBand_detect_time, xBand_detect_std, 'g',linestyle=':', linewidth=4, label="standard deviation value of the signal")
plt.legend(loc='upper left', frameon=False)
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('Movement detection graph')
'''
gs3 = GridSpec(5, 1)
gs3.update(left=0.03, right=0.98, wspace=0)
detect_plt = plt.subplot(gs3[4])
detect_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
detect_plt.plot(xBand_detect_time, xBand_detect_std, 'g',linestyle=':', linewidth=4, label="standard deviation value of the signal")
detect_plt.plot(xBand_detect_time, xBand_detect_mean, 'k', linestyle='-', linewidth=3, label="mean value of the signal")
#detect_plt.plot(xBand_detect_time, xBand_detect_status, 'r', linewidth=4, label="movement is detected")
plt.legend(loc='upper left', frameon=False)
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('Movement detection graph')
'''
'''
for i in range(len(xBand_detect_status)):  
	if xBand_detect_status[i] == 'True': xBand_detect_status[i] = 10
	if xBand_detect_status[i] == 'False': xBand_detect_status[i] = 0
detect_plt.plot(xBand_detect_time, xBand_detect_status, 'r', linewidth=4, label="movement is detected")
'''

plt.show()





import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})
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


gs1 = GridSpec(2, 1)
gs1.update(left=0.03, right=0.98, wspace=0)

raw_plt = plt.subplot(gs1[0])
raw_plt.plot(xBand_raw_time, xBand_raw_data, 'b')
raw_plt.plot(xBand_fr_transform_time, xBand_fr_transform_data, 'b')
plt.ylabel('Motion status')
plt.title('Raw X-Band detector data')

detect_plt = plt.subplot(gs1[1])
detect_plt.plot(xBand_detect_time, xBand_detect_status, 'r')
detect_plt.plot(xBand_detect_time, xBand_detect_mean, 'k')
detect_plt.plot(xBand_detect_time, xBand_detect_std, 'g')
plt.ylabel('Motion status')
plt.title('Raw X-Band detector data')

'''
fr_ = plt.subplot(gs1[1])

fr_.plot(xBand_time1, std_graph, 'g')
plt.ylabel('Motion status')
plt.title('Frequency transformation')
'''
plt.show()





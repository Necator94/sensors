import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (20.0,12.0)})
import random
import numpy as np
import math



xBand_time = []
xBand_fr = []

xBand_time1 = []
xBand_s = []
std_graph = []
mean_graph = []

raw_data = open("plot_data_" + ".txt", "r")
for line in raw_data:
	string = line.split()
	xBand_time.append(string[0])
	xBand_fr.append(string[1])

raw_data1 = open("detect_signal_" + ".txt", "r")
for line in raw_data1:
	string = line.split()
	xBand_time1.append(string[0])
	xBand_s.append(string[1])
	mean_graph.append(string[2])
	std_graph.append(string[3])

gs1 = GridSpec(1, 1)
gs1.update(left=0.03, right=0.98, wspace=0)

fr_tr = plt.subplot(gs1[0])
fr_tr.plot(xBand_time, xBand_fr, 'b')
fr_tr.plot(xBand_time1, xBand_s, 'r')
fr_tr.plot(xBand_time1, mean_graph, 'k')
fr_tr.plot(xBand_time1, std_graph, 'g')

plt.ylabel('Motion status')
plt.title('Frequency transformation')

'''
fr_ = plt.subplot(gs1[1])

fr_.plot(xBand_time1, std_graph, 'g')
plt.ylabel('Motion status')
plt.title('Frequency transformation')
'''
plt.show()





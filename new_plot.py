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

raw_data = open("plot_data_" + ".txt", "r")
for line in raw_data:
	string = line.split()
	xBand_time.append(string[0])
	xBand_fr.append(string[1])

gs1 = GridSpec(1, 1)
gs1.update(left=0.03, right=0.98, wspace=0)

fr_tr = plt.subplot(gs1[0])
fr_tr.plot(xBand_time, xBand_fr, 'r')
plt.ylabel('Motion status')
plt.title('Frequency transformation')

plt.show()





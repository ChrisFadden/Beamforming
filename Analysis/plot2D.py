import h5py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#******************
#   Read in data
#******************
fp = '../build/weights_2D.h5'

f5 = h5py.File(fp,"r")
azm = np.asarray(f5['/listAzm'])
elev = np.asarray(f5['/listElev'])
mag = np.asarray(f5['/Magnitude'])

#*******************
#   Set asthetics
#*******************
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

#*******************
#   Create heatmap
#*******************
sns.heatmap(mag,cmap = "viridis",
    cbar_kws={"shrink": 0.40,"aspect": 10,"label": "Magnitude (dB)"},
    square=True,xticklabels=30,yticklabels=30,vmin=-30,vmax=0,
    rasterized=True)

#******************
#   Add titles and
#   labels
#******************
plt.title("2D Beamformed Response",fontsize=14)
plt.xlabel("Range (m)")
plt.ylabel("Cross-Range (m)")

plt.show()
#plt.savefig("Heatmap.pdf",bbox_inches='tight')

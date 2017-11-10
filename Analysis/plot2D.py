import h5py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#******************
#   Read in data
#******************
fp = '../build/output.h5'

f5 = h5py.File(fp,"r")
azm = np.asarray(f5['/Parameters/listAzm'])
elev = np.asarray(f5['/Parameters/listElev'])
mag = np.asarray(f5['/2D Beamforming/MVDR/Magnitude'])

#*******************
#   Set asthetics
#*******************
plt.style.use("bmh")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

#*******************
#   Create heatmap
#*******************
sns.heatmap(mag,cmap = "viridis",
    cbar_kws={"shrink": 0.30,"aspect": 10,"label": "Magnitude (dB)"},
    square=True,xticklabels=30,yticklabels=30,vmin=-30,vmax=0,
    rasterized=True)

#******************
#   Add titles and
#   labels
#******************
plt.title("2D Beamformed Response",fontsize=14)
plt.xlabel("Down-Range (m)")
plt.ylabel("Cross-Range (m)")

plt.show()
#plt.savefig("Heatmap.pdf",bbox_inches='tight')

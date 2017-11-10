import h5py
import numpy as np
import matplotlib.pyplot as plt

#******************
#   Read in data
#******************
fp = '../build/output.h5'

f5 = h5py.File(fp,"r")
azm = np.asarray(f5['/Parameters/listAzm'])
music = np.asarray(f5['/Direction Finding/MUSIC'])
bart = np.asarray(f5['/Direction Finding/Bartlett'])

#*******************
#   Set asthetics
#*******************
plt.style.use("ggplot")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

#*******************
#   Plot and add
#   legend
#*******************
pmusic = plt.plot(azm,music[0:len(azm)],'k-',label = "MUSIC")
pbart = plt.plot(azm,bart[0:len(azm)],'k:',label = "Bartlett")

plt.legend(handles=[pmusic[0],pbart[0]],title="Algorithm",bbox_to_anchor=(0.9,1))


#******************
#   Add titles and
#   labels
#******************
plt.title("Array Response",fontsize=14)
plt.xlabel("Azimuth (deg.)")
plt.ylabel("Magnitude (dB)")

plt.show()
#plt.savefig("Heatmap.pdf",bbox_inches='tight')

import h5py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

fp = '../build/weights_2D.h5'

f5 = h5py.File(fp,"r")
azm = np.asarray(f5['/listAzm'])
elev = np.asarray(f5['/listElev'])
mag = np.asarray(f5['/Magnitude'])

sns.heatmap(mag,cmap="jet",square=True,xticklabels=30,yticklabels=30,vmin=-30,vmax=0)
plt.show()

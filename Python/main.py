import h5py
import numpy as np
import random
import DF.bartlett as ds
import matplotlib.pyplot as plt

ds.hello()

#Signal of Interest
SOI = [30]

#Signal to Noise Ratio (dB)
SNR = 30

fp = '../build/testnec.h5'
dp = '/289.8/90.0/'
f5 = h5py.File("../build/testnec.h5","r")

#get Azimuths
azm = np.asarray(f5['/listAzm'])

#get Array Manifold
d5 = f5[dp]
AM_mag = np.asarray(d5['Magnitude'])
AM_phase = np.asarray(d5['Phase'])
AM_herm = np.asarray(d5['Hermitian'])

#create signal
x = AM_mag[SOI,:] * np.exp(1j * AM_phase[SOI,:])
noise = 10**(-SNR / 10)
x += (np.min(x) * noise * np.random.randn(len(x.transpose())))
Rxx = np.dot(x.transpose(),x)

Pds = ds.getSpectrum(Rxx,AM_mag,AM_herm)


plt.plot(azm,P)
plt.show()

print("Hello World")

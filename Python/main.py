import h5py
import numpy as np
import random
import DF.bartlett as ds
import DF.mvdr as mvdr
import DF.music as MUSIC
import matplotlib.pyplot as plt

#Signal of Interest
SOI = [30]

#Signal to Noise Ratio (dB)
SNR = 30

#fp = '../build/testnec.h5'
fp = '../build/ULA.hdf5'
#dp = '/289.8/90.0/'
dp = '/299.8/90.0/'
f5 = h5py.File(fp,"r")

#get Azimuths
azm = np.asarray(f5['/listAzm']).T

#get Array Manifold
d5 = f5[dp]
AM_mag = (np.asarray(d5['Magnitude'])).T
AM_phase = (np.asarray(d5['Phase'])).T
AM_herm = (np.asarray(d5['Hermitian'])).T

#create signal
x = AM_mag[:,SOI] * np.exp(1j * AM_phase[:,SOI])
noise = 10**(-SNR / 10)
#x += (0.001 * np.min(abs(x)) * noise * np.random.randn(len(x),1))
Rxx = np.dot(x,x.conj().T) + noise * np.eye(5)

Pds = ds.getSpectrum(Rxx,AM_mag,AM_herm)
Pmvdr = mvdr.getSpectrum(Rxx,AM_mag,AM_herm)
Pmusic = MUSIC.getSpectrum(Rxx,AM_mag,AM_herm,len(SOI))

MUSIC.hello()
plt.plot(azm,Pmusic)
plt.show()

print("Hello World")

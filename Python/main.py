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

#fp = '../build/Test.h5'
fp = '../build/ULA.h5'

f5 = h5py.File(fp,"r")

#get Azimuths
azm = np.asarray(f5['/listAzm']).T

#get Array Manifold
AM_mag = (np.asarray(f5['/Magnitude'])).T
AM_phase = (np.asarray(f5['/Phase'])).T

#create signal
freq = np.asarray(f5['/listFreq']).T
elev = np.asarray(f5['/listElev']).T

soiIdx = 1*len(freq) * 0*len(elev) + SOI[0]

x = AM_mag[:,SOI] * np.exp(1j * AM_phase[:,SOI])
noise = 10**(-SNR / 10)
Rxx = np.dot(x,x.conj().T) + noise * np.eye(5)

##Get the Spectrum
Pds = ds.getSpectrum(Rxx,AM_mag,-1*AM_phase)
Pmvdr = mvdr.getSpectrum(Rxx,AM_mag,-1*AM_phase)
Pmusic = MUSIC.getSpectrum(Rxx,AM_mag,-1*AM_phase,len(SOI))

##Find range to plot azm
dsIdx = (np.argmax(Pds) // len(azm))*len(azm)
mvdrIdx = (np.argmax(Pmvdr) // len(azm))*len(azm)
musicIdx = (np.argmax(Pmusic) // len(azm))*len(azm)

##Plot Spectrum
ds.hello()
plt.plot(azm,Pds[dsIdx:dsIdx + len(azm)])
plt.show()

print("Hello World")

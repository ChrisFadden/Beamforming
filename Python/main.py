import h5py
import numpy as np
import random
import DF.bartlett as DS
import DF.mvdr as MVDR
import DF.music as MUSIC
import WEIGHT.mvdr as mvdr
import WEIGHT.arrayFactor as AF
import matplotlib.pyplot as plt

def plot_DF_Spectrum(P, azm):
    idx = (np.argmax(P) // len(azm))*len(azm)
    plt.plot(azm,P[idx:idx + len(azm)])
    plt.show()

def plot_Beamform_Spectrum(w,AM_mag,AM_phase,azm,idx):
    y = 0*azm 
    AM_mag[:,idx:idx + len(azm)] = AM_mag[:,idx:idx + len(azm)] / np.max(AM_mag[:,idx:idx+len(azm)])
    for ii in range(len(azm)):
        y[ii] = np.abs(np.dot(w.conj(), AM_mag[:,idx + ii] * np.exp(1j * AM_phase[:,idx + ii])))
    y = y / np.max(y)
    
    offset = int(np.round(0.5*len(azm))) 
    plt.plot(azm - offset,20*np.log10(np.roll(y,offset)))
    plt.show()

#***********************
#   Simulation Parameters
#***********************
#Signal of Interest
SOI = [0]

#Signal to Noise Ratio (dB)
SNR = 90

fp = '../build/Test.h5'
#fp = '../build/ULA.h5'

f5 = h5py.File(fp,"r")

#**********************
#   Read-in Data
#**********************
#get Parameters
azm = np.asarray(f5['/listAzm']).T
freq = np.asarray(f5['/listFreq']).T
elev = np.asarray(f5['/listElev']).T

#get Array Manifold
AM_mag = (np.asarray(f5['/Magnitude'])).T
AM_phase = (np.asarray(f5['/Phase'])).T

#**********************
#   Create Signal
#**********************

freqIdx = 1;
elevIdx = 0;

soiIdx = freqIdx*elevIdx*len(azm) +  SOI[0]

x = AM_mag[:,soiIdx] * np.exp(1j * AM_phase[:,soiIdx])

noise = 10**(-SNR / 10)
Rxx = np.outer(x,x.conj()) + noise * np.eye(5)

#**********************
#   Direction Finding
#**********************
#Get the Spectrum
Pds = DS.getSpectrum(Rxx,AM_mag,-1*AM_phase)
Pmvdr = MVDR.getSpectrum(Rxx,AM_mag,-1*AM_phase)
Pmusic = MUSIC.getSpectrum(Rxx,AM_mag,-1*AM_phase,len(SOI))

#*****************
#   Beamforming
#*****************

wmvdr = mvdr.getWeights(np.eye(5),AM_mag[:,soiIdx],AM_phase[:,soiIdx])
wAF = AF.getWeights(5,0.5,2*np.pi,SOI[0])
wones = np.ones((1,5))
plot_Beamform_Spectrum(wones,AM_mag,AM_phase,azm,soiIdx - SOI[0])

#Plot Spectrum
#plot_DF_Spectrum(Pmusic,azm)

print("Hello World")

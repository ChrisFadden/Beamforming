import h5py
import numpy as np
import random
import DF.bartlett as DS
import DF.mvdr as MVDR
import DF.music as MUSIC
import DF.rootmusic as ROOT
import WEIGHT.mvdr as mvdr
import WEIGHT.arrayFactor as AF
import matplotlib.pyplot as plt

def plot_DF_Spectrum(P, azm):
    idx = (np.argmax(P) // len(azm))*len(azm)
    plt.plot(azm,P[idx:idx + len(azm)])
    plt.show()

def plot_Beamform_Spectrum(w,AM_mag,AM_phase,azm,idx,ifPlot = True):
    y = 0*azm 
    AM_mag[:,idx:idx + len(azm)] = AM_mag[:,idx:idx + len(azm)] / np.max(AM_mag[:,idx:idx+len(azm)])
    for ii in range(len(azm)):
        y[ii] = np.abs(np.dot(w.conj(), AM_mag[:,idx + ii] * np.exp(1j * AM_phase[:,idx + ii])))
    y = y / np.max(y)
    
    offset = int(np.round(0.5*len(azm)))
    
    azm = azm - offset
    Mag = 20*np.log10(np.roll(y,offset))
    
#    print(Mag[120])
    print("I think something is wrong when Test.h5 is used at DC")
    print("The magnitude should be 0 dB at SOI, but it doesn't give that...") 
     
    if(ifPlot):
        plt.plot(azm,Mag)
        plt.show()
    return azm, Mag
#***********************
#   Simulation Parameters
#***********************
#Signal of Interest
SOI = [20]

#Signal to Noise Ratio (dB)
SNR = 50

#fp = '../build/Test.h5'
fp = '../build/ULA.h5'

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

#freqIdx = 10;
elevIdx = 1;
freqIdx = 0

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
Proot = ROOT.getSpectrum(Rxx,len(SOI))
print(Proot)
#*****************
#   Beamforming
#*****************

wmvdr = mvdr.getWeights(np.eye(5),AM_mag[:,soiIdx],AM_phase[:,soiIdx])
wAF = AF.getWeights(5,0.5,2*np.pi,SOI[0])
wones = np.ones((1,5))

pAzm, pMag = plot_Beamform_Spectrum(wmvdr,AM_mag,AM_phase,azm,soiIdx - SOI[0])

#Find Half Power Points
offset = np.round(len(azm)*0.5)
p3dB = np.array(np.where(pMag < -3))
u3dB = np.min(p3dB[p3dB > (SOI[0] + offset)]) - offset
l3dB = np.max(p3dB[p3dB < (SOI[0] + offset)]) - offset

#Save Spectrum
f5 = h5py.File("../build/weights.h5","w")
fazm = f5.create_dataset("listAzm", data = np.asarray(pAzm))
fmag = f5.create_dataset("Magnitude", data = np.asarray(pMag))
fsoi = f5.create_dataset("SOI", data = np.asarray(SOI[0]))
f3db = f5.create_dataset("HPP", data = np.asarray([u3dB,l3dB]))
fazm.dims[0].label = "Azimuth (degrees)"
fmag.dims[0].label = "Magnitude (dBV)" 
#Plot Spectrum
#plot_DF_Spectrum(Pmusic,azm)

print("Hello World")

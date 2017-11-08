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
import seaborn as sns

def plot_DF_Spectrum(P, azm):
    idx = (np.argmax(P) // len(azm))*len(azm)
    plt.plot(azm,P[idx:idx + len(azm)])
    plt.show()

def save_Beamform_Spectrum(w,AM_mag,AM_phase,azm,idx,SOI,ifPlot = True):
    y = 0*azm 
    
    for ii in range(len(azm)):
        y[ii] = np.abs(np.dot(w.conj(), AM_mag[:,idx + ii] * np.exp(1j * AM_phase[:,idx + ii])))
     
    Mag = 20*np.log10(y)
     
    if(ifPlot):
        plt.plot(azm,Mag)
        plt.show()


    #Find Half Power Points
    u3dB = np.max(azm)
    l3dB = np.min(azm)
    p3dB = np.array(np.where(Mag < -3))
    if(np.any(p3dB > SOI)): 
        u3dB = np.min(p3dB[p3dB > SOI]) 
    if(np.any(p3dB < SOI)):
        l3dB = np.max(p3dB[p3dB < SOI])

    #Save Spectrum
    f5 = h5py.File("../build/weights.h5","w")
    fazm = f5.create_dataset("listAzm", data = np.asarray(azm))
    fmag = f5.create_dataset("Magnitude", data = np.asarray(Mag))
    fsoi = f5.create_dataset("SOI", data = np.asarray(SOI))
    f3db = f5.create_dataset("HPP", data = np.asarray([u3dB,l3dB]))
    fazm.dims[0].label = "Azimuth (degrees)"
    fmag.dims[0].label = "Magnitude (dB)" 

    return

def plot_2D_Beamform_Spectrum(w,AM_mag,AM_phase,azm,elev,xSOI,ySOI,ifPlot = True):
    y = np.zeros((len(elev),len(azm))) 
    ii = 0 
    for th in range(len(elev)):
        for phi in range(len(azm)):
            y[th,phi] = np.abs(np.dot(w.conj(),AM_mag[:,ii]*np.exp(1j*AM_phase[:,ii])))
            ii = ii + 1
    
    Mag = 20*np.log10(y)

    if(ifPlot):
        sns.heatmap(Mag,cmap = "jet",square=True,xticklabels=30,yticklabels=30,vmax = 0,vmin = -40)
        plt.show()
    
    xu3dB = np.max(azm)
    xl3dB = np.min(azm)
    yu3dB = np.max(elev)
    yl3dB = np.min(elev)
    
    p3dB = np.array(np.where(Mag[ySOI,:] < -3))
    if(np.any(p3dB > xSOI)):
        xu3dB = np.min(p3dB[p3dB > xSOI]) 
    if(np.any(p3dB < xSOI)):
        xl3dB = np.max(p3dB[p3dB < xSOI])
    p3dB = np.array(np.where(Mag[:,xSOI] < -3))
    if(np.any(p3dB > ySOI)): 
        yu3dB = np.min(p3dB[p3dB > ySOI]) 
    if(np.any(p3dB < ySOI)):
        yl3dB = np.max(p3dB[p3dB < ySOI]) 
    
    #Save Spectrum
    f5 = h5py.File("../build/weights_2D.h5","w")
    fazm = f5.create_dataset("listAzm", data = np.asarray(azm))
    felev = f5.create_dataset("listElev", data = np.asarray(elev)) 
    fmag = f5.create_dataset("Magnitude", data = Mag)
    fsoi = f5.create_dataset("SOI", data = np.asarray([xSOI,ySOI]))
    f3db = f5.create_dataset("HPP", data = np.asarray([xu3dB,xl3dB,yu3dB,yl3dB]))
     
    return

#***********************
#   Simulation Parameters
#***********************
#Signal of Interest (relative to broadside)
SOI = [180]

#Signal to Noise Ratio (dB)
SNR = 50

#fp = '../build/Test.h5'
#fp = '../build/ULA.h5'
fp = '../build/URA.h5'

ySOI = 45
xSOI = 180
SOI = [ySOI*361 + xSOI]
#SOI = [10*361 + 180]
#SOI = [90*361 + 180]

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

soiIdx = SOI[0] #+ len(AM_phase[0,:]) - len(azm)

x = AM_mag[:,soiIdx] * np.exp(1j * AM_phase[:,soiIdx])

noise = 10**(-SNR / 10)
Rxx = np.outer(x,x.conj()) + noise * np.eye(len(AM_phase[:,0]))

#**********************
#   Direction Finding
#**********************
#Get the Spectrum
#Pds = DS.getSpectrum(Rxx,AM_mag,-1*AM_phase)
#Pmvdr = MVDR.getSpectrum(Rxx,AM_mag,-1*AM_phase)
#Pmusic = MUSIC.getSpectrum(Rxx,AM_mag,-1*AM_phase,len(SOI))
#Proot = ROOT.getSpectrum(Rxx,len(SOI))
#print(Proot)
#print(SOI[0])
#*****************
#   Beamforming
#*****************

wmvdr = mvdr.getWeights(Rxx,AM_mag[:,soiIdx],AM_phase[:,soiIdx])
#print(wmvdr)
#wAF = AF.getWeights(5,0.5,2*np.pi,SOI[0])
#wones = np.ones((1,5))

#save_Beamform_Spectrum(wmvdr,AM_mag,AM_phase,azm,soiIdx - SOI[0],SOI[0])
plot_2D_Beamform_Spectrum(wmvdr,AM_mag,AM_phase,azm,elev,xSOI,ySOI,False)

#Plot Spectrum
#plot_DF_Spectrum(Pmusic,azm)

print("Hello World")

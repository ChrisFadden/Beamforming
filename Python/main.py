import h5py
import numpy as np
import random

import DF.bartlett as DS
import DF.mvdr as MVDR
import DF.music as MUSIC
import DF.rootmusic as ROOT

import WEIGHT.mvdr as mvdr
import WEIGHT.arrayFactor as AF

import ecos

import matplotlib.pyplot as plt
import seaborn as sns



def plot_DF_Spectrum(P, azm):
    idx = (np.argmax(P) // len(azm))*len(azm)
    plt.plot(azm,P[idx:idx + len(azm)])
    plt.show()

def save_Beamform_Spectrum(w,AM_mag,AM_phase,azm,idx,SOI,h5file,ifPlot = True):
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
    h5file.create_dataset("Magnitude", data = np.asarray(Mag))
    h5file.create_dataset("HPP", data = np.asarray([u3dB,l3dB]))
     
    return

def plot_2D_Beamform_Spectrum(w,AM_mag,AM_phase,azm,elev,xSOI,ySOI,h5file,ifPlot = True):
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
    h5file.create_dataset("Magnitude", data = Mag)
    h5file.create_dataset("HPP", data = np.asarray([xu3dB,xl3dB,yu3dB,yl3dB]))
     
    return

#***********************
#   Simulation Parameters
#***********************
#Signal to Noise Ratio (dB)
SNR = 30

#fp = '../build/Test.h5'
fp = '../build/ULA.h5'
#fp = '../build/URA.h5'

#ySOI = 45
ySOI = 0
xSOI = 60
SOI = [ySOI*361 + xSOI]

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
#   Prepare Output
#**********************
fout = h5py.File("../build/output.h5","w")
gparam = fout.create_group("Parameters")
dazm = gparam.create_dataset("listAzm", data = np.asarray(azm))
delev = gparam.create_dataset("listElev", data = np.asarray(elev)) 
dfreq = gparam.create_dataset("listFreq", data = np.asarray(freq))
dSOI = gparam.create_dataset("SOI", data = np.asarray([xSOI,ySOI]))
dazm.dims[0].label = "Azimuth (degrees)"
delev.dims[0].label = "Elevation (degrees)"
dfreq.dims[0].label = "Frequency (MHz)"

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
Pds = DS.getSpectrum(Rxx,AM_mag,-1*AM_phase)
Pmvdr = MVDR.getSpectrum(Rxx,AM_mag,-1*AM_phase)
Pmusic = MUSIC.getSpectrum(Rxx,AM_mag,-1*AM_phase,len(SOI))
Proot = ROOT.getSpectrum(Rxx,len(SOI))

#Save to Output
gdf = fout.create_group("Direction Finding")
dds = gdf.create_dataset("Bartlett",data = np.asarray(20*np.log10(Pds)))
dmvdr = gdf.create_dataset("MVDR",data = np.asarray(20*np.log10(Pmvdr)))
dmusic = gdf.create_dataset("MUSIC", data = np.asarray(20*np.log10(Pmusic)))
droot = gdf.create_dataset("RootMUSIC", data = np.asarray(Proot))

#*****************
#   Beamforming
#*****************
wmvdr = mvdr.getWeights(Rxx,AM_mag[:,soiIdx],AM_phase[:,soiIdx])
wAF = AF.getWeights(len(AM_mag[:,0]),0.5,2*np.pi,SOI[0])

#Save to output
gbf = fout.create_group("Beamforming")
gmvdr = gbf.create_group("MVDR")
gmvdr.create_dataset("weights",data = np.asarray(wmvdr))
save_Beamform_Spectrum(wmvdr,AM_mag,AM_phase,azm,len(azm)*ySOI,SOI[0],gmvdr,False)

gAF = gbf.create_group("Array Factor")
gAF.create_dataset("weights",data = np.asarray(wAF))
save_Beamform_Spectrum(wAF,AM_mag,AM_phase,azm,len(azm)*ySOI,SOI[0],gAF,False)

#*******************
#   2D-Beamforming
#*******************
g2bf = fout.create_group("2D Beamforming")
gmvdr = g2bf.create_group("MVDR")
gmvdr.create_dataset("weights",data = np.asarray(wmvdr))
plot_2D_Beamform_Spectrum(wmvdr,AM_mag,AM_phase,azm,elev,xSOI,ySOI,gmvdr,False)

#Plot Spectrum
#plot_DF_Spectrum(Pds,azm)

print("Hello World")

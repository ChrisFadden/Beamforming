#*************************
#   Nec2hdf5.py
#
#   This reads a NEC output file that has used the PT
#card to print currents at the feed of antenna elements
#in an array, one PT card per element.  The currents are
#stored in an HDF5 file for easy use in MATLAB, Python or C
#
#   The transpose is not stored, since BLAS has methods for
#   the transpose.  Note that HDF5 will store it in Row-major
#   format, when it is read in by C 
#
#   TO DO:
#       Add Polarization
#       See if it can all be done in one pass?
#           splitting it up takes slightly more time
#           easier to follow though...
#*************************

import h5py 
import numpy as np
import re

f = open("Test.out","r") 

#Normalize so that at each frequency max is magnitude 1
Normalize = True

#***************************
#   Create HDF5 file
#***************************
f5 = h5py.File("../build/testnec.h5","w")

#*****************
#   Get Parameters
#*****************
#  Frequencies 
#  Azimuths
#  Elevations
#  Number of array elements
#
#  Does not currently
#  use polarization
#
#*****************
freq = set()
azm = set()
elev = set()
Elem = set()


ii = 1
for line in f:
    #*************************
    #   Find Frequency in MHz
    #*************************
    if("FREQUENCY" in line): 
        #Parse the number from NEC
        freq_i = re.findall('[\d.]+',f.readline())
        freq_i = round(float(freq_i[0]) * 10**(float(freq_i[1])),4)
        freq.add(freq_i) 
    
    if("THETA" in line):
        f.readline() #Skip line
        
        #Parse out useful data
        for data in f:
            if(not data.strip() or "DATA" in data):
                break
            dataArray = re.findall('[+-]?\d+(?:\.\d+)?',data) 
            elev.add(float(dataArray[0]))
            azm.add(float(dataArray[1]))
            Elem.add(int(dataArray[5]))

#Reset to top of file
f.seek(0)

freq = sorted(list(freq))
elev = sorted(list(elev))
azm = sorted(list(azm))
Elem = sorted(list(Elem))


#******************************
#   Create HDF5 File Structure
#
#   /Freq/Elev/Elem Mag[Azm]
#                   Phase[Azm]
#******************************
f5.create_group("Frequency (MHz)")
f5.create_dataset("listFreq", data = np.asarray(freq))
f5.create_dataset("listElev", data = np.asarray(elev))
f5.create_dataset("listAzm", data = np.asarray(azm))
f5.create_dataset("listElem", data = np.asarray(Elem))
for ff in freq:
    gFreq = f5.create_group(str(ff))
    gFreq.create_group("Elevation (degrees)")
    for th in elev:
        gElev = gFreq.create_group(str(th))

#**************************
#   Parse Mag/Phase data 
#**************************
mag = np.zeros((len(freq),len(elev),len(azm),len(Elem)))
phase = np.zeros((len(freq),len(elev),len(azm),len(Elem)))

freqIdx = 0
elemIdx = 0
for line in f:
    
    if(freqIdx >= len(freq)):
        freqIdx = 0
        elemIdx = elemIdx + 1

    #Parse nearly identital to before
    if("THETA" in line):
        f.readline()

        #Need to iterate over [Elev,Azm]
        ii = 0
        jj = 0
        for data in f:      
            #Find end of data
            if(not data.strip() or "DATA" in data):
                break
            #Regex out numbers 
            dataArray = re.findall('[+-]?\d+(?:\.\d+)?',data)
            
            #make mag[elev,azm] array
            mag[freqIdx,jj,ii,elemIdx] = float(dataArray[2]) * 10**(float(dataArray[3]))
            phase[freqIdx,jj,ii,elemIdx] = float(dataArray[4])
            if(jj < len(elev)-1):
                jj = jj + 1
            else:
                jj = 0 
                ii = ii + 1  
        
        freqIdx = freqIdx + 1

#*********************
#   Normalize max to 1
#   
#   normalize over freq
#   if user input
#*********************
mag = mag / np.max(mag)

normFactor = np.zeros((len(freq),len(elev)))

for ff in range(len(freq)):
    for th in range(len(elev)):
        tmp = mag[ff,th,:,:]
        normFactor[ff,th] = np.max(np.sum(tmp,axis=1))
        if(Normalize):
            mag[ff,th,:,:] = mag[ff,th,:,:] / normFactor[ff,th]

if(not Normalize):
    mag = mag / np.max(normFactor)

#***********************
#   Create Datasets for 
#   Mag/Phase in HDF5 file
#***********************
for ff in range(len(freq)):
    for th in range(len(elev)):
        gElev = f5[str(freq[ff])][str(elev[th])] 
        
        #Create Datasets
        magSet = gElev.create_dataset("Magnitude", data = mag[ff,th,:,:])
        phaseSet = gElev.create_dataset("Phase",data = phase[ff,th,:,:])
        
        #Label dimensions
        magSet.dims[0].label = "Azimuth"
        magSet.dims[1].label = "Element"
        phaseSet.dims[0].label = "Azimuth"
        phaseSet.dims[1].label = "Element"
f.close()



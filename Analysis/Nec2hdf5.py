import h5py 
import numpy as np
import re

f = open("Test.out","r") 

#***************************
#   Create HDF5 file
#***************************
f5 = h5py.File("testnec.h5","w")
gFreq = f5.create_group("Frequency")

while(True):

    #*************************
    #   Find Frequency in MHz
    #*************************
    for line in f:
        if("FREQUENCY" in line):
            #stop for looop 
            break 
    else:   
        #EOF stop while loop
        break   

    #Parse the number from NEC
    freq = re.findall('[\d.]+',f.readline())
    freq = round(float(freq[0]) * 10**(float(freq[1])),4)
       
    #create Group for the frequency found
    gPattern = gFreq.create_group(str(freq))
    
    #**************************
    #   Parse Radiation Pattern
    #**************************
    Elev = []
    Azm = []
    EthMag = []
    EthPhase = []
    EphiMag = []
    EphiPhase = []
    for line in f:
        if("RADIATION PATTERNS" in line):
            for x in range(4):  f.readline()
            break
    for line in f: 
        if(not line.strip()):
            break
        data = re.findall('[+-]?\d+(?:\.\d+)?',line)
    
        Elev.append(float(data[0])) 
        Azm.append(float(data[1]))
  
        EthMag.append(float(data[7]) * 10**(float(data[8])))
        EthPhase.append(float(data[9]))
    
        EphiMag.append(float(data[10]) * 10**(float(data[11])))
        EphiPhase.append(float(data[12]))
        
    #Place Radiation Patterns in a group in the HDF5 file 
    gPattern.create_dataset("Elevation",data = np.asarray(Elev))
    gPattern.create_dataset("Azimuth",data = np.asarray(Azm))
    gPattern.create_dataset("ElevMagnitude",data = np.asarray(EthMag))
    gPattern.create_dataset("ElevPhase",data = np.asarray(EthPhase))
    gPattern.create_dataset("AzmMagnitude",data = np.asarray(EphiMag))
    gPattern.create_dataset("AzmPhase",data = np.asarray(EphiPhase))

f.close()



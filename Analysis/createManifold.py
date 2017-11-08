#*************************
#   createManifold.py
#   
#   Create HDF5 files 
#   for the array manifold
#
#   TO DO:
#       PARSE the file names for nec2hdf5
#       ADD uniform circular arrays of various geometries
#
#   ADDITIONAL FEATURES:
#       ADD geometry of elements? i.e. elem1(x,y,z), elem2(x,y,z)?
#       in order to optimize locations of elements?
#*************************

import h5py 
import numpy as np
import re
#speed of light for MHz
cc = 299.792458

def createHDF5(fn,freq,elev,azm,mag,phase):
    f5 = h5py.File(fn,"w")
    f5.create_dataset("listFreq", data = np.asarray(freq))
    f5.create_dataset("listElev", data = np.asarray(elev))
    f5.create_dataset("listAzm", data = np.asarray(azm))
    
    magSet = f5.create_dataset("Magnitude", data = mag)
    phaseSet = f5.create_dataset("Phase", data = phase)

    #Label dimensions 
    magSet.dims[0].label = "Freq x Elev x Azimuth" 
    magSet.dims[1].label = "Element"
    
    phaseSet.dims[0].label = "Freq x Elev x Azimuth" 
    phaseSet.dims[1].label = "Element"

def nec2hdf5(fn):
    #f = open("Test.out","r") 
    f = open(fn,"r")    


    Normalize = True

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
                phase[freqIdx,jj,ii,elemIdx] = float(dataArray[4]) * np.pi / 180
                if(jj < len(elev)-1):
                    jj = jj + 1
                else:
                    jj = 0 
                    ii = ii + 1  
            
            freqIdx = freqIdx + 1

    f.close()
    mag = np.reshape(np.ravel(mag),(len(freq)*len(elev)*len(azm),len(Elem)))
    phase = np.reshape(np.ravel(phase),(len(freq)*len(elev)*len(azm),len(Elem)))
    
    if(Normalize):
        for ii in range(len(freq)*len(elev)*len(azm)):
            mag[ii,:] = mag[ii,:] / np.linalg.norm(mag[ii,:])

    fnh5 = fn[:-4]
    fnh5 = fnh5 + ".h5"
    createHDF5(fnh5,freq,elev,azm,mag,phase)
    
    print("Hello from Nec2hdf5")

#omni-directional uniform linear array
#M is number of elements
#d is spacing
#k is wavenumber (can be a vector for multiple frequencies)
def ULA(M,d,k):
    
    #Create ULA array manifold
    freq = np.zeros(len(k))
    elev = [90.0] 
    #Use same range as NEC files 
    azm = np.arange(361,dtype='float')
    
    mag = np.ones((len(k)*len(elev)*len(azm),M))
    phase = np.zeros((len(k)*len(elev)*len(azm),M))
    
    idx = 0
    for kk in range(len(k)):
       freq[kk] = (round(cc * k[kk] / (2*np.pi),1))
       for phi in range(len(azm)):
            for mm in range(M):
                #to agree with NEC sign convention 
                phase[idx,mm] = mm * k[kk] * d * np.sin(azm[phi] * np.pi / 180.)  
            idx = idx+1 
    
    createHDF5("../build/ULA.h5",freq,elev,azm,mag,phase)

    print("Hello from Uniform Linear Array")

#omni-directional rectangular array
def URA():
    M = 25
    row = 5
    col = M // row
    k = [2*np.pi]   
    d = 0.5
    elev = np.arange(91,dtype='float')
    azm = np.arange(361,dtype='float')
    freq = np.zeros(len(k))
    mag = np.ones((len(k)*len(elev)*len(azm),M))
    phase = np.zeros((len(k)*len(elev)*len(azm),M))

    idx = 0
    for kk in range(len(k)):
        freq[kk] = (round(cc*k[kk] / (2*np.pi),1))
        for th in range(len(elev)):
            for phi in range(len(azm)):
                for rr in range(row):
                    for cl in range(col):
                        rowP = rr*k[kk]*d*np.sin(azm[phi] * np.pi / 180.) 
                        colP = cl*k[kk]*d*np.sin(elev[th] * np.pi / 180.) 
                        phase[idx,rr*row + cl] = rowP + colP
                idx = idx + 1
    
    createHDF5("../build/URA.h5",freq,elev,azm,mag,phase)
    print("Hello from Uniform Rectangular Array")
#omni-directional uniform circular array
def UCA():
      
    print("Hello from Uniform Circular Array")
    return

if __name__ == '__main__':
    ULA(5,0.5,[2*np.pi])
    #UCA()
    URA() 
    nec2hdf5("../build/Test.out") 
    print("Hello World")



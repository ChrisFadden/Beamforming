#*************************
#   analyticArray2hdf5.py
#   
#   Create HDF5 files for
#   analytic definitions
#   for the array manifold
#*************************

import h5py 
import numpy as np

#speed of light for MHz
cc = 299.792458

#omni-directional uniform linear array
#M is number of elements
#d is spacing
#k is wavenumber (can be a vector for multiple frequencies)
def ULA(M,d,k):
    
    #Create ULA array manifold
    ff = [] 
    A = np.zeros((len(k),181,M),dtype='complex')
    ki = 0
    for kk in k:
       ff.append(round(cc * kk / (2*np.pi),1))
       for mm in range(M):
            for azm in range(181):
                A[ki,azm,mm] = np.exp(-1j * mm * kk * d * np.sin(azm))  
       ki = ki + 1
    
    elev = [90.0]
    azm = range(181)
    
    #*********************
    #   Create HDF5 file
    #*********************
    f5 = h5py.File("../build/ULA.hdf5","w")
    f5.create_group("Frequency (MHz)")
    f5.create_dataset("listFreq", data = np.asarray(ff))
    f5.create_dataset("listElev", data = np.asarray(elev))
    f5.create_dataset("listAzm", data = np.asarray(azm))
    
    for fii in ff:
        gFreq = f5.create_group(str(fii))
        gFreq.create_group("Elevation (degrees)")
        for th in elev:
            gElev = gFreq.create_group(str(th))

    for fi in range(len(ff)):
            gElev = f5[str(ff[fi])][str(elev[0])]
            magSet = gElev.create_dataset("Magnitude", data = (np.abs(A[fi,:,:])))
            phaseSet = gElev.create_dataset("Phase", data = (np.angle(A[fi,:,:])))
            hermSet = gElev.create_dataset("Hermitian", data = -1 *(np.angle(A[fi,:,:])))

            #Label Dimensions
            magSet.dims[0].label = "Azimuth"
            magSet.dims[1].label = "Element"
            phaseSet.dims[0].label = "Azimuth"
            phaseSet.dims[1].label = "Element"
            hermSet.dims[0].label = "Azimuth"
            hermSet.dims[1].label = "Element"

    print("Hello from Uniform Linear Array")

#omni-directional uniform circular array
def UCA():
    print("Hello from Uniform Circular Array")
    return

if __name__ == '__main__':
    ULA(5,0.5,[2*np.pi])
    UCA()
    print("Hello World")



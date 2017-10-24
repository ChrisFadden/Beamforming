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
    for kk in k:
       ff = round(cc * kk / (2*np.pi),1)
       A = np.zeros((M,181),dtype='complex')
       for mm in range(M):
            for azm in range(181):
                A[mm,azm] = np.exp(-1j * mm * kk * d * np.sin(azm))  
    print("Hello from Uniform Linear Array")

#omni-directional uniform circular array
def UCA():
    print("Hello from Uniform Circular Array")
    return

if __name__ == '__main__':
    ULA(5,0.5,[2*np.pi])
    UCA()
    print("Hello World")



import scipy.linalg
import numpy as np

def hello():
    print("Hello from MUSIC DF module")

def getSpectrum(Rxx,AM_mag,AM_herm,n):
    
    ##  INPUTS:
    #       Rxx:    Covariance Matrix           (dim: NumAnt x NumAnt)
    #       AM_mag:  Array manifold magnitude    (dim: NumAnt x Azm)
    #       AM_herm: Array manifold phase        (dim: NumAnt x Azm)
    #       n:       The number of SOI
    #   
    ##  OUTPUTS:
    #       P:  The power spectrum with peaks at the SOI    (dim: Azm x 1)


    aH = (AM_mag * np.exp(1j * AM_herm)).transpose()
    
    w,v = np.linalg.eigh(Rxx)

    idx = np.argsort(w)

    v = v[:,idx]
    
    vn = v[:,0:len(v)-1-n]

    P = abs(np.dot(aH,vn))**2
    P = np.dot(P,np.ones(len(v)-1-n))

    return np.min(P) / P
    

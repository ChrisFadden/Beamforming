import scipy.linalg
import numpy as np

def hello():
    print("Hello from Bartlett DF module")

def getSpectrum(Rxx,AM_mag,AM_herm):
    ##  INPUTS:
    #       Rxx:    Covariance Matrix           (dim: NumAnt x NumAnt)
    #       AM_mag:  Array manifold magnitude    (dim: NumAnt x Azm)
    #       AM_herm: Array manifold phase        (dim: NumAnt x Azm)
    #
    ##  OUTPUTS:
    #       P:   The power spectrum with peaks at the SOI    (dim: Azm x 1)

    Rxx += 10**-9 * np.eye(Rxx.shape[0])

    aH = (AM_mag * np.exp(1j * AM_herm)).transpose()
    
    L = np.linalg.cholesky(Rxx)

    P = abs(np.dot(aH,L))**2 
    P = np.dot(P,np.ones(Rxx.shape[0]))
    
    return P / np.max(P)
    

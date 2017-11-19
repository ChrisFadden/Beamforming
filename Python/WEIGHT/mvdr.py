import scipy.linalg
import numpy as np

def hello():
    print("Hello from MVDR Beamform Weighting module")

def getWeights(Rxx,AM_mag,AM_phase):
    ##  INPUTS:
    #       Rxx:    Covariance Matrix           (dim: NumAnt x NumAnt)
    #       AM_mag:  Array manifold magnitude    (dim: NumAnt x Azm)
    #       AM_herm: Array manifold phase        (dim: NumAnt x Azm)
    #
    ##  OUTPUTS:
    #       P:   The power spectrum with peaks at the SOI    (dim: Azm x 1)

    aH = (AM_mag * np.exp(-1j * AM_phase)).transpose()
    a = (AM_mag * np.exp(1j * AM_phase)) 
    
    RxxA = np.linalg.solve(Rxx,a)
    
    return RxxA / np.dot(aH,RxxA)

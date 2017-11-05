import scipy.linalg
import numpy as np

def hello():
    print("Hello from MVDR Beamform Weighting module")

def getWeights(Rxx,AM_mag,AM_phase):
    
    aH = (AM_mag * np.exp(-1j * AM_phase)).transpose()
    a = (AM_mag * np.exp(1j * AM_phase)) 
    
    RxxA = np.linalg.solve(Rxx,a)
    
    return RxxA / np.dot(aH,RxxA)

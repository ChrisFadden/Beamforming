import scipy.linalg
import numpy as np

def hello():
    print("Hello from MVDR DF module")

def getSpectrum(Rxx,AM_mag,AM_phase,AM_herm):
    
    Rxx += 10**(-12) * np.eye(Rxx.shape[0]) 
    
    aH = (AM_mag * exp(1j * AM_herm)).transpose()
    a = (AM_mag * exp(1j * AM_phase))
    
    return P / np.max(P)
    

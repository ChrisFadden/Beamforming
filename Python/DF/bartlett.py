import scipy.linalg
import numpy as np

def hello():
    print("Hello from Bartlett DF module")

def getSpectrum(Rxx,AM_mag,AM_herm):
     
    PL,U = scipy.linalg.lu(Rxx,permute_l = True) 
    
    aH = (AM_mag * np.exp(1j * AM_herm)).transpose()

    P = abs(np.dot(aH,PL))**2 
    P = np.dot(P,np.ones(Rxx.shape[0]))
    
    return P / np.max(P)
    

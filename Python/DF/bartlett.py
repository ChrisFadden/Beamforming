import scipy.linalg
import numpy as np

def hello():
    print("Hello from Bartlett DF module")

def getSpectrum(Rxx,AM_mag,AM_herm):
       
    Rxx += 10**-9 * np.eye(Rxx.shape[0])

    aH = (AM_mag * np.exp(1j * AM_herm)).transpose()
    
    L = np.linalg.cholesky(Rxx)

    P = abs(np.dot(aH,L))**2 
    P = np.dot(P,np.ones(Rxx.shape[0]))
    
    return P / np.max(P)
    

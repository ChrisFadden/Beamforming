import scipy.linalg
import numpy as np

def hello():
    print("Hello from MVDR DF module")

def getSpectrum(Rxx,AM_mag,AM_herm):
       
    aH = (AM_mag * np.exp(1j * AM_herm)).transpose()
    
    #The LAPACK routine for this is sytrf
    Rxx += 10**-9 * np.eye(Rxx.shape[0]) 
    
    L = np.linalg.cholesky(np.linalg.inv(Rxx))

    P = abs(np.dot(aH,L))**2
    P = np.dot(P,np.ones(Rxx.shape[0]))
    
    return np.min(P) / P


import scipy.linalg
import numpy as np

def hello():
    print("Hello from MVDR DF module")

def getSpectrum(Rxx,AM_mag,AM_herm):
    
    Rxx += 10**(-12) * np.eye(Rxx.shape[0]) 
    
    aH = (AM_mag * np.exp(1j * AM_herm)).transpose()
    
    RxxI = np.linalg.inv(Rxx)
    
    print("LU is not as good as LDLT... can use eig since its symmetric...")
    PL, U = scipy.linalg.lu(RxxI,permute_l=True)

    P = abs(np.dot(aH,PL))**2
    P = np.dot(P,np.ones(RxxI.shape[0]))
    
    return np.min(P) / P
    

import scipy.linalg
import numpy as np

def hello():
    print("Hello from MUSIC DF module")

def getSpectrum(Rxx,AM_mag,AM_herm,n):
    
    aH = (AM_mag * np.exp(1j * AM_herm)).transpose()
    
    w,v = np.linalg.eig(Rxx)

    idx = np.argsort(w)

    v = v[:,idx]
    
    vn = v[:,0:len(v)-1-n]

    P = abs(np.dot(aH,vn))**2
    P = np.dot(P,np.ones(len(v)-1-n))

    return np.min(P) / P
    

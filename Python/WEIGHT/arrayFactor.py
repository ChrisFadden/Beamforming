import scipy.linalg
import numpy as np

def hello():
    print("Hello from Array Factor ULA Beamform Weighting module")

def getWeights(M,d,k,SOI):
    
    wphase = []     
    for mm in range(M):
        wphase.append(1j*mm * k * d * np.sin(SOI * np.pi / 180.)) 
    return np.exp(np.asarray(wphase))

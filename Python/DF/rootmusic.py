import scipy.linalg
import numpy as np

def hello():
    print("Hello from Root MUSIC DF module")

def getSpectrum(Rxx,n):
       
    w,v = np.linalg.eigh(Rxx)

    idx = np.argsort(w)

    v = v[:,idx]
    
    vn = v[:,0:len(v)-1-n]
    
    P = np.dot(vn,(vn.conj()).transpose())
    
    #Extract Polynomial 
    M = Rxx.shape[0] 

    D = 0j*np.zeros(2*M+1)
    for (idx,val) in enumerate(range(M-1,-M,-1)):
        D[idx] = np.sum(np.diag(P,val))
    
    z = np.roots(D) 
    
    #Keep roots with mag < 1, and non-zero imag part
    z = np.extract(np.abs(z) < 1,z)
    z = np.extract(np.imag(z) != 0,z) 
    
    allAzm = np.angle(z)
        
    #Get roots closest to the unit circle
    d2c = np.abs(np.abs(z) - 1)
    idx = np.argsort(d2c) 
    azm = np.angle(z[idx[:n]])
    
    #normalize azimuths
    k = 2*np.pi
    d = 0.5
    
    #No Negative to keep with NEC convention
    azm = (np.arcsin(azm / (k*d))) * 180 / np.pi
    
    allAzm = (np.arcsin(-allAzm / (k*d))) * 180 / np.pi
    
    return azm
    

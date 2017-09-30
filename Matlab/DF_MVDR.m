function [ P ] = DF_MVDR(x, AM)
%%  Description:
 %      MVDR Beamformer
 %      Implements P(azm) = 1 / (a^H Rxx^-1 a)
 %  
 %      This implements the minimum variance 
 %      distortionless response direction finding
 %      algorithm.

%%  Inputs:
 %      x is the input signal
 %     AM is the array manifold

%%  Outputs:
 %      P returns the power at each angle

%%  Computation:
    Rxx = x * x' + 10^(-12) * eye(length(x));
    
    aH = (AM.mag .* exp(1j * AM.herm)).';
    a = (AM.mag .* exp(1j * AM.phase));
    
    P = abs(diag(aH * inv(Rxx) * a));
    P = max(P) ./ P;
end
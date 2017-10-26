function [ P ] = DF_MVDR(Rxx, AM_mag, AM_phase)
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
    
    Rxx = Rxx + 10^(-12) * eye(size(Rxx,1));
    
    aH = (AM_mag .* exp(1j * AM_phase))';
    
    RxxI = inv(Rxx);
    [L,D] = ldl(RxxI);
		%NOTE the sqrt for LDLT factorization
    P = abs(aH * L * sqrt(D)).^2 * ones(size(Rxx,1),1);
    P = min(P) ./ P;
end

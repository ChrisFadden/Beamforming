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
    
    RxxI = inv(Rxx);
    [L,D] = ldl(RxxI);
		%NOTE the sqrt for LDLT factorization
    P = abs(aH * L * sqrt(D)).^2 * ones(length(x),1);
    P = min(P) ./ P;
end

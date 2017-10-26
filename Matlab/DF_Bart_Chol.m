function [ P ] = DF_Bart_Chol(Rxx, AM_mag,AM_phase)
%%  Description:
 %      Bartlett Beamformer
 %      Implements P(azm) = a^H L D L^T a
 %      using the Cholesky Decomposition
 
%%  Inputs:
 %      x is the input signal
 %     AM is the array manifold

%%  Outputs:
 %      P returns the power at each angle

%%  Computation:
    aH = (AM_mag .* exp(1j * AM_phase))';
    
    [L,D] = ldl(Rxx);
		%NOTE the sqrt for LDLT factorization
    P = abs(aH * L * sqrt(D)).^2 * ones(size(Rxx,1),1);
    P = P ./ max(P);
end

function [ P ] = DF_Bart_Chol(x, AM)
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
    Rxx = x * x';
    aH = (AM.mag .* exp(1j * AM.herm)).';
    
    [L,D] = ldl(Rxx);
		%NOTE the sqrt for LDLT factorization
    P = abs(aH * L * sqrt(D)).^2 * ones(length(x),1);
    P = P ./ max(P);
end

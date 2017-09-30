function [ P ] = DF_Bart(x, AM)
%%  Description:
 %      Bartlett Beamformer
 %      Implements P(azm) = a^H Rxx a

%%  Inputs:
 %      x is the input signal
 %     AM is the array manifold

%%  Outputs:
 %      P returns the power at each angle

%%  Computation:
    Rxx = x * x';
    aH = (AM.mag .* exp(1j * AM.herm)).';
    a = (AM.mag .* exp(1j * AM.phase));
    
    %Should be able to use projection matrices
    %to get the diagonal elements...
    P = diag(aH * Rxx * a);  
    P = P ./ max(P);
end
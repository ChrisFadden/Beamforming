function [ P ] = DF_Bart(Rxx, AM_mag, AM_phase)
%%  Description:
 %      Bartlett Beamformer
 %      Implements P(azm) = a^H Rxx a

%%  Inputs:
 %      Rxx is the input covariance matrix
 %     AM is the array manifold

%%  Outputs:
 %      P returns the power at each angle

%%  Computation:
    aH = (AM_mag .* exp(1j * AM_phase))';
    a = (AM_mag .* exp(1j * AM_phase));
    
    %Should be able to use projection matrices
    %to get the diagonal elements...
    P = diag(aH * Rxx * a);  
    P = P ./ max(P);
end
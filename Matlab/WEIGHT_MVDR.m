function [ w ] = WEIGHT_MVDR(Rxx, AM_mag, AM_phase)
%%  Description:


%%  Inputs:


%%  Outputs:


%%  Computation:
    R_inv = inv(Rxx);
    
    a = AM_mag .* exp(1j * AM_phase);
    
    w = R_inv * a / (a' * R_inv * a);
    
    fprintf('I am wrong and I dont know why\n');

end

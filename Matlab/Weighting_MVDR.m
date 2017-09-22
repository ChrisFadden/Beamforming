function [ w ] = Weighting_MVDR( AM, SOI)
%%  Assumptions:
    
%%  Inputs:
    %AM     =   Array Manifold
    %SOI    =   Signal of Interest ( -180 < SOI < 180 )
    %SNR    =   Signal to Noise Ratio (dB)
%%  Calculation:  
R_inv = eye(size(AM,1)); 

%MVDR Beamformer
w = R_inv * AM(:,SOI) / (AM(:,SOI)' * R_inv * AM(:,SOI));

%%  Output:
    % w     = M x 1 vector of complex weights
    % SNR only affects ability to null interferers
end


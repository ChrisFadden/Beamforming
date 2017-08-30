function [ w ] = Weighting_MVDR( AM, SOI, interAzm, SNR)
%%  Assumptions:
    
%%  Inputs:
    %AM     =   Array Manifold
    %SOI    =   Signal of Interest ( -180 < SOI < 180 )
    %SNR    =   Signal to Noise Ratio (dB)
%%  Calculation:  
sigma = 10^(-SNR / 20);

%When there is an interferer
if(abs(interAzm) <= 180)
    R = sigma * eye(size(AM,1));
    R = R + AM(:,interAzm)*AM(:,interAzm)';
    R_inv = inv(R);
else %no interferer
   R_inv = eye(size(AM,1)); 
end



%MVDR Beamformer
w = R_inv * AM(:,SOI) / (AM(:,SOI)' * R_inv * AM(:,SOI));

%%  Output:
    % w     = M x 1 vector of complex weights
    % SNR only affects ability to null interferers
end


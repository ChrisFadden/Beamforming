function [ w ] = Weighting_MVDR( AM, SOI, interAzm, SNR)
%%  Assumptions:
    
%%  Inputs:
    %AM     =   Array Manifold
    %SOI    =   Signal of Interest ( -180 < SOI < 180 )
    %SNR    =   Signal to Noise Ratio (dB)
%%  Calculation:  
sigma = 10^(-SNR / 20);

%When there is an interferer
R_inv = sigma * eye(size(AM,1));
R_inv = R_inv + AM(:,interAzm)*AM(:,interAzm)';
R_inv2 = inv(R_inv);

if(abs(interAzm) <= 180)
R_inv = eye(size(AM,1)) - ...
    (AM(:,interAzm)*AM(:,interAzm)') ./ (sigma + (AM(:,interAzm)'*AM(:,interAzm)));

else %no interferer
   R_inv = eye(size(AM,1)); 
end



%MVDR Beamformer
w = R_inv * AM(:,SOI) / (AM(:,SOI)' * R_inv * AM(:,SOI));
w2 = R_inv2 * AM(:,SOI) / (AM(:,SOI)' * R_inv2 * AM(:,SOI));

norm(w - w2)

%%  Output:
    % w     = M x 1 vector of complex weights
    % SNR only affects ability to null interferers
end


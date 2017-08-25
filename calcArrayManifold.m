function [ am ] = calcArrayManifold(r,az)
%%  Assumptions
%Assumes Linear Array

%%  Inputs:
%r   =  spacing of antenna elements (vector) half-wavelengths
%az  =  desired antenna pattern azimuths (vector)

%%  Calculation:
    am = zeros(length(r),length(az));
    for phi = 1:length(az)
        for elem = 1:length(r)
            am(elem, phi) = exp(-1j*r(elem)*pi*(cosd(az(phi))));
        end 
    end

%%  Outputs: 
%   am(element, azimuth)

end


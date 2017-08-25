%MVDR Algorithm Main
clear;
clc;

%Azimuths
AzmMax = 180;
AzmMin = 0;
numAzm = AzmMax - AzmMin;
az = linspace(AzmMin,AzmMax,numAzm);

%Desired Steering
SteerAzm = 45;

%Num elements
M = 7;

%Antenna Spacing (units of half-wavelength) 
 d = 1;
% for mm = 1:M
%    r(mm) = (mm-1)*d; 
% end
if(mod(M,2) == 0)
    error('Number of array elements must be odd')
else
    r(ceil(M/2)) = 0;
    for mm = 1:floor(M/2)
        r(ceil(M/2) + mm) = mm*d;
        r(ceil(M/2) - mm) = -mm*d;
    end
end

%Array Manifold
AM = calcArrayManifold(r,az);

%Weighting Algorithm
w = ones(M,1);
%w = Weighting_ULA_Phased(M,SteerAzm);
w = Weighting_Chebyshev(r,SteerAzm,30);

%Plotting
for phi = 1:length(az)
   y(phi) = (w' * AM(:,phi)) / M; 
end

%subplot(2,1,1)
plot(az,20*log10(abs(y)))
title('Array Response')
xlabel('Angle of Arrival (\circ)')
ylabel('Magnitude (dB)')
ylim([-60,2])
% subplot(2,1,2)
% plot(az,angle(y)*180/pi)
% ylim([-182,182])
% xlabel('Angle of Arrival (\circ)')
% ylabel('Phase (\circ)')






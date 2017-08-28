%MVDR Algorithm Main
clear;
clc;

%%  Parameters

%Azimuths
AzmMax = 180;
AzmMin = 0;
numAzm = AzmMax - AzmMin;
az = linspace(AzmMin,AzmMax,numAzm);

%Desired Steering
SOI = 70 - 1;

%Interference Pattern
interAzm = 30 - 1;

%Signal to Noise Ratio of the Array (dB)
SNR = 30;

%Num elements
M = 10;

%%  Antenna Spacing (units of half-wavelength) 
d = 1;

r = zeros(M,1);
if(mod(M,2) == 0)
    for mm = 0:M/2-1
       r(M/2 + mm) = mm*d;
       r(M/2 - mm) = -mm*d;
    end
else
    r(ceil(M/2)) = 0;
    for mm = 1:floor(M/2)
        r(ceil(M/2) + mm) = mm*d;
        r(ceil(M/2) - mm) = -mm*d;
    end
end

%%  Array Manifold
AM = calcArrayManifold(r,az);

%%  Weighting Algorithm
w = ones(M,1);
%w = Weighting_ULA_Phased(M,d,SOI) / M;
w = Weighting_MVDR(AM,SOI,interAzm,SNR);

%%  Plotting
for phi = 1:length(az)
   y(phi) = (w' * AM(:,phi)); 
end

ymin = -60;
ymax = 2;
xmin = AzmMin - 2;
xmax = AzmMax + 2;
plot(az,20*log10(abs(y)))
title('Array Response')
xlabel('Angle of Arrival (\circ)')
ylabel('Magnitude (dB)')
ylim([ymin,ymax])
xlim([AzmMin,AzmMax])
hold on

x0 = SOI; %% Plot vertical lines at SOI and interferer location
grid_y = ymax:-1:ymin;
grid_x = x0+0*(grid_y);
plot(grid_x,grid_y,'linewidth',1.5)
hold on
x0 = interAzm;
if(abs(x0) > 180)
   x0 = 0; 
end
grid_x = x0+0*grid_y;
plot(grid_x,grid_y,'--r','linewidth',1.5)
legend('Array Pattern','Signal of Interest','Interferer')








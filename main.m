%MVDR Algorithm Main
clear;
clc;

%%  Parameters

%Azimuths
AzmMax = 180;
AzmMin = 0;
numAzm = AzmMax - AzmMin + 1;
az = linspace(AzmMin,AzmMax,numAzm);

%Desired Steering
SOI = 90 + 1;

%Interference Pattern
interAzm = 85 + 1;

%Signal to Noise Ratio of the Array (dB)
SNR = 60;

%Desired Side Lobe Level
SLL = 30;

%Num elements
M = 0;
M = 100;

%%  Antenna Spacing (units of half-wavelength) 
r = zeros(M,1);
d = 1;

r = Position_ULA_PhaseCentered(M,d);
%r = Position_ULA_PhaseProgression(M,d);

%%  Array Manifold
AM = calcArrayManifold(r,az);

%%  Weighting Algorithm
w = ones(M,1);
w = Weighting_ULA_Phased(M,d,az(SOI));
w = Weighting_Chebyshev(M,SLL);
%w = Weighting_MVDR(AM,SOI);


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
max(abs(y))

x0 = SOI-1; %% Plot vertical lines at SOI and interferer location
grid_y = ymax:-1:ymin;
grid_x = x0+0*(grid_y);
plot(grid_x,grid_y,'linewidth',1.5)
hold on
x0 = interAzm;
if(abs(x0) > 180)
   x0 = SOI; 
end
grid_x = x0+0*grid_y;
plot(grid_x,grid_y,'--r','linewidth',1.5)
legend('Array Pattern','Signal of Interest','Interferer')

%%  Analytic reference
% figure()
% for phi = 1:length(az)
%     psi = pi*r(2)*cosd(az(phi));
%     yA(phi) = sin(M * psi / 2) / (M * sin(psi/2));
% end
% yA(91) = 1;
% plot(az,20*log10(abs(yA)))
% ylim([-60,2])





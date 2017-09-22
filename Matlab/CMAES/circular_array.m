clc; clear all; close all;

N = 5;                  % Number of elements
freq = 2e6:1e6:30e6;    % frequency range (Hz)
a = 15;                % radius of array (m)
if mod(N,1) == 0
    phi_n = 2*pi*[1:N]/N;
else
    disp('Error: Number of elements must be integer!')
end

In = ones(size(freq));   % Element (complex) currents

% EM constants
e0 = 8.85e-12;
m0 = 4*pi*1e-7;
c0 = 1/sqrt(m0*e0);

beta = 2*pi*freq/c0;

% Far field parameters
phi = linspace(-pi,pi,360);
theta = linspace(0,pi/2,90);

[PP, TT] = meshgrid(phi,theta);

Efar = zeros(length(freq),size(PP,1),size(PP,2));
Etemp = zeros(size(PP));
for ff = 1:length(freq)
    for nn = 1:N
        Etemp = Etemp + In(nn)*exp(1i*a*beta(ff)*cos(PP-phi_n(nn)).*sin(TT));
    end
    Efar(ff,:,:) = Etemp/max(max(Etemp));         % normalize pattern
end

f_ind = 9;


imagesc(phi,theta,20*log10(abs(squeeze(Efar(f_ind,:,:)))))
colorbar
tname = sprintf('Circular Array Factor: N = %i, a = %d m',N,a);
title(tname,'fontname','times','fontsize',20)
% xlabel('\phi (deg)','fontname','times','fontsize',18)
% ylabel('\theta (deg)','fontname','times','fontsize',18)
xlabel('Azimuth (deg)','fontname','times','fontsize',18)
ylabel('Elevation (deg)','fontname','times','fontsize',18)
grid on
set(gca,'linewidth',1.5,'fontname','times','fontsize',16)
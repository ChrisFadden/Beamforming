clc; clear all; close all;

load variablescmaes.mat
params = varargin;
In = bestever.x(1:2:end) + 1i*bestever.x(2:2:end);
% Array Configuration
N = params{1}{1};           % number of elements in array
phi_n = params{1}{2};       % angular location of elements
a = params{1}{3};                 % radius of circular array (meters)
freq = params{1}{4};            % Frequencies (Hz)

% EM constants
e0 = 8.85e-12;
m0 = 4*pi*1e-7;
c0 = 1/sqrt(m0*e0);

beta = 2*pi*freq/c0;

% Far field parameters
phi = params{1}{5};
theta = params{1}{6};

[PP, TT] = meshgrid(phi,theta);

Efar = zeros(length(freq),size(PP,1),size(PP,2));
for ff = 1:length(freq)
    Etemp = zeros(size(PP));
    for nn = 1:N
        Etemp = Etemp + In(nn)*exp(1i*a*beta(ff)*cos(PP-phi_n(nn)).*sin(TT));
    end
    Efar(ff,:,:) = Etemp/max(max(Etemp));         % normalize pattern
end

Efar = 20*log10(abs(Efar));

% Goals
% Max Target
ind_max_phi = params{1}{7};
ind_max_theta = params{1}{8};
% Null Target
ind_null_phi = params{1}{9};
ind_null_theta = params{1}{10};

for ff = 1:length(freq)
    figure(ff)
    imagesc(phi*180/pi,theta*180/pi,squeeze(Efar(ff,:,:)))
    hold on
    plot(phi(ind_max_phi)*180/pi,theta(ind_max_theta)*180/pi,'bx',...
        phi(ind_null_phi(1))*180/pi,theta(ind_null_theta(1))*180/pi,'rx',...
        phi(ind_null_phi(2))*180/pi,theta(ind_null_theta(2))*180/pi,'rx',...
        'markersize',25,'linewidth',4)
    hold off
    cb = colorbar;
    caxis([-40 0])
    tname = sprintf('Circular Array Factor: N = %i, a = %d m',N,a);
    title(tname,'fontname','times','fontsize',20)
    % xlabel('\phi (deg)','fontname','times','fontsize',18)
    % ylabel('\theta (deg)','fontname','times','fontsize',18)
    xlabel('Azimuth (deg)','fontname','times','fontsize',18)
    ylabel('Elevation (deg)','fontname','times','fontsize',18)
    ylabel(cb,'dB','fontname','times','fontsize',18)
    grid on
    set(gca,'linewidth',1.5,'fontname','times','fontsize',16)
end
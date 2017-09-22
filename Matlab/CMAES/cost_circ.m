function cost_circ = cost_circ(xvar, evalOps)

In = xvar(1:2:end) + 1i*xvar(2:2:end);  % Element currents

N = evalOps{1};                  % Number of elements
phi_n = evalOps{2};             % angular location of elements
a = evalOps{3};                % radius of array (m)
freq = evalOps{4};     % frequency range (Hz)

% EM constants
e0 = 8.85e-12;
m0 = 4*pi*1e-7;
c0 = 1/sqrt(m0*e0);
beta = 2*pi*freq/c0;    % wavenumbers

% Far field grid construction
phi = evalOps{5};
theta = evalOps{6};
[PP, TT] = meshgrid(phi,theta); 
Efar = zeros(length(freq),size(PP,1),size(PP,2));
for ff = 1:length(freq)
    Etemp = zeros(size(PP));
    for nn = 1:N
        Etemp = Etemp + In(nn)*exp(1i*a*beta(ff)*cos(PP-phi_n(nn)).*sin(TT));
    end
    Efar(ff,:,:) = Etemp/max(max(Etemp));         % normalize pattern
end

Efar = 20*log10(abs(Efar));         % convert pattern to dB

% Goals
% Max Target
ind_max_phi = evalOps{7};
ind_max_theta = evalOps{8};
% Null Target
ind_null_phi = evalOps{9};
ind_null_theta = evalOps{10};

cost_circ = sum(-Efar(:,ind_max_theta,ind_max_phi) + max([Efar(:,ind_null_theta(1),ind_null_phi(1)), ...
                                                          Efar(:,ind_null_theta(2),ind_null_phi(2)), ...
                                                          -40*ones(length(freq),1)],[],2));


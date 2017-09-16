clc; clear all; close all;

freq = [2:2:10]*1e6;      % Frequencies (Hz) (can be single or multiple)

% Array Configuration
numElems = 5;           % number of elements in array
if mod(numElems,1) == 0
    phi_n = 2*pi*[1:numElems]/numElems;
else
    disp('Error: Number of elements must be integer!')
end
a = 75;                 % radius of circular array (meters)

% Goals
max_phi = 0;       % Max radiation angle
max_theta = 45;
null_phi = [120 -45];     % Null Angle(s)
null_theta = [15 85];

% Far Field Resolution (the less resolved, the faster the simulations are)
phi = linspace(-pi,pi,72);
theta = linspace(0,pi/2,18);

% Farfield Target Indexes
% Max Targe
[val_max_phi, ind_max_phi] = min(abs(phi*180/pi - max_phi));
[val_max_theta, ind_max_theta] = min(abs(theta*180/pi - max_theta));
% Null Target(s)
for ii  = 1:length(null_phi)
    [val_null_phi(1), ind_null_phi(1)] = min(abs(phi*180/pi - null_phi(1)));
    [val_null_theta(1), ind_null_theta(1)] = min(abs(theta*180/pi - null_theta(1)));
    [val_null_phi(2), ind_null_phi(2)] = min(abs(phi*180/pi - null_phi(2)));
    [val_null_theta(2), ind_null_theta(2)] = min(abs(theta*180/pi - null_theta(2)));
end

% Evaluation Parameters
evalOps{1} = numElems;
evalOps{2} = phi_n;
evalOps{3} = a;
evalOps{4} = freq;
evalOps{5} = phi;
evalOps{6} = theta;
evalOps{7} = ind_max_phi;
evalOps{8} = ind_max_theta;
evalOps{9} = ind_null_phi;
evalOps{10} = ind_null_theta;

evalFN = 'cost_circ';

seedPop = rand(numElems*2);     % Random seed, 2 vars per element for real and imaginary

insigma = 0.5; % initial coordinate wise standard deviation(s)
opts=cmaes;   % This creates a CMAES structure with default options
opts.StopFitness = -40*length(freq);
opts.TolFun = 1e-4;
opts.Restarts     = 5;
opts.IncPopSize   = 2;
opts.EvalInitialX = 'no';
opts.LBounds = 0;
opts.UBounds = 1;
opts.DispModulo = 5;
opts.DispFinal= 0;
[x, fmin] = cmaes( ...
    evalFN, ...    % name of objective/fitness function
    seedPop, ...    % objective variables initial point, determines N
    insigma, ...   % initial coordinate wise standard deviation(s)
    opts, ...
    evalOps);      % addition args for fitness function
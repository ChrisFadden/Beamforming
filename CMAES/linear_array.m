% function pattern = [N, freq, d, In]

clc; clear all; close all;

N = 10;                  % Number of elements
freq = 2e6:1e6:30e6;    % frequency range (Hz)
d = 15;                % distance between elements (m)
if mod(N,1) == 0
    ds = [0:d:(N-1)*d] - d*(N-1)/2;
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
phi = linspace(-pi,pi,500);

Efar = zeros(length(freq),length(phi));
for ff = 1:length(freq)
    for nn = 1:N
        Efar(ff,:) = Efar(ff,:) + In(nn)*exp(1i*ds(nn)*beta(ff)*cos(phi));
    end
    Efar(ff,:) = Efar(ff,:)/max(Efar(ff,:));         % normalize pattern
end

find = 9;


plot(phi,20*log10(abs(Efar(find,:))))
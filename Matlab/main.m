clear;
clc;
%%
%*****************
%   User Inputs
%       hdf5 input file
%       Frequency, Elevation
%       Signals of Interest
%       Signal to Noise Ratio
%*****************
%H5 file
fp = '../build/testnec.h5';
dp = '/289.8/90.0/';

%Signal of Interest
SOI = [34];

%Signal to Noise ratio (dB)
SNR = 30;

%%
%*********************
%   Read in HDF5 File
%       read in array manifold
%       create noisy input signal
%*********************

%Get Azimuths
azm = h5read(fp,'/listAzm');

%Get Array Manifold
AM.mag = h5read(fp,strcat(dp,'Magnitude'));
AM.phase = h5read(fp,strcat(dp,'Phase'));
AM.herm = h5read(fp,strcat(dp,'Hermitian'));

%Get incoming signal, add noise
x = AM.mag(:,SOI) .* exp(1j * AM.phase(:,SOI));
x = awgn(x,SNR,'measured');

%%  Computation:
    P = abs(DF_Bart(x,AM));
    P2 = DF_Bart_Chol(x,AM);
    Bart_Check = norm(P - P2);

    Pm = DF_MUSIC(x,AM,length(SOI));
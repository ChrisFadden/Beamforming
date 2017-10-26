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
fp = '../build/Test.h5';

%Signal of Interest
SOI = [30];

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
freq = h5read(fp,'/listFreq');
elev = h5read(fp,'/listElev');

%Get Array Manifold
AM_mag = h5read(fp,'/Magnitude');
AM_phase = h5read(fp,'/Phase');

%Get incoming signal, add noise
fIdx = 1;
elevIdx = 1;

soiIdx = SOI + fIdx*length(freq) * (elevIdx-1) * length(elev);

x = AM_mag(:,soiIdx) .* exp(1j * AM_phase(:,soiIdx));
x = awgn(x,SNR,'measured');

%%  Computation:
    Rxx = x*x';

    P_bart = abs(DF_Bart(Rxx,AM_mag,AM_phase));
    P_bartChol = DF_Bart_Chol(Rxx,AM_mag,AM_phase);
 
    P_music = DF_MUSIC(Rxx,AM_mag,AM_phase,length(SOI));
    
    P_mvdr = DF_MVDR(Rxx,AM_mag,AM_phase);   
    
    [~,bartIdx] = max(P_bart);
    [~,bart_cholIdx] = max(P_bartChol);
    [~,musicIdx] = max(P_music);
    [~,mvdrIdx] = max(P_mvdr);
    
    bartIdx = floor(bartIdx / length(azm))*length(azm) + 1;
    bart_cholIdx = floor(bart_cholIdx / length(azm))*length(azm) + 1;
    musicIdx = floor(musicIdx / length(azm))*length(azm) + 1;
    mvdrIdx = floor(mvdrIdx / length(azm))*length(azm)+1;
    
    subplot(2,2,1)
    plot(azm,P_bart(bartIdx:bartIdx + length(azm)-1))
    title('Bartlet')
    hold on
    subplot(2,2,2)
    plot(azm,P_bartChol(bart_cholIdx:bart_cholIdx + length(azm)-1))
    title('Bartlet - Cholesky')
    subplot(2,2,3)
    plot(azm,P_music(musicIdx:musicIdx + length(azm)-1))
    title('MUSIC')
    subplot(2,2,4)
    plot(azm,P_mvdr(mvdrIdx:mvdrIdx + length(azm)-1))
    title('MVDR')
    
    
    
    
    
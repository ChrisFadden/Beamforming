function [ r ] = Position_ULA_PhaseProgression(M,d)
%%  Assumptions:
%   Uniform Linear Array
%   Same spacing between elements in a linear geometry
%   Phase reference is the first element of the array

%%  Inputs
%   M   Number of Antenna Elements
%   d   Spacing between elements    [half wavelengths]

%%  Calculation
r = (0:M-1)*d;

%%  Output:
    %   r   The position of the array elements in half wavelengths

end

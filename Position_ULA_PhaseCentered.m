function [ r ] = Position_ULA_PhaseCentered(M,d)
%%  Assumptions:
%   Uniform Linear Array
%   Same spacing between elements in a linear geometry
%   Phase reference is the center of the array

%%  Inputs
%   M   Number of Antenna Elements
%   d   Spacing between elements    [half wavelengths]

%%  Calculation
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

%%  Output:
    %   r   The position of the array elements in half wavelengths

end


function [ w ] = Weighting_Chebyshev( r, AoA, SLL )
%%  Assumptions:
    %Uniform Linear Array with proper small element spacing


%%  INPUTS:
    %   r       =   position in half-wavelengths
    %   AoA     =   Steering Direction
    %   SLL     =   Desired Sidelobe Level

%%  Calculations:
  
    w = ones(length(r),1);
    warning('I Have not implemented this yet');
%%  OUTPUTS:
    %   w   =   weighting vector (M x 1)
    

end


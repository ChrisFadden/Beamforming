function [ w ] = Weighting_ULA_Phased( M, AoA )
%%  Inputs:
    %M      =   Number of antenna elements (int > 0)
    %AoA    =   Desired Steering Direction ( -180 < AoA < 180 )
    
%%  Calculation:  
    w = ones(M,1);
    for mm = 1:M
       w(mm,1) = exp(-1j * (mm-1)*pi*cosd(AoA)); 
    end

%%  Output:
    % w     = M x 1 vector of complex weights
end


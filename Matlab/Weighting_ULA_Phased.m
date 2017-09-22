function [ w ] = Weighting_ULA_Phased( M, d, SOI )
%%  Assumptions:
    %Uniform Linear Array
    %Steers towards SOI
    %Doesn't null Interferers


%%  Inputs:
    %M      =   Number of antenna elements (integer > 0)
    %SOI    =   Signal of Interest ( -180 < SOI < 180 )
    
%%  Calculation:  
    w = ones(M,1);
    
    if(mod(M,2) == 0)
        for mm = 0:M/2-1
            w(M/2 + mm) = exp(-1j*mm*d*pi*cosd(SOI));
            w(M/2 - mm) = exp(1j*mm*d*pi*cosd(SOI));
        end
    else
        w(ceil(M/2)) = 0;
        for mm = 1:floor(M/2)
            w(ceil(M/2) + mm) = exp(-1j*mm*d*pi*cosd(SOI));
            w(ceil(M/2) - mm) = exp(1j*mm*d*pi*cosd(SOI));
        end
    end
    

%%  Output:
    % w     = M x 1 vector of complex weights
end


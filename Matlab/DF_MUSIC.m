function [ P ] = DF_MUSIC(Rxx, AM_mag,AM_phase,n)
%%  Description:
 %     MUSIC Algorithm
 %    
 %     Performs DF through the Multiple Signal
 %   Classification (MUSIC) algorithm.  An 
 %   extension of Parasenko's harmonic decomposition
 %   it basically uses eigendecomposition to do the DF
 
%%  Inputs:
 %      x is the input signal
 %     AM is the array manifold
 %      n is the number of SOI
%%  Outputs:
 %      P returns the power at each angle

%%  Computation:
    aH = (AM_mag .* exp(1j * AM_phase))';

    [V,D] = eig(Rxx);
    [~,idx] = sort(diag(D));
    V = V(:,idx);
    Vn = V(:,1:end-n);
    
    P = abs(aH * Vn).^2 * ones(size(Rxx,1)-n,1); 
    
    P = min(P) ./ P;
end
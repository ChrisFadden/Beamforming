function [ MS ] = MUSIC_Spectrum(x,AM,M)
%%  Assumptions:
    %  There are a known number of signals to detect

%%  Inputs:
    %   x = vector of complex signals at each antenna element
    %   M = Nu mber of signals to detect
    


%%  Calculation:   
   Rxx = x*x';
   [V,D] = eig(Rxx);
   [~,idx] = sort(diag(D));
   V = V(:,idx);
   Vn = V(:,1:end-M);
   
   MS = sum(abs(AM'*Vn).^2,2) * size(AM,1); 
end

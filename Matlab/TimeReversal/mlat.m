function rt=mlat(r,t,c,rt0)
% rt=mlat(t,c)
% found position rt in 2d of wave source
% it t - times of arrival
% in microphones with positions r
% c - speed of wave
% rt0 - initial guess
n=length(t); % number of microphones
itm=150; % number of iterations

rt=rt0; % initial guess

for it=1:itm
    % calulate shift:
    sh=zeros(2,1); % zeros for beginind
    % pairs:
    np=0; % number of pair
    for nc1=2:(n-1)
        r1=rt-r(1:2,nc1);
        r1l=sqrt(r1'*r1);
        for nc2=(nc1+1):n
            r2=rt-r(1:2,nc2);
            dtr=t(nc1)-t(nc2); % time difference requared
            r2l=sqrt(r2'*r2);
            d=r1l-r2l; % current distance differens
            dd=dtr*c-d; % on how much distance difference need to increas
            if r1l~=0
                n1=r1/r1l;
            else
                n1=zeros(2,1);
            end
            if r2l~=0
                n2=r2/r2l;
            else
                n2=zeros(2,1);
            end
            dn=n1-n2;
            dn2=(dn'*dn);
            if dn2~=0
                sht=dd*(dn)/dn2; % current shift
            else
                sht=zeros(2,1);
            end
            sh=sh+sht; % accumulate
            np=np+1;
        end
    end
    sh=sh/np; % mean shift from all pairs
    rt=rt+sh; % move point
end

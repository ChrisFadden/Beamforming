
c=1; % speed of wave
c2=c^2;
nx=256;
ny=256; % size
dx=0.1; % space step
dt=0.01; % time step

Lx=dx*nx;
Ly=dx*ny; % size

u=zeros(ny,nx); % u is matrix with pixels values

% u(128,192)=100;

x=0:dx:dx*(nx-1);
y=0:dx:dx*(ny-1);


close all;
hf=figure;
ha=axes;
hi=imagesc(x,y,u);
colorbar;
set(ha,'clim',[-1 1]);

% cyan colormap:
bl1=linspace(0,1,64)';
bl2=linspace(0.0,1,64)';
bl3=linspace(0.0,0,64)';
bl=[bl3 bl2 bl1];
colormap(bl);

zh=zeros(1,nx);
zh1=zeros(1,nx-1);
zv=zeros(ny,1);
zv1=zeros(ny-1,1);

% decay factor:
kk=7;
ka=kk*ones(ny,nx); % decay factor distribution
% [X,Y] = meshgrid(x,y);   
% RR=sqrt((X-Lx/2).^2+(Y-Ly/2).^2);
% ka=exp(RR);
ks=35; 
% ka1=ka(ks:end-ks,ks:end-ks);
% ka1=zeros(size(ka1));
% ka(ks:end-ks,ks:end-ks)=ka1;

ksx=ks*dx;
ksx1=Lx/2-ksx;

ycc=1;
for yc=y
    xcc=1;
    for xc=x
        ax=abs(xc-Lx/2);
        ay=abs(yc-Ly/2);
        ax=ax*(ax>ksx1);
        ay=ay*(ay>ksx1);
        ka2=max(ax/(Lx/2),ay/(Ly/2));
        ka2=((Lx/2)/ksx)*(ka2-1)+1;
        ka(ycc,xcc)=ka2*((ax>ksx1)||(ay>ksx1));
        xcc=xcc+1;
    end
    ycc=ycc+1;
end
ka=kk*ka;
% imagesc(ka); colorbar; % decay distribution,
% high only near edges and 0 in the center



dt3=dt^2*c2/dx^2;

u_old=u; % zero initial velocity
dlc=20;
R=0.5; % obsticle radius
ox=6;
oy=15; % obsttacle position
[X,Y] = meshgrid(x,y);   
RR=sqrt((X-ox).^2+(Y-oy).^2);
lm=RR<=R;
al=0:pi/24:2*pi;
hold on;
plot(ox+R*cos(al),oy+R*sin(al),'k-');
indo=find(lm(:));
u(indo)=0;
un(indo)=0;
u(indo)=0;
u_old(indo)=0;
tdx=1; % transedusers step
tN=10; % number of transenduses
tx=19.2; 
ty=12.5; % transendusers position
tL=tN*tdx; % length of array
ty0=ty-tL/2;
tya=ty0+(0:tdx:tdx*(tN-1)); % y-coordinaties
tyai=ceil(ny*tya/Ly); %converts to indexes
r=[tx*ones(size(tya));
    tya];
txi=ceil(nx*tx/Lx); %converts to indexes
lm=false(ny,nx);
lm(tyai,txi)=true;
indt=find(lm(:));
plot(tx*ones(size(tya)),tya,'r.');
T=0.55*(2*Lx/c); % time between start sending and start listerning
Ti=ceil(T/dt); % as index
TT=T/4; % time of sending/listerning
TTi=ceil(TT/dt);
gn=20; % gain
snd=true; % sinfind, snd=false => listerning
utd=zeros(tN,TTi); % signal recorded
utd0=zeros(tN,TTi); % to smooth edges
ht=title(' ');
rt=[Lx/2;Ly/2]; % intial guess for obstacle position
hrt=plot(rt(1),rt(1),'r^');
axis equal;
for TTic=1:TTi
    utd(:,TTic)=5*exp(-((TTic-TTi/2)/(TTi/20))^2);
    utd0(:,TTic)=exp(-((TTic-TTi/2)/(TTi/5))^2);
end
%for lc=1:500000
for lc=1:21041
    % new u:
    un=((2-ka*dt).*u-(1-ka*dt).*u_old+...
    dt3*([u(2:end,:);zh]+[zh;u(1:end-1,:)]+[u(:,2:end) zv]+[zv u(:,1:end-1)] -4*u));

    un(indo)=0;

    u_old=u;
    u=un;
    
    lc1=mod(lc-1,Ti)+1;
    if lc1<=TTi % if sending or listerning
        if snd
            % sending
            %for tNc=1:tN
                u(indt)=utd(:,lc1)';
            %end
            set(ht,'string','sending');
        else
            % listerning
            utd(:,lc1)=gn*u(indt)'; % with gain
            set(ht,'string','listerning');
        end
    else
        set(ht,'string','nothing');
    end
    
    if mod(lc,Ti)==(TTi+1)
        
        if ~snd
            % get obstacle position:
            lt=zeros(tN,1); % times
            for tNc=1:tN
                [tmp im]=min(utd(tNc,:));
                lt(tNc)=im*dt;
            end
            rt=mlat(r,lt',c,rt);
            % if no convergens and out of bouds, then return:
            if rt(1)<x(1)
                rt(1)=x(1);
            end
            if rt(1)>x(end)
                rt(1)=x(end);
            end
            if rt(2)<y(1)
                rt(2)=y(1);
            end
            if rt(2)>y(end)
                rt(2)=y(end);
            end
            set(hrt,'XData',rt(1),'YData',rt(2));
        end
        
        snd=~snd; % turn
     
        utd=-fliplr(utd); % revers time
        utd=bsxfun(@minus,utd,mean(utd,2)); % remove bias
        utd=utd.*utd0; % decrase in start and end to avoid jumps in signal
    end
    
    if mod(lc,dlc)==0
        set(hi,'CData',u);
        drawnow;
    end
    
end

a1=10;a2=6;b1=2;b2=3;h1=0.4;h2=0.15;t1=2;t2=4;
a=[a1,a2];
b=[b1,b2];
h=[h1,h2];
T=24;
t=[t1,t2];
[x1,x2] = fmincon(@(x) oljykustannusfunktio(x,a,b,h),...
    [4;4],[],[],[],[],[0;0],[], @(x) oljyrajoitus(x,t,T));
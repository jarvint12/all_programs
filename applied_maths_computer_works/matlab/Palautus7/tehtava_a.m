clear all;clc;close all

a=2;
b=0.2;
p=3;
q=0.1;
%x0 = 5;
%y0=2;
x0 = p/q;
y0 = a/b;

sim('peto')

figure
hold on
plot(tout,x)
plot(tout,y)
title('Ilves-jänis-suhde')
xlabel('t')
ylabel('Populaation koko')
legend('Jänikset', 'Ilvekset')

figure
plot(x,y)
title('Ilves-jänis-suhde')
xlabel('Jänisten lkm')
ylabel('Ilvesten lkm')

%x0 = p/q;
%y0 = a/b;


figure
plot(tout,x)
plot(tout,y)
title('Ilves-jänis-suhde')
xlabel('t')
ylabel('Populaation koko')
legend('Jänikset', 'Ilvekset')

figure
plot(x,y, 'x')
title('Ilves-jänis-suhde')
xlabel('Jänisten lkm')
ylabel('Ilvesten lkm')

hold off
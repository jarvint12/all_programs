%Tehtävä A: Log_normaalijakauma

%Tee luvuille eksponenttimuunnos
%Esimerkki: Luvun 3
%eksponenttimuunnos: exp(3)=20.0855.
clear all;clc;close all
x = randn(100,1);
for t=1:100
    y(t,1)=exp(x(t,1));
end
hold on
subplot(2,1,1)
hist(x,20)
title('Normaalijakautuneet luvut')
grid on
subplot(2,1,2)
hist(y,20)
title('Eksponenttimuunnokset')
grid on
hold off
close all

[parmhat, parmci] = lognfit(y,0.05);
parmhat
parmci


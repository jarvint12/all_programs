clear all;clc;

ydata = [2 8 19 32 43 45]';
xdata = [2 10 18 26 31 35]';
beta= [40,40,20];

w = kasvumalli(beta,xdata);
b_est = lsqcurvefit(@(beta, xdata) kasvumalli(beta,xdata),beta,xdata,ydata);

figure
hold on 
plot(xdata,ydata,'o')
x=[0:50];
plot(x,kasvumalli(b_est,x))
grid on
xlabel('aika päivissä')
ylabel('jyvän paino')
title('Jyvän painon aikariippuvuus')
ylim([0,46])
legend('Data pisteet', 'Kasvumalli')
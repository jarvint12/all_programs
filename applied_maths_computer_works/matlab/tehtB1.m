clear all;close all;
x=1900:10:2010;
y=[2.656 2.943 3.148 3.463 3.696 4.030 4.446 4.706 4.788 4.999 5.181 5.375];
figure;
plot(x,y,'o');
xlabel('vuodet');
ylabel('väestö');
P=polyfit(x,y,4);
hold on;
uudet_pisteet=1900:2050;
sovite=polyval(P,uudet_pisteet);
plot(uudet_pisteet,sovite)


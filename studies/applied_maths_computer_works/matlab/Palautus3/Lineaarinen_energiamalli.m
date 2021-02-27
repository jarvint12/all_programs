clear all
varallisuus = [20.0; 30.5;40.0; 55.1; 60.3; 74.9; 88.4; 95.2];
energia = [1.8; 3.0; 4.8; 5.0; 6.5; 7.0; 9.0; 9.1];
%Plottaa tehtavanannon data, luo lineaarinen malli ja piirra sen
%ennusteet valilla [10; 120] samaan kuvaan datan kanssa. Katso
%esimerkkiaa luento-osuuden esimerkista.

model = fitlm(varallisuus,energia,'linear');
hold on
plot(varallisuus, energia, 'rx');
x = [10:1:120]';
p = 0.36;
[ypred,yci] = predict(model,x,'alpha',p,'Prediction','observation');
plot(x,predict(model,x))
plot(x, ypred, '--')
plot(x, yci, '--')
grid on
xlabel('Kotitalouden varallisuus')
ylabel('Kulutettu energia')
legend('Mittaukset', 'Ennuste', 'Luottamusvälin yläraja', 'Luottamusvälin alaraja', 'location', 'best')
hold off
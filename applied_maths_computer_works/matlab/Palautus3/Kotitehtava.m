clear all, close all, clc

taajuus = [519; 549; 688; 740; 821];
jannite = [1.0; 1.2; 1.9; 2.4; 2.3];
virhe = [0.15; 0.40; 0.20; 0.30; 0.10];

[b, bci] = sovittaja(taajuus, jannite, virhe);
x_akseli = [500:1000];
y = b(1) + b(2)*x_akseli;
model = fitlm(taajuus, jannite, 'linear');
hold on
errorbar(taajuus, jannite, virhe, 'o')
plot(x_akseli, y)
plot(taajuus, predict(model, taajuus))
legend('Näytepiste virherajalla', 'Regressiosuora', 'Fitlm', 'location', 'best')
xlabel('Taajuus *(1/10^{12})')
ylabel('Pysäytysjännite')
hold off

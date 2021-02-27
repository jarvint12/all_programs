clear all; close all;
x = [519 549 688 740 821];
y = [1 1.2 1.9 2.4 2.3];
deltay = [0.15 0.4 0.2 0.3 0.1];

[b,bci] = sovittaja(x,y,deltay);
model = fitlm(x,y);
x1=[450:850];
t=[450 850]';
[ypred, yci] = predict(model, t, 'alpha', 0.36, 'Prediction', 'observation');

y1=b(1)+b(2)*x1;
plot(x1,y1)
hold on
plot(t,ypred)
errorbar(x,y,deltay,'o')
xlabel('valon taajuus')
ylabel('pysäytysjännite')
title('Pysäytysjännitteen taajuusriippuvuus')
legend('regressiosuora','fitlm-suora', 'data', 'Location','SouthEast')

%%
b11=bci(1,2);
b12=bci(2,2);

h1=b11*10^(-12)*1.6*10^(-19)
h2=b12*10^(-12)*1.6*10^(-19)
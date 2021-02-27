varallisuus = [20, 30.5, 40, 55.1, 60.3, 74.9, 88.4, 95.2]';
energia = [1.8, 3, 4.8, 5, 6.5, 7, 9, 9.1]';
model = fitlm(varallisuus, energia, 'linear');
t=[10:1:120]';
[ypred, yci] = predict(model, t, 'alpha', 0.36, 'Prediction', 'Observation');

plot(varallisuus, energia, 'x r')
hold on
plot(t, ypred)
plot(t, yci, '--')
xlabel('varallisuus')
ylabel('energian kulutus')
title('Energian kulutus varallisuuteen verrattuna')
legend('data pisteet', 'regressio suora', 'luottamusvälit')

%%

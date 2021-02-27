clear all
a = 0.89;
b = 0.89;
y = 500;
C(1) = a*2000;
I(1) = b*(C(1)-1000) + y;
Y(1) = C(1) + I(1);
for t = 2:50
    C(t) = a*Y(t-1);
    I(t) = b*(C(t)-C(t-1)) + y;
    Y(t) = C(t) + I(t);
end
t=1:50;
figure
subplot(2,1,1)
title('Timo Järvinen')
hold on
plot(t,C)
plot(t,I)
plot(t,Y)
legend('kulutus', 'Investointi', 'BKT', 'Location', 'Best')
hold off

clear all
for t = 1:50
    Y(t) = BKT(t);
end
t = 1:50;
subplot(2,1,2)
plot(t,Y, '.')
legend('BKT', 'Location', 'Best')
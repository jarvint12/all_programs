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
for t = 1:50
    X(t) = 1000*BKT(t);
end
t=1:50;
figure
subplot(3,1,1)
title('Timo Järvinen')
hold on
plot(t,C)
plot(t,I)
plot(t,Y)
plot(t,X, '.')
legend('kulutus', 'Investointi', 'BKT', 'BKT-AN')
xlabel('Vuosi')
ylabel('M€')
hold off

clear all
a = 0.75;
b = 1.4;
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
subplot(3,1,2)
hold on
plot(t,C)
plot(t,I)
plot(t,Y)
legend('kulutus', 'Investointi', 'BKT', 'Location', 'Best')
xlabel('Vuosi')
ylabel('M€')
hold off

clear all
a = 1.0;
b = 1.1;
y = 300;
C(1) = a*1000;
I(1) = b*(C(1)-500) + y;
Y(1) = C(1) + I(1);
for t = 2:50
    C(t) = a*Y(t-1);
    I(t) = b*(C(t)-C(t-1)) + y;
    Y(t) = C(t) + I(t);
end
t=1:50;
subplot(3,1,3)
hold on
plot(t,C)
plot(t,I)
plot(t,Y)
legend('kulutus', 'Investointi', 'BKT', 'Location', 'Best')
xlabel('Vuosi')
ylabel('M€')
hold off

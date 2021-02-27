alfa = 0.0011;
beeta = 0.03;
gamma = 0.0013;
s = [];
i = [];
r = [];
d = [];
s(1) = 999;
i(1) = 1;
r(1) = 0;
d(1) = 0;
for t = 1:100
    s(t+1) = s(t) - alfa * i(t) * s(t);
    i(t+1) = i(t) + alfa * i(t) * s(t) - beeta * i(t);
    r(t+1) = r(t) + beeta * i(t);
end

%%
figure;
hold on
plot(s,'b')
plot(i, 'g')
plot(r, 'r')
plot(d, 'm')
title('Atte Föhr')
xlabel('aika')
ylabel('Ihmisten määrä')
legend('Suspectible', 'Infected', 'Recovered', 'Dead')


a = 0.0011;
b = 0.03;
y = 0.0013;
s(1) = 999;
i(1) = 1;
r(1) = 0;
d(1) = 0;
for t=1:100
    s(t+1) = s(t) - a*i(t) * s(t);
    i(t+1) = i(t) + a*i(t)*s(t)-b*i(t) -y*i(t);
    r(t+1) = r(t) + b*i(t);
    d(t+1) = d(t) + y*i(t);
end
t = 0:100;
hold on
title('Timo Järvinen');
ylabel('Hlö');
xlabel('Aika');

plot(t,s);
plot(t,i);
plot(t,r);
plot(t,d);

legend('Terveet', 'Sairastuneet', 'Parantuneet', 'Kuolleet', 'Location', 'Best');
hold off
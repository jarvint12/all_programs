clear all
close all

tj = [2;10;18;26;31;35];
wj = [2;8;19;32;43;45];
beta = [40,40,20];

w = kasvumalli(beta,tj);
x_akseli = [0:50];
b_est = lsqcurvefit(@(beta,tj) kasvumalli(beta,tj),beta,tj,wj);
figure
hold on
plot(tj,wj,'o');
xlabel('Mittauspäivä')
ylabel('Jyvän paino')
title('Kasvumalli')
plot(x_akseli, kasvumalli(b_est, x_akseli))
ylim([0,46])
grid on
hold off
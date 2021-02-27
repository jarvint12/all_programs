clear all; clc; close all

%%a-kohta: Veden m‰‰r‰ kasvaa lineaarisesti
A=5;
f_in_orig=20;

%b-kohta: Veden pinta tasoittuu 100 litraan
k_v=2.0;

%c-kohta: about ajanhetkell‰ 300, 225 litraa
h0 = 100;

%d-kohta: Ei saavuteta s‰‰tˆtavoitetta
h_ref = 100;
P=15;
I=1;
D=8;

sim('vesitankki')

figure
subplot(3,1,1)
plot(tout,h)
xlabel('t/s')
ylabel('h/m')
legend('pinnan korkeus')
title('Timo J‰rvinen')

subplot(3,1,2)
plot(tout,f_out)
hold on
plot(tout,f_in)
legend('f_{out}', 'f_{in}')
xlabel('t/s')
ylabel('l/s')
hold off

subplot(3,1,3)
plot(tout, pi_out)
hold on
plot(tout,pi_out_raja)
xlabel('t/s')
ylabel('l/s')
legend('PI-s‰‰timen ulostulo', 'Rajoittimella')
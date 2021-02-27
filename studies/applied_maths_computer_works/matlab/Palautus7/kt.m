%Eri kohdista mallia juttuja mit‰ tahdotaan piirt‰‰,
%3 subplot: h, (f_in, f_out), (Pid1, PID2)
%
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
P=0;
I=0;
D=0;
f=0.01;

sim('vesitankki')

figure
subplot(2,1,1)
plot(tout,f_out)
legend('f_{out}')
xlabel('t/s')
ylabel('l/s')

subplot(2,1,2)
plot(tout,f_in)
legend('f_{in}')
xlabel('t/s')
ylabel('l/s')
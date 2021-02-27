%%
% A-kohdan arvot
alfa = 0.89;
beeta = 0.89;
gamma = 500; % miljoonissa
C = [1000];
I = [1000];
BKT = [2000];

%%
%B-kohdan arvot
alfa = 0.75;
beeta = 1.4;
gamma = 500; % miljoonissa
C = [1000];
I = [1000];
BKT = [2000];

%%
%C-kohdan arvot
alfa = 1.0;
beeta = 1.1;
gamma = 300; % miljoonissa
C = [500];
I = [500];
BKT = [1000];

%%
%Tällä lasketaan vektorit BKT:lle, investoinnelle ja kustannuksille. A, B
%ja C kohtien arvot lasketaan erikseen
for t = 1:50
    C(t+1) = alfa * BKT(t);
    I(t+1) = beeta * (C(t+1) - C(t)) + gamma;
    BKT(t+1) = C(t+1) + I(t+1);
end

%% 
%Piirretään kuvaajat B kohta
ts = 0:50;
figure;
hold on;
plot(ts,C, 'b');
plot(ts,I, 'r');
plot(ts,BKT, 'm');
legend('Cost', 'Investment','BKT')
xlabel('Vuodet')
ylabel('Miljoonaa euroa')
title('Atte Föhr')

%%
%Lasketaan analyyttinen arvio ja plotataan se A-kohdan kuvaajan kanssa 
t = 1:51;
ts=0:50;
X = BKT1(t);
figure;
hold on
plot(ts,X, '.')
plot(ts,C, 'b');
plot(ts,I, 'r');
plot(ts,BKT, 'm');
xlabel('Vuodet')
ylabel('Miljoonaa euroa')
title('Atte Föhr')
legend('Analyyttinen tulos','Kustannukset','Investoinnit','Bkt')

%%
%C-kohdan kuvaaja
ts = 0:50;
figure;
hold on;
plot(ts,C, 'b');
plot(ts,I, 'r');
plot(ts,BKT, 'm');
legend('Cost', 'Investment','BKT')
xlabel('Vuodet')
ylabel('Miljoonaa euroa')
title('Atte Föhr')
    
%Kotitehtävä: Newsvendor

clear all;clc;close all

c=30; %Ostohinta
p=120; %Myyntihinta
q=0; %Tilausmäärä
m=1;
while(q<=500)
    n=1; %Matriisin indeksi
    A=[];
    while(n<50000) %Pyöritetään 100 tapausta
        D=round(300*rand,0); %Kysyntä, pyöristettynä kokonaisluvuksi
        Z=rand; %Toimitettujen vekottimien osuus tilausmäärästä
        A(n,1)=min(D,Z*q)*p-c*(Z*q); %Tulos, Z*q= Vesalle toimitetut vekottimet
        %A(n,1)=min(D,q)*p-c*q;
        n=n+1;
    end
%B((q+1),m) = numel(find(A<0))/(n-1);
B((q+1),m) = mean(A); %Tallennetaan kierrosten odotusarvo matriisiin
q=q+1;
m=m+1;
end
x=0:500;
y=[];
i=1;
while(i<502)
    y(1,i)=B(i,i);
    i=i+1;
end
figure
plot(x,y)
title('Timo Järvinen')
xlabel('Tilausmäärä')
ylabel('Voitto')
ytickformat('eur')
axis tight
hold off
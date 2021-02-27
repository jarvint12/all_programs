a=[1 2 3];
b=[1 5 9];
C=eye(3);
D=ones(3,2);
E=zeros(2,3);

A = [1900 1910 1920 1930 1940 1950 1960 1970 1980 1990 2000 2010];
B = [2.656 2.943 3.148 3.463 3.696 4.030 4.446 4.706 4.788 4.999 5.181 5.375];

%p = polyfit(A,B,4);
%x2 = 1900:10:2040;
%y2 = polyval(p,x2);
%hold on
%plot(A,B)
%plot(x2,y2)
%hold off

%Kotitehtävä
clear all;

Dataset = xlsread('msft.xlsx','A1:H161');
Dataset2 = xlsread('ibm.xlsx','A1:H161');
Dataset3 = xlsread('djia',1,'E:E');
x = 1:152;
y = flipud(Dataset(1:152,6));
z = flipud(Dataset2(1:152,6));
format bank
v = flipud(Dataset3);
subplot(3,1,1);
plot(x,y);
title('Microsoftin osakekurssi');
ylabel('$');
xlabel('Päivä');
subplot(3,1,2);
plot(x,z);
title('IBM:n osakekurssi');
ylabel('$');
xlabel('Päivä');
subplot(3,1,3);
plot(x,v(1:152));
title('DJIA-indeksin arvo');
ylabel('Indeksin arvo');
xlabel('Päivä');

%%
corr1=corr(y,z);
corr2=corr(v(1:152),z);
corr3=corr(v(1:152),y);

subplot(3,1,1);
scatter(y,z, '.');
xlabel('Microsoft');
ylabel('IBM');
title(['IBM ja MSFT hajontakuvio. Corr=',num2str(corr1)]);
grid on
subplot(3,1,2);
scatter(v(1:152),z, '.');
xlabel('DJIA');
ylabel('IBM');
title(['IBM ja DJIA hajontakuvio. Corr=',num2str(corr2)]);
grid on
subplot(3,1,3);
scatter(v(1:152),y, '.');
xlabel('DJIA');
ylabel('Microsoft');
title(['MSFT ja DJIA hajontakuvio. Corr=',num2str(corr3)]);
grid on

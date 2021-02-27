clear all;
msft= xlsread('msft',1,'F:F');
msft= flipud(msft);
ibm= xlsread('ibm',1,'F:F');
ibm = flipud(ibm);
djia= xlsread('djia',1,'E:E');
djia= flipud(djia);
x=1:161;

%%
figure;
subplot(3,1,1);
plot(x,ibm);
title('IBM:n osakekurssi');
xlabel('p�iv�');
ylabel('kurssi');

subplot(3,1,2);
plot(x,msft);
title('Microsoftin osakekurssi');
xlabel('p�iv�');
ylabel('kurssi');

subplot(3,1,3);
plot(x,djia);
title('Down Jones Industrial Average');
xlabel('p�iv�');
ylabel('kurssi');
%%
corr1=corr(ibm,msft);
corr2=corr(ibm,djia);
corr3=corr(msft,djia);


subplot(3,1,1);
scatter(ibm,msft);
title(['IBM ja MSFT hajontakuvio. Corr=',num2str(corr1)])
xlabel('IBM');
ylabel('MSFT');

subplot(3,1,2);
scatter(ibm,djia);
title(['IBM ja DJIA hajontakuvio. Corr=',num2str(corr2)]);
xlabel('IBM');
ylabel('DJIA');

subplot(3,1,3);
scatter(msft,djia)
title(['MSFT ja DJIA hajontakuvio. Corr=',num2str(corr3)])
xlabel('MSFT')
ylabel('DJIA')
%%
%laita aika kulkemaan oikeinp�iin flipud 
%piirr� aikasarjat:vaaka-akselilla aika,pystyll� arvot
%piirr� aikasarjat samaan kuvaikkunaan subplot(3,1,1)
%nime� akslit plus otsikot 
%2. 3 eri hajonta kuvaa. scatter kometoa plus corr 
%Tehtävä B: Monte Carlo
clear all;close all;clc

R = exprnd(3,15,1);

k = 1;
while(k<7) %Pyöritetään tilanne eri kassamäärillä
    j=0;
    subplot(3,2,k)
    while(j<10) %Piirretään samalla kassamäärällä 10 kertaa
        t=0;
        i=1; %Aika-asiakasmäärä-matriisin indeksi
        A=[]; %Luodaan tyhjä matriisi asiakasmäärille ja ajanhetkille
        kassoja_kaytossa = 0;
        jono=0;
        while t<8*60 %
            t_asiakas = exprnd(3); %Aika asiakkaan saapumiseen
            m=1;
            kuluva_aika=[];
            kuluva_aika(1,1)=Inf; %Aika kassan vapautumiseen, jos kassoja ei käytössä arvona pysyy inf
            while (m<=kassoja_kaytossa) %Mikäli kassoja käytössä useita, arvotaan jokaiselle oma aika
                kuluva_aika(m,1)=exprnd(5);
                m=m+1;
            end
            t_kassa=min(kuluva_aika); %Katsotaan, milloin seuraava kassa vapautuu
            if t_asiakas<t_kassa %Mikäli aika asiakkaan saapumiseen on pienempi kuin kassan vapautumiseen
                if kassoja_kaytossa<k
                    kassoja_kaytossa = kassoja_kaytossa+1; %Asiakas menee suoraan kassalle
                else
                    jono = jono+1; %Lisätään jonoon yksi
                end
            else %Mikäli kassan vapautumiseen on pienempi aika (eli kassoja on myös käytössä)
                if jono==0 %Mikäli ketään ei ole enää jonossa
                    kassoja_kaytossa=kassoja_kaytossa-1; %Kassoja vapautuu yksi
                else
                    jono = jono-1;
                end
            end
            t = t+min(t_asiakas,t_kassa); %Uuteen aikaan lisätään toteutunut aika
            A(i,1)=t; %Matriisiin lisätään uudelle kohdalle aika ja jono
            A(i,2)=jono; %Jono (kassojen asiakkaita ei lasketa mukaan)
            i=i+1; %Siirrytään matriisin seuraavalle kohdalle seuraavaa kierrosta varten
        end
        stairs(A(:,1),A(:,2)) %Piirretään tilanne
        hold on
        j=j+1; %Looppi samalla kassamäärällä lähtee pyörimään uudestaan
    end
    title(strcat(num2str(k), ' kassaa'))
    xlabel('Aika (min)')
    ylabel('Asiakkaiden lkm')
    axis tight
    grid on
    hold off
    k = k+1; %Kassamäärää kasvatetaan yhdellä
end
%Teht�v� B: Monte Carlo
clear all;close all;clc

R = exprnd(3,15,1);

k = 1;
while(k<7) %Py�ritet��n tilanne eri kassam��rill�
    j=0;
    subplot(3,2,k)
    while(j<10) %Piirret��n samalla kassam��r�ll� 10 kertaa
        t=0;
        i=1; %Aika-asiakasm��r�-matriisin indeksi
        A=[]; %Luodaan tyhj� matriisi asiakasm��rille ja ajanhetkille
        kassoja_kaytossa = 0;
        jono=0;
        while t<8*60 %
            t_asiakas = exprnd(3); %Aika asiakkaan saapumiseen
            m=1;
            kuluva_aika=[];
            kuluva_aika(1,1)=Inf; %Aika kassan vapautumiseen, jos kassoja ei k�yt�ss� arvona pysyy inf
            while (m<=kassoja_kaytossa) %Mik�li kassoja k�yt�ss� useita, arvotaan jokaiselle oma aika
                kuluva_aika(m,1)=exprnd(5);
                m=m+1;
            end
            t_kassa=min(kuluva_aika); %Katsotaan, milloin seuraava kassa vapautuu
            if t_asiakas<t_kassa %Mik�li aika asiakkaan saapumiseen on pienempi kuin kassan vapautumiseen
                if kassoja_kaytossa<k
                    kassoja_kaytossa = kassoja_kaytossa+1; %Asiakas menee suoraan kassalle
                else
                    jono = jono+1; %Lis�t��n jonoon yksi
                end
            else %Mik�li kassan vapautumiseen on pienempi aika (eli kassoja on my�s k�yt�ss�)
                if jono==0 %Mik�li ket��n ei ole en�� jonossa
                    kassoja_kaytossa=kassoja_kaytossa-1; %Kassoja vapautuu yksi
                else
                    jono = jono-1;
                end
            end
            t = t+min(t_asiakas,t_kassa); %Uuteen aikaan lis�t��n toteutunut aika
            A(i,1)=t; %Matriisiin lis�t��n uudelle kohdalle aika ja jono
            A(i,2)=jono; %Jono (kassojen asiakkaita ei lasketa mukaan)
            i=i+1; %Siirryt��n matriisin seuraavalle kohdalle seuraavaa kierrosta varten
        end
        stairs(A(:,1),A(:,2)) %Piirret��n tilanne
        hold on
        j=j+1; %Looppi samalla kassam��r�ll� l�htee py�rim��n uudestaan
    end
    title(strcat(num2str(k), ' kassaa'))
    xlabel('Aika (min)')
    ylabel('Asiakkaiden lkm')
    axis tight
    grid on
    hold off
    k = k+1; %Kassam��r�� kasvatetaan yhdell�
end
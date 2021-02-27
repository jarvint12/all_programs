function w = kasvumalli(beta,t)
%maxw = maksimipaino, maxt = aika, jolloin maxw, tv = kasvunopeus suurimmillaan
maxw = beta(1);
maxt = beta(2);
tv = beta(3);

w = maxw.*(1+(maxt-t)./(maxt-tv)).*(t/maxt).^(maxt./(maxt-tv));
[~,i]=max(w);
w(i:end)= maxw;
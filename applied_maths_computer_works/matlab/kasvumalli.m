function w = kasvumalli(beta, xdata)
wmax = beta(1);
tmax = beta(2);
tv = beta(3);
wmax

w = wmax.*(1+((tmax-xdata)./(tmax-tv))).*(xdata/tmax).^(tmax./(tmax-tv));
[~,i]=max(w);
w(i:end)= wmax;
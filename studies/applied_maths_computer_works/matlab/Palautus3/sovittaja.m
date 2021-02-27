function [b, bci] = sovittaja(x,y,deltay)
D = sum(1./deltay.^2)*sum(x.^2./deltay.^2)-(sum(x./deltay.^2))^2;

a = (sum(1./deltay.^2)*sum(x.*y./deltay.^2));
e = (sum(x./deltay.^2)*sum(y./deltay.^2));

b(2) = 1/D*(a-e);
b(1) = 1/D*(sum(x.^2./deltay.^2)*sum(y./deltay.^2)-sum(x./deltay.^2)*sum(x.*y./deltay.^2));

deltab2 = sqrt(1/D*sum(1./deltay.^2));
deltab1 = sqrt(1/D*sum(x.^2./deltay.^2));
bci = [b(1)- deltab1, b(2)- deltab2; b(1)+ deltab1, b(2) + deltab2];

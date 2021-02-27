function [b, bci] = sovittaja(x,y,deltay)
%lasketaan kertoimen D sekä b0 ja b1 osia for loopilla
for i = 1:5
    D1(i) = (1/deltay(i)^2);
    D2(i) = ((x(i)^2)/(deltay(i)^2));
    D3(i) = (x(i)/(deltay(i)^2));
    b11(i) = (x(i)*y(i))/(deltay(i))^2;
    b12(i) = (y(i))/(deltay(i))^2;
end
%ja summilla
D11=sum(D1);
D22=sum(D2);
D33=sum(D3);
B11=sum(b11);
B12=sum(b12);
%lasketaan kerroin D
D = D11*D22-D33^2;
%lasketaan b1 ja b0
b1=(1/D)*(D11*B11-D33*B12);
b0=(1/D)*(D22*B12-D33*B11);
%ja deltab1 ja deltab0
deltab1=sqrt((1/D)*D11);
deltab0=sqrt((1/D)*D22);

%luodaan b vektori ja bci matriisi
b = [b0,b1];
bci= [b0-deltab0, b1-deltab1;b0+deltab0,b1+deltab1];



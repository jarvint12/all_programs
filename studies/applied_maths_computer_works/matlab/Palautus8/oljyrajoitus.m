function [c, ceq] = oljyrajoitus(x,t,T)
c = T-t(1)*x(1)+t(2)*x(2);
ceq=[];
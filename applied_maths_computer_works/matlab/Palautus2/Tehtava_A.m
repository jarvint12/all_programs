%Tehtava1: Nainen, ennen 1970 syntynyt, gen1>5, gen2>3, viim.tark. <2010
m = 0;
i = 1;
load('asiakasdata.mat');
while i<=10000
    if asiakasdata(i,1) == 1
        if asiakasdata(i,2<1970)
            if asiakasdata(i,3) >5
                if asiakasdata(i,4)>3
                    if asiakasdata(i,6)<2010
                        m = m+1;
                    end
                end
            end
        end
    end
    i = i+1;
end
m
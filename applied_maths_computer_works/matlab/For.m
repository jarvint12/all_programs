x = 0;
for i = 1:1:10000 
    if asiakasdata(i,1) == 1
        if asiakasdata(i,2) < 1970
            if asiakasdata(i,3) > 5
                if asiakasdata(i,4) > 3
                    if asiakasdata(i,6) < 2010
                        x = x +1;
                    end
                end
            end
        end
    end
end
x
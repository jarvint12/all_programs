function alkuluku = omafunktio(N)
res = N;
x =isprime(res);
while x == 0
    res = res +1;
    x = isprime(res);
end
alkuluku=res;
end

install.packages("rrcov")
library(rrcov)


D <- read.table("wood.txt", header=TRUE, sep="\t")
regular_covm <- cov(D)
regular_covm
MCD_covm <- CovMcd(D,alpha=1/2) 
MCD_covm@cov


s.maha <- mahalanobis(D, center=colMeans(D), cov=regular_covm)
r.maha <- mahalanobis(D, center=MCD_covm@center, cov=MCD_covm@cov)

plot(c(1,nrow(D)),range(sqrt(c(s.maha,r.maha))),type="n",
     xlab="Observation",ylab="Mahal. distance")

points(1:nrow(D),sqrt(s.maha),col="green",pch=16)

points(1:nrow(D),sqrt(r.maha),col="blue",pch=16)


legend("topleft",col=c("green","blue"),cex=0.8,legend=c("Regular","MCD"),
       pch=c(16,16))


###Problem 2
library(mvtnorm)
set.seed(123)
n <- 200

D1 <- rmvnorm(n,mean=c(0,0),sigma=diag(2))
plot(D1, pch = 19, col="blue")

cov1  <- cov(D1)
rcov1 <- CovMcd(D1,alpha=1/2)@cov
cov1
rcov1

###Bivariate t-distribution

D2 <- rmvt(n,df=5,sigma=diag(2))
plot(D2, pch = 19, col="blue")
cov2  <- cov(D2)
rcov2 <- CovMcd(D2,alpha=1/2)@cov
cov2
rcov2

#####Bivariate Weibull-Gamma distribution

x1 <- rweibull(n,shape=1,scale=2)
x2 <- rgamma(n,shape=2,scale=1)
D3 <- cbind(x1,x2)
plot(D3, pch = 19, col="blue")

cov3 <- cov(D3)
rcov3 <- CovMcd(D3,alpha=1/2)@cov
cov3
rcov3



data<-read.table("DECATHLON.txt", header=T, sep="\t", row.names = 1)
View(data)

DEC<-data[,-c(1,12,13)]
str(DEC)
head(DEC)
pairs(DEC)

plot(DEC$R100m,DEC$R400m, xlab="Running 100m", ylab="Running 400m", main="100m vs 400m", type="n")
text(DEC$R100m,DEC$R400m,labels=rownames(DEC))



# PCA
DEC.PCA<-princomp(DEC,cor=FALSE)
names(DEC.PCA)
DEC.PCA$call #Call to create DEC.PCA
DEC.PCA$scores # Y matrix from the lecture slides
DEC.PCA$n.obs #Number of objects
DEC.PCA$center # Sample means - same as colMeans(DEC)
DEC.PCA$loadings # eigenvector matrix (G matrix from the slides), small values are not shown
DEC.PCA$loadings[1,1]
DEC.PCA$sdev # standard deviations of each principle component
plot(DEC.PCA, las=2) #Varuances of principle components


#The variances of principle components are just eigenvalues of the covariance matrix of the original data
#Princomp uses biased max. likelihood estimator for the covariance matrix
n<-nrow(DEC)
DEC_cov<-(n-1)/n * cov(DEC)
DEC_cov_eval <- eigen(DEC_cov)$values
DEC_cov_eval
(DEC.PCA$sdev)^2

#b how much variation is explained by first k (10) principal components

#If k = 4->trace of 4 first components and normalize with trace of everything
sum(DEC_cov_eval[1:4])/sum(DEC_cov_eval) #About 70% explained by the first 4 components

plot(cumsum(DEC.PCA$sdev^2 / sum(DEC.PCA$sdev^2)), 
     type='b',pch=21, lty=3, bg=2, cex=1.5, ylim=c(0,1),
     xlab='Principal component', ylab='Cumulative proportion of variance',
     axes = F, frame.plot = T)
axis(1, at=1:10, tck=0.02)
axis(2, at=0:10/10, las=2)
abline(0,1/10,lty=3)


# C. Choose a sucient amount of principal components and try to interpret them. Visualize the scores of the observations with respect to the first two principal components.

PC1PC2<- DEC.PCA$scores[,1:2]
LD1LD2 <- DEC.PCA$loadings[,1:2]

pc.axis <- c(-max(abs(PC1PC2)), max(abs(PC1PC2)))
axis <- c(-0.8,0.8) #Limits to axis

plot(PC1PC2, xlim=pc.axis, ylim=pc.axis, pch=21, bg=8, cex=1.25)
par(new=T)
plot(LD1LD2, axes=F, type= "n", xlab='', ylab='',
     xlim=axis, ylim=axis)
axis(3,col=2)
axis(4, col=2)
arrows(0,0,LD1LD2[,1], LD1LD2[,2], length=0.1, col=2)
text(LD1LD2[,1], LD1LD2[,2], rownames(LD1LD2))
abline(h=0, lty=3)
abline(v=0, lty=3)



# D. 

cov(DEC.PCA$scores) # Diagonal, as expected
(n-1)/n*diag(cov(DEC.PCA$scores)) # The diagonal elements are equal to the variances of the principal components
colMeans(DEC.PCA$scores) # Zero as expected
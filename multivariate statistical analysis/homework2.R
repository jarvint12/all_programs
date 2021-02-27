mu=matrix(c(4,7), nrow=2)
mu
sigma<-matrix(c(10,6,6,8), nrow=2)
sigma

library("mvtnorm")
samples<-rmvnorm(100, mu, sigma)
samples

#A plot and label with observation number
plot(samples, ylim=c(0,15), xlim=c(0,13))
text(samples[,1],samples[,2]+1, 1:nrow(samples), cex=0.5)

#B. perform covariance based PCA transformation

sample.PCA<-princomp(samples,cor=FALSE)
sample.PCA
names(sample.PCA)

# C. Plot the score matrix
plot(sample.PCA$scores)
text(sample.PCA$scores[,1], sample.PCA$scores[,2]+0.7, 1:nrow(sample.PCA$scores), cex=0.5)


# Compare the plots of (a) and (c) and describe the differences.
par(mfrow=c(1,2))

plot(samples, ylim=c(0,15), xlim=c(0,13), main="Samples")
text(samples[,1],samples[,2]+0.5, 1:nrow(samples), cex=0.5)

plot(sample.PCA$scores, ylim=c(-10,10), xlim=c(-10,10), main="PCA")
text(sample.PCA$scores[,1], sample.PCA$scores[,2]+0.5, 1:nrow(sample.PCA$scores), cex=0.5)

# Calculate the G and Y matrices without using any existing PCA functions.
sample_cov<-(n-1)/n * cov(samples)
G<-eigen(sample_cov)$vector
Y<-sweep(samples,2,colMeans(samples), "-")%*%G

# Verify that the estimated scores and the loadings are equal (up to signs)
round(abs(Y),6)==round(abs(sample.PCA$scores),6)

G
sample.PCA$loadings

# Plot the directions of the first and second principal component to the original data
PC1PC2<- sample.PCA$scores[,1:2]
LD1LD2<-sample.PCA$loadings[,1:2]

par(mfrow=c(1,1))
pc.axis <- c(-max(abs(PC1PC2)), max(abs(PC1PC2)))
axis <- c(-0.8,0.8) #Limits to axis

plot(PC1PC2, xlim=pc.axis, ylim=pc.axis, pch=21, bg=8, cex=1.25)
par(new=TRUE)
plot(LD1LD2, axes=FALSE, type= "n", xlab='', ylab='',
     xlim=axis, ylim=axis)
axis(3,col=2)
axis(4, col=2)
arrows(0,0,LD1LD2[,1], LD1LD2[,2], length=0.1, col=2)
text(LD1LD2[,1], LD1LD2[,2], rownames(LD1LD2))
abline(h=0, lty=3)
abline(v=0, lty=3)

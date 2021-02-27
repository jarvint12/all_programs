#1. Take sample

n=100
D1 <- rnorm(n,mean=0, sd=1)

plot(D1)

#2. Count median

orig_median<-median(D1)

#3. Add 1 data point, count median again, take difference multiplied by n+1
D2<-D1
differences<-vector()
new_medians<-vector()
i<-1
for (y in -3000:3000) {
  D2[length(D1)+1]<-y
  new_medians[i]<-median(D2)
  differences[i]<-(n+1)*abs(new_medians[i]-orig_median)
  i<-i+1
}

#4. Plot
plot(c(-3000,3000),c(min(min(D1), min(differences)), max(max(D1), max(differences))),type="n",
     xlab="Y or index",ylab="Value")
points(seq(-3000,3000,1), differences, col="red")
points(seq(-3000,3000,1), new_medians, col="black")
points(1:length(D1),D1, col="blue")
points(length(D1)/2, orig_median, col="brown")
orig_median
max(differences)


# Sample median is a robust estimator.
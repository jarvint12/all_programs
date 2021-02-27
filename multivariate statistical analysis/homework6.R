setwd("C:/Users/TimoJ/Documents/Yliopisto/Maisteri/Multivariate Statistical Analysis/week6")
library(ca)
data<-read.table("SMOKING.txt", header=T, row.names=1)
data
SD <- data[-dim(data)[1],-dim(data)[2]]
SD

v1 <- matrix(rowSums(SD),ncol=1)
v2 <- matrix(colSums(SD),nrow=1)

#a

#Row profiles
SD/v1

#Col profiles
SD/v2[col(SD)]


#b How much of the variation is explained by the combination of components 1 and 3
SD.ca <- ca(SD)
SD.ca
87.76+0.49

total_variations<-SD.ca$sv^2/sum(SD.ca$sv^2)
(total_variations[1]+total_variations[3])*100

#Produce the BCA graph with respect to the rst two components.
plot(SD.ca)
plot(SD.ca,arrows=c(T,T),map="symmetric") 
#plot(SD.ca,arrows=c(T,T),map="symmetric",dim=c(2,4))

#plot(SD.ca, arrows=c(T,T), map="rowprincipal")

#According to (c), which employees are more frequently heavy smokers? Justify!
#Heavy smoking has a low angle with junior managers, so junior managers are more frequently heavy smokers. In addition, the arrow is long, so it has high inertia,
#which means association between that variable with heavy smoking is high.
summary(SD.ca)
#Heavy: 99.5, Medium 98.3 

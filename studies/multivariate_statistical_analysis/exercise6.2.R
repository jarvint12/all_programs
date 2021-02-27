library(ca)
data3 <- read.table("SCIENCEDOCTORATES.txt",header=T,sep="",row.names=1)
# View(data)
data=SCIENCEDOCTORATES
# Again, remove the total col/row
SD <- data[-dim(data)[2]]
dim(SD)

# To interpret correspondence analysis, the first step is to evaluate whether there is a significant
# dependency between the rows and columns.


n <- sum(SD)

v1 <- matrix(colSums(SD),nrow=1)
v2 <- matrix(rowSums(SD),ncol=1)

#theoretical frequencies under independence
E <- v2 %*% v1/n

I <- dim(SD)[1]
J <- dim(SD)[2]

s <- 0
#chi-square statistic
for(i in 1:I){
  for(j in 1:J){
    s <- s + ( SD[i,j]-E[i,j] )^2/(E[i,j])
  }
}

pchisq(s,df=((I-1)*(J-1)),lower.tail=F)

# H0: Discipline and Year are independent
# H1: Discipline and Year are not independent

chisq.test(SD)
# there is evicende that there is statistically
# significant association between the number
# of doctors graduated and the year (in USA)

help(ca)


SD.ca <- ca(SD) #set nd=8 to make all columns visible in summary
names(SD.ca)

SD.ca$sv #The roots of singular values related to the PCA transformation for rows/cols
# (how much variation explained by the principal components)
# for symmetric matrices, singular values = |eigenvalues|
# (here sv's are used since the package uses svd instead of eigen)

# The chi-squared distances from the "center", where variables close to center do not deviate from the
# independence assumption.
SD.ca$rowdist
SD.ca$rownames

SD.ca$coldist
SD.ca$colnames

# Variables distant from the origin represent variables different from the average profile
# The distances below are scaled versions of the distances in the plot

SD.ca$rowcoord #scaled coordinates 
SD.ca$colcoord 

summary(SD.ca)
# We get the coordinates in summary with:
SD.ca$rowcoord[11,]*SD.ca$sv*1000 #Coordinates for anthropology (note that we multiply with the singular-values)
#distance from the "center" for engineering
sqrt(sum((SD.ca$rowcoord[1,]*SD.ca$sv)^2)) 

########################
# Inertia
########################
n <- sum(SD)

# How much of the total "variation" the specific variable explains
# i.e. how much it contributes to the chi-squared statistic

# Inertia is the chi squared statistic divided by n

SD.ca$rowinertia 
SD.ca$colinertia

#Note that
sum(SD.ca$rowinertia)
sum(SD.ca$colinertia)
#is the same as
sum(SD.ca$sv^2)
s/n 

SD.ca$rowinertia/sum(SD.ca$sv^2) #these proportional values are the ones seen in summary(SD.ca)
SD.ca$colinertia/(s/n)
# You can get the single row-inertia values by fixing i (the row index)
s2 <- 0

#For physics, i =3

i <- 3
  for(j in 1:J){
    s2 <- s2 + ( SD[i,j]-E[i,j] )^2/(E[i,j])
  }


s2/n 

###############################################

SD.ca$rowmass
SD.ca$colmass # Relative marginal frequencies of the original table

margin.table(as.matrix(SD),1)/sum(SD)
margin.table(as.matrix(SD),2)/sum(SD)


SD.ca$N #The original table


# rowsup,colsup, nd is related if you want to have supplementary
# rows/columns while still having the original margins of the
# table

SD.ca
summary(SD.ca)
# Note that the quantities are multiplied by 1000
# Quality of representation = as in the lecture slides, but here we consider the angle between profiles and 
# the plane spanned by the two first principal components
# Squared correlations = quality of representation from lecture slides
# also, the sum of the squared correlations is the quality of representation.

# ctr = contribution in forming that ca-component (contributions sum to 1)
# important variables related to forming the specific component have a high ctr 

# k=1 and k=2 are the coordinates on the plot 

names(summary(SD.ca)$rows)

# Contributions sum up to 1
# Contribution of engineering to the second axis
margins = margin.table(as.matrix(SD),1)/sum(SD)
margins[1]*SD.ca$rowcoord[1,2]^2
# If the rows and columns were independent, ctr would be same for every variable

# Squared correlation of biology with the second component
d2 = (SD.ca$rowcoord[6,]*SD.ca$sv)^2
d2[2]/sum(d2)

plot(SD.ca)


# Note that below we have not "scaled" the variables using the formula in this weeks proof
plot(SD.ca,arrows=c(T,T),map="symmetric") 
plot(SD.ca,arrows=c(T,T),map="symmetric",dim=c(2,4))

plot(SD.ca, arrows=c(T,T), map="rowprincipal")
# However, the directions are the important thing here


# If two row-variables are close on the picture, they have a similar profile,
# the same is true for column-variables

# Distant row/column-variables have different profiles

# Variables distant from the origin represent variables different from the average profile
# these are usually the most interesting ones

# Now you can again try to interpret the dimensions.
# 1st dim splits the sciences into soft/hard
# 2nd dim splits the sciences into more formula heavy(math,physics,engineering) vs
# the more experimental ones (chemistry,agriculture,earthsciences)

# same for different years


# You can also try this:
plot3d.ca(SD.ca)

i=0;
sum((SD.ca$rowdist)<1)
sum((SD.ca$rowdist)>1 & (SD.ca$rowdist)<1.3)

sum((SD.ca$rowdist)<1.5 &(SD.ca$rowdist)>1.3)

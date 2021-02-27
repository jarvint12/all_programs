setwd("C:/Users/TimoJ/Documents/Yliopisto/Maisteri/Multivariate Statistical Analysis/week5")

data <- read.table("SMOKING.txt", header=T, row.names=1)

data <- data[-nrow(data), -ncol(data)]

D <- as.matrix(data)

prob_table<-prop.table(D)
prob_table


marginal_rows<-prop.table(D,1) #Conditional frequencies rows
marginal_rows
marginal_cols<-prop.table(D,2) #Conditional frequencies columns
marginal_cols


## Homework 1a
rowsums<-margin.table(D,1) #rowsums
colsums<-margin.table(D,2) #colsums

rowsum_matrix<-matrix(rowsums,ncol=1) 
colsum_matrix<-matrix(colsums,nrow=1) 

E <- rowsum_matrix %*% colsum_matrix /sum(D) #the theoretical relative frequencies under independence
E

## Homework 1b
# Attraction repulsion matrix is got from dividing real values with expected
atr_rep_matrix<-D/E

## Homework 1c, is the smoking more frequent among a specific group in this company
# It seems like there is more heavy smokers in junior management and senior management compared to the theoretical values. In addition, junior manager have many 
#medium smokers, while non smokers are more rare. Senior managers have non smokers too.
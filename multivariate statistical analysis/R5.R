
setwd("C:/Users/TimoJ/Documents/Yliopisto/Maisteri/Multivariate Statistical Analysis/week5")

data <- read.table("SCIENCEDOCTORATES.txt",header=T,row.names=1)

dim(data)

S <- data[-13,-9] #remove the total col/row

View(S)

class(S)

D <- S

D <- as.matrix(S)


# prob table wants a matrix
# A <- as.matrix(A)

prop.table(D) # table of relative frequencies

prop.table(D,1) #row profiles
prop.table(D,2) #col profiles

rowSums(prop.table(D,1))
colSums(prop.table(D,2))

margin.table(D,1) ###sum of table entries 1 indicate rows
data[,9]

margin.table(D,2)  ###sum of table entries 2 indicate columns
data[13,] 

margin.table(D)
sum(D)

v1 <- margin.table(D,1)
v2 <- margin.table(D,2)

V1 <- matrix(v1,ncol=1) 
V2 <- matrix(v2,nrow=1) 

E <- V1 %*% V2 /sum(D)
AR.matrix <- D/E  #D = original data (number of observations), 
                  #E = expected number of observations under independence

# Values near 1: The year and science are independent
# Values < 1: The science is less frequent in that specific year
# Values > 1: The science is more frequent in that specific year
View(round(AR.matrix,2))

# A nice way to represent the AR-matrix:

library(ggplot2)
library(reshape)

melted <- melt(AR.matrix)
View(melted)
range(melted$value)
ggplot(melted, aes(x=X1, y=X2, fill=value)) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white",
                       midpoint = median(melted$value), limit = c(0.5, 1.55),
                       name="AR value")


###Problem 2 (salary vs education(Lecture example))

data <- read.table("SALARY.txt", header=T, row.names=1)
s <- as.matrix(data)
s
##     B1  B2 B3
## A1 150  40 10
## A2 190 350 60
## A3  10 110 80


F <- prop.table(s)
round(F, 2)
##      B1   B2   B3
## A1 0.15 0.04 0.01
## A2 0.19 0.35 0.06
## A3 0.01 0.11 0.08

rowp <- prop.table(s, 1)
round(rowp, 2)
##      B1   B2   B3
## A1 0.75 0.20 0.05
## A2 0.32 0.58 0.10
## A3 0.05 0.55 0.40
colp <- prop.table(s, 2)
round(colp, 2)
##      B1   B2   B3
## A1 0.43 0.08 0.07
## A2 0.54 0.70 0.40
## A3 0.03 0.22 0.53

#6. Attraction Repulsion Matrix

#    | B1    B2   B3 |  v1
# -------------------|-----
# A1 | 150   40   10 | 200
# A2 | 190  350   60 | 600  
# A3 |  10  110   80 | 200
# -------------------------
# v2 | 350  500  150 | 1000


v1 <- margin.table(s,1)
v2 <- margin.table(s,2)

V1 <- matrix(v1,ncol=1) 
V2 <- matrix(v2,nrow=1) 

E <- V1 %*% V2 /sum(s) # n_{jk}^{*} from above!

# We obtain D simply dividing each n_{jk} by n_{jk}^{*}
D <- s/E

round(D, 2)




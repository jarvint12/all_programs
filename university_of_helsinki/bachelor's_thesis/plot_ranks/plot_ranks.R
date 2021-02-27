ranks <- read.csv("muffinn_oncodrivefm.csv") #or dendrix_oncodrivefm.csv/dendrix_muffinn.csv

ranks2<-ranks[,-1]
ranks3<-ranks2[which(ranks2[,2]<10000),]
ranks3<-ranks3[which(ranks3[,1]<10000),]
rownames(ranks2)<-ranks[,1]

getwd()

i=1
coordinates=vector()
while(i<=length(ranks3[,1])){
  coordinates[i]<-paste(c("(", ranks3[i,2], ",", ranks3[i,1], ")"), collapse = "")
  i=i+1
}

plot(ranks3[,2], ranks3[,1], xlab="Geenin sijoitus Oncodrive-fm:n tuloksissa", ylab="Geenin sijoitus MUFFINNNin tuloksissa", 
     main="Geenien sijoitukset Oncodrive-fm ja MUFFINN", col=ifelse(abs(ranks3[,1]-ranks3[,2])<100, 'red', 'black'))# log="y")
#text(ranks3[,2], ranks3[,1],coordinates,cex=0.5, pos=3, col=ifelse(abs(ranks3[,1]-ranks3[,2])<100, 'red', 'black'))

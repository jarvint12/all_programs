setwd("C:/Users/TimoJ/Documents/Työpaikat/Helsingin Yliopisto/kandi/golden")
getwd()

get_coordinates <- function(given_ranks, x, y){
  i=1
  coordinates=vector()
  while(i<=nrow(given_ranks)){
    coordinates<-paste(c("(", given_ranks[i,x], ",", given_ranks[i,y], ")"), collapse = "")
    i=i+1
  }
  return(coordinates)
}

get_ranks <- function(file, first_lim, second_lim){
  ranks <- read.csv(file, header=FALSE) #or dendrix_oncodrivefm.csv/dendrix_muffinn.csv
  ranks<-ranks[which(ranks[,2]<first_lim),] #Filter first ranks that have too large value
  ranks<-ranks[which(ranks[,3]<second_lim),] #Filter second ranks that have too large value
  rownames(ranks)<-ranks[,1] #Get rownames
  ranks<-ranks[,-1] #Leave gene name out, only two ranks per gene, ranks[1:997,-1] to filter only 997 first ranks
  return(ranks)
}


get_cols <- function(row_num, ranks) {
  cols <- rep("Black",row_num)
  cols[abs(ranks[,1]-ranks[,2])<=100]<-"deeppink"
  cols[abs(ranks[,1]-ranks[,2])<=50]<-"red"
  cols[abs(ranks[,1]-ranks[,2])<=10]<-"blue"
  return(cols)
}


plot_ranks<- function(ranks, x_coord, y_coord, x_name, y_name, cols, gen1, gen2, x_leg1, leg_width, y_leg1, leg_height, pt_cex=1.5, pt_lwd=2, plot_legend)  {
  
  plot(ranks[,x_coord], ranks[,y_coord], xlab=paste0("Geenin sijoitus ",x_name,gen1," tuloksissa"), ylab=paste0("Geenin sijoitus ", y_name,gen2," tuloksissa"), 
       main=paste0("Geenien sijoitukset ",x_name," ja ",y_name), col=cols, cex=1, lwd=2)
  
  if (plot_legend){
    legend(c(x_leg1, x_leg1+leg_width), c(y_leg1,y_leg1+leg_height), title="Etäisyys sijoituksissa", legend=c("<=10", "<=50", "<=100", "100<"), 
           col=c("blue", "red", "deeppink", "black"), cex=1, pch=1, pt.cex=pt_cex, pt.lwd=pt_lwd)
  }
}

dend_onc_ranks<-get_ranks("dendrix_oncodrive.csv",2000,10000)
cols<-get_cols(nrow(dend_onc_ranks), dend_onc_ranks)
par(mfrow=c(1,2))
plot_ranks(dend_onc_ranks, 1, 2, "Dendrix", "Oncodrive-fm", cols, "in", ":n", 14, 15, 188, 80, plot_legend=FALSE)

dend_muf_ranks<-get_ranks("dendrix_muffinn.csv",10000, 23000)
cols<-get_cols(nrow(dend_muf_ranks), dend_muf_ranks)
plot_ranks(dend_muf_ranks, 1, 2, "Dendrix", "MUFFINN", cols, "in", "in", 17, 20, 450, 220, plot_legend=TRUE)


par(mfrow=c(1,2))
muf_onc_ranks <- get_ranks("muffinn_oncodrivefm.csv", 14000, 10300)
cols<-get_cols(nrow(muf_onc_ranks), muf_onc_ranks)
plot_ranks(muf_onc_ranks, 2, 1, "Oncodrive-fm", "MUFFINN", cols, ":n", "in", 20, 155, 8000, 3000, 1, 1, plot_legend=FALSE)

muf_onc_ranks <- get_ranks("muffinn_oncodrivefm.csv", 2000, 10300)
cols<-get_cols(nrow(muf_onc_ranks), muf_onc_ranks)
plot_ranks(muf_onc_ranks, 2, 1, "Oncodrive-fm", "MUFFINN", cols, ":n", "in", 20, 200, 680, 320, plot_legend=TRUE)

#Dendrix has only 38 genes

#muf_onc_ranks <- get_ranks("muffinn_oncodrivefm.csv", 14000, 38)
#cols<-get_cols(nrow(muf_onc_ranks), muf_onc_ranks)
#plot_ranks(muf_onc_ranks, 2, 1, "Oncodrive-fm", "MUFFINN", cols, ":n", "in", 20, 200, 680, 320, plot_legend=TRUE)

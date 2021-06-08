library('reshape2')
library("ggplot2")
library(scales)
library(dplyr)
library(RColorBrewer)
library(gridExtra)

# Rscript /mnt/c/Users/TimoJ/Documents/Atom_projects/hus_git/hus_hematology/Timo/bachelor_thesis/mutation_permutation_tool/mutation_load_coverages_multiple_files.R  /path/to/file.csv /path/to/result.jpg /path/to/result_zoomed.jpg

rm(list=ls())

roundUp <- function(x, freqs=seq(0.1,1,0.1)) { #From https://stackoverflow.com/questions/6461209/how-to-round-up-to-the-nearest-10-or-100-or-x, theforestecologist
  if(length(x) != 1) stop("'x' must be of length 1")
  return(freqs[min(which(freqs>=x))])
}

args <- commandArgs(trailingOnly=TRUE)
jpeg(args[2], width = 1024, height = 1500) #1024, 768, 3072, 
df <- read.csv(args[1])

mycolors <- colorRampPalette(brewer.pal(8, "Paired"))(15)
df <- df %>% group_by(bam_file) %>% mutate(mx = max(cumulative_sum))
df %>% group_by(bam_file) %>%  ggplot(aes(x = factor( bam_file ), y = percent , fill = factor(interval))) +    # print bar chart
  geom_bar( stat = 'identity', aes(reorder(bam_file,-mx),percent)) + 
  ggtitle("CDF of reads covering genomic positions") + theme(text = element_text(size=23)) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1), labels = scales::percent, breaks=seq(0, 1, by = 0.1)) +
  theme(panel.grid.major.x = element_blank(), panel.grid.major.y = element_line( size=.1, color="black" )) + coord_flip() +
  scale_fill_manual(values = mycolors, breaks=c(1, 5, 7, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 500),
                    labels=paste("DP >=", c(1, 5, 7, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 500)), name="Fraction of bases with")
# +ylab("Fraction of genomic positions covered wrt. reference genome") + xlab("Sample ID")
dev.off()

jpeg(args[3], width = 1024, height = 1200)
percent_sum = df %>% group_by(bam_file) %>% summarise(y = sum(percent))
df %>% group_by(bam_file) %>%  ggplot(aes(x = factor( bam_file ), y = percent , fill = factor(interval))) +    # print bar chart
  geom_bar( stat = 'identity', aes(reorder(bam_file,-mx),percent)) + 
  ggtitle("CDF of reads covering genomic positions") + theme(text = element_text(size=23)) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, roundUp(max(percent_sum$y))), labels = scales::percent, breaks=seq(0, 1, by = 0.1)) +
  theme(panel.grid.major.x = element_blank(), panel.grid.major.y = element_line( size=.1, color="black" )) + coord_flip() +
  scale_fill_manual(values = mycolors, breaks=c(1, 5, 7, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 500),
                    labels=paste("DP >=", c(1, 5, 7, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 500)), name="Fraction of bases with")
#+ ylab("Fraction of genomic positions covered wrt. reference genome") + xlab("Sample ID")

dev.off()
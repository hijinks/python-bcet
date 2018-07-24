#!/usr/bin/Rscript

library(methods)
library(grDevices)
library(reshape2)
library(stats)
library(ggplot2)
library(plyr)
library(scales)
library(data.table)
library(gridExtra)
require(grid)
library(lattice)

hp <- read.csv('./data_random/GEE/hanaupah.csv')

d <- data.table(hp)

HPT_ref <- data.frame(Label=d$label, Surface=d$surface, B1=d$B1_BCET, B2=d$B2_BCET, B3=d$B3_BCET, B4=d$B4_BCET, B5=d$B5_BCET, B6=d$B6_BCET, B7=d$B7_BCET)

mean_surface <- aggregate(HPT_ref[,3:9], list(HPT_ref$Surface), mean)
min_surface <- aggregate(HPT_ref[,3:9], list(HPT_ref$Surface), min)
max_surface <- aggregate(HPT_ref[,3:9], list(HPT_ref$Surface), max)

HPT2 <- melt(HPT_ref,id=c("Label", "Surface"), variable.name = "Band")
HPT_mean <- melt(mean_surface,id=c("Group.1"), variable.name = "Band")
HPT_max <- melt(max_surface,id=c("Group.1"), variable.name = "Band")
HPT_min <- melt(min_surface,id=c("Group.1"), variable.name = "Band")

HPT_min_max <- merge(HPT_min, HPT_max, by=c("Band", "Group.1"))
HPT_all <- merge(HPT_min_max, HPT_mean, by=c("Band", "Group.1"))
colnames(HPT_all) <- c("Band", "Surface", "Min", "Max", "Mean")

HPT_all <- merge(HPT_all, HPT2, by=c("Band", "Surface"))

print(HPT_all)

p <- ggplot(HPT_all, aes_string(x='Band',y='Mean', ymax="Max", ymin="Min", group="Surface",colour="Surface")) +
	geom_ribbon(alpha=0.3,aes(fill=Surface),colour=NA,data=HPT_all) +
	geom_line(aes(size=.7)) +
	geom_point(aes_string(x="Band",y="value",group="Label",colour="Surface"),alpha=0.5)+
	geom_point(aes_string(x="Band",y="value",group="Label",colour="Surface"),alpha=0.5)+
	geom_point(aes(size=1)) +
	scale_fill_manual(values=c("red", "green"), name="fill") +
	theme_bw() 

ggsave('./plots/hanaupah.pdf', width = 12, height = 5)




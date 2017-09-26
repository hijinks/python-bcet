#!/usr/bin/Rscript

library(methods)
library(grDevices)
library(reshape2)
library(stats)
library(ggplot2)
library(plyr)
library(scales)
require(grid)

coord_reflectance <- read.csv("./inyo_bcets.csv", header = TRUE, sep=",")

cr = data.frame(x = coord_reflectance$Wavelength, y = coord_reflectance$Reflectance, l = coord_reflectance$Label)

p <- ggplot(cr, aes_string(x = "x", y = "y")) +
	ggtitle("Test") +
	geom_point(aes(colour = l)) +
	theme_bw()
	
ggsave("test.pdf", width = 8, height = 6, dpi = 220)

	
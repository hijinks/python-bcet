#!/usr/bin/Rscript

library(methods)
library(grDevices)
library(reshape2)
library(stats)
library(ggplot2)
library(plyr)
library(scales)
library(data.table)
require(grid)


# No cloud mask
coord_reflectance <- read.csv("./inyo_bcets.csv", header = TRUE, sep=",")

DT <- data.table(coord_reflectance)
DT[DT == "--"] <- NA
DT$Reflectance <- as.numeric(DT$Reflectance) # Make sure reflectance is numerical

band_std <- DT[,.(Reflectance = sd(Reflectance)), by = .(Date, Wavelength,Band)] # Get std of each band

coord_band_std <- DT[,.(Reflectance = sd(Reflectance)), by = .(Label,Wavelength,Band)] # Get std of each band per location
coord_band_std <- dcast(coord_band_std, Label ~ Band , ) # Show std per band per label

# With cloud mask
coord_reflectance_cloud <- read.csv("./inyo_bcets_cloud.csv", header = TRUE, sep=",")

DT_cloud <- data.table(coord_reflectance_cloud)
DT_cloud[DT_cloud == "--"] <- NA
DT_cloud$Reflectance <- as.numeric(DT_cloud$Reflectance) # Make sure reflectance is numerical

band_std_cloud <- DT_cloud[,.(Reflectance = sd(Reflectance)), by = .(Date,Wavelength,Band)]
print(band_std_cloud)


coord_band_std_cloud <- DT_cloud[,.(Reflectance = sd(Reflectance)), by = .(Label,Wavelength,Band)]
print(coord_band_std_cloud)

coord_band_std_cloud <- dcast(coord_band_std_cloud, Label ~ Band , )

for (i in 1:nrow(coord_band_std)){
  x1 <- coord_band_std[i,] # Non cloud reflectance standard deviation
#   x2 <- coord_band_std_cloud[i,] # Cloud masked reflectance standard deviation
#   x1 <- rbind(x1,x2)
  label_name = as.character(x1[1]$Label)
  x1[,c("Label"):=NULL] # Remove label column
  bp <- barplot(as.matrix(x1), ylim = range(0:30))
  png(as.character(label_name))
}

#cr = data.frame(x = coord_reflectance$Wavelength, y = coord_reflectance$Reflectance, l = coord_reflectance$Label)

#p <- ggplot(cr, aes_string(x = "x", y = "y")) +
#	ggtitle("Test") +
#	geom_point(aes(colour = l)) +
#	theme_bw()
	
# ggsave("test.pdf", width = 8, height = 6, dpi = 220)

	

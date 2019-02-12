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

# Python source
c <- read.csv("../data_random/random_python.csv", header = TRUE, sep=",")

DT <- data.table(c)
DT[DT == "--"] <- NA

py_mean <- DT[,.(ref_mean = mean(Reflectance)), by = .(Label,Wavelength,Band)] # Get mean of each band per location
py_mean <- dcast(py_mean, Label ~ Band , ) # Show std per band per label
py_std <- DT[,.(ref_std = sd(Reflectance)), by = .(Label,Wavelength,Band)] # Get std of each band per location
py_std <- dcast(py_std, Label ~ Band , ) # Show std per band per label


# GEE source
d <- read.csv("../data_random/random_gee.csv", header = TRUE, sep=",")

gee_ref <- data.frame(Label=d$label, B1=d$B1_BCET, B2=d$B2_BCET, B3=d$B3_BCET, B4=d$B4_BCET, B5=d$B5_BCET, B6=d$B6_BCET, B7=d$B7_BCET)

ref_comp <- merge(gee_ref, py_mean, by="Label")

bands <- c('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7')
subtitles <- c('Ultra Blue', 'Blue', 'Green', 'Red', 'NIR', 'SWIR 1', 'SWIR 2')
colours <- c('deepskyblue2','dodgerblue3', 'green4', 'red3', 'red4', 'gray63', 'grey24')
lm_eqn = function(df){
    m = lm(y ~ 0 + x, df);
    eq <- substitute(italic(y) == a %.% italic(x)*","~~italic(r)^2~"="~r2, 
         list(a = format(coef(m)[1], digits = 5), 
              b = 0, 
             r2 = format(summary(m)$r.squared, digits = 3)))
    as.character(as.expression(eq));                 
}

i = 1
grobs = c()
for (b in bands){

  df <- data.frame(x=ref_comp[,i+1],y=ref_comp[,i+7+1])
  fit = lm(y ~ 0 + x, df);
  cfs <- coef(fit)
  m <- cfs[[1]]
  conf <- confint(fit, level = 0.99999)
  lwr <- conf[1]
  upr <- conf[2]
  eq <- function(x){x*m}
  lwr_eq <- function(x){x*lwr}
  upr_eq <- function(x){x*upr}
  
  df <- data.frame(x=ref_comp[,i+1],y=ref_comp[,i+7+1])
  grobs[[i]] <- ggplot(df, aes_string(x='x',y='y')) +
	  geom_point(alpha=.15, col=colours[i]) +
	  ylim(low=0,high=200) +
	  xlim(low=0,high=200) +
	  geom_text(x = 80, y = 185, label = lm_eqn(df), parse = TRUE) +
	  stat_function(fun=eq, gem="line", linetype=2) +
      labs(title=paste('Band',i,'-',subtitles[i]), x=expression('DN'['BCET']~'(Composite)'), y=expression('DN'['BCET']~'(GEE)')) +
	  theme_bw()
  ggsave(paste('../plots/random/',b,".pdf", sep=''), width = 4, height = 4, dpi = 220)
  i = i+1
}

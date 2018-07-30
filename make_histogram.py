#!/usr/bin/env python

# BCET Workflow 

__author__ = 'Sam Brooke'
__date__ = 'September 2017'
__copyright__ = '(C) 2017, Sam Brooke'
__email__ = "sbrooke@tuta.io"

import os
import georasters as gr
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser
import fnmatch
import re
from scipy.interpolate import spline

parser = OptionParser()

(options, args) = parser.parse_args()

# args[0] for bcet_directory
# args[1] for no_bcet_directory

bcet_directory = False
no_bcet_directory = False

file_prefix = ''
if os.path.isdir(args[0]):
	bcet_directory = args[0]

if os.path.isdir(args[1]):
	no_bcet_directory = args[1]

bcet_matches = []
for root, dirnames, filenames in os.walk(bcet_directory):
    for filename in fnmatch.filter(filenames, '*.tif'):
        bcet_matches.append(os.path.join(root, filename))

print(bcet_matches)

no_bcet_matches = []
for root, dirnames, filenames in os.walk(no_bcet_directory):
    for filename in fnmatch.filter(filenames, '*.tif'):
        no_bcet_matches.append(os.path.join(root, filename))

print(no_bcet_matches)


output = args[2]
	# Load Raster 

colours = {
	'B1':'lightblue',
	'B2':'blue',
	'B3':'green',
	'B4':'red',
	'B5':'firebrick',
	'B6':'grey',
	'B7':'k'
}

band_labels = {
	'B1':'Band 1 - Ultra Blue',
	'B2':'Band 2 - Blue',
	'B3':'Band 3 - Green',
	'B4':'Band 4 - Red',
	'B5':'Band 5 - NIR',
	'B6':'Band 6 - SWIR 1',
	'B7':'Band 7 - SWIR 2'
}


# Display results
#fig = plt.figure(figsize=(8, 5))
fig, axarr = plt.subplots(2, sharex=False)
width = 25 #cm
height = 20 #cm
fig.set_size_inches(float(width)/2.54, float(height)/2.54)


for ma in no_bcet_matches:
	raster = os.path.join(ma)
	base = os.path.basename(raster)
	m = re.search(r"B[0-9]+",base)
	band_name = m.group()
	ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(raster) # Raster information
	# ndv = no data value
	data = gr.from_file(raster) # Create GeoRaster object
	crs = projection.ExportToProj4() # Create a projection string in proj4 format
	sp = data.raster.ravel()
	spn = len(sp)	
	hist, bins = np.histogram(data.raster.ravel(), bins=50)
	hist_norm = hist.astype(float) / spn 
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	centernew = np.linspace(center.min(),center.max(),300) #300 represents number of points to make between T.min and T.max
	hist_smooth = spline(center,hist_norm,centernew)
	axarr[0].plot(centernew, hist_smooth, color=colours[band_name], label=band_labels[band_name])
	
for ma in bcet_matches:
	raster = os.path.join(ma)
	base = os.path.basename(raster)
	m = re.search(r"B[0-9]+",base)
	band_name = m.group()
	ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(raster) # Raster information
	# ndv = no data value
	data = gr.from_file(raster) # Create GeoRaster object
	crs = projection.ExportToProj4() # Create a projection string in proj4 format
	sp = data.raster.ravel()
	spn = len(sp)
	hist, bins = np.histogram(data.raster.ravel(), bins=25)
	hist_norm = hist.astype(float) / spn 
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	centernew = np.linspace(center.min(),center.max(),300) #300 represents number of points to make between T.min and T.max
	hist_smooth = spline(center,hist_norm,centernew)
	axarr[1].plot(centernew, hist_smooth, color=colours[band_name], label=band_labels[band_name])


axarr[0].set_xlim([0, 25000])
axarr[1].set_xlim([0,255])
axarr[0].set_ylim([0, 0.5])
axarr[1].set_ylim([0, 0.5])
axarr[0].set_xlabel('R')
axarr[1].set_xlabel('R*')
axarr[0].set_ylabel('f')
axarr[1].set_ylabel('f')
axarr[0].set_title('LANDSAT (White Mountains ROI) 2014-02-25 Unmodified Histogram')
axarr[1].set_title('LANDSAT (White Mountains ROI) 2014-02-25 BCET Histogram')
axarr[0].legend()
axarr[1].legend()
plt.savefig('histograms.pdf')


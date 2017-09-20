#!/usr/bin/env python

# BCET Workflow 

__author__ = 'Sam Brooke'
__date__ = 'September 2017'
__copyright__ = '(C) 2017, Sam Brooke'
__email__ = "sbrooke@tuta.io"

import os
from geopandas import GeoDataFrame
from shapely.geometry import Polygon
import georasters as gr
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser
import json
import re

parser = OptionParser()
parser.add_option("-c", "--cloud", dest="cloud", help="Location of cloud raster", metavar="CLOUD")

(options, args) = parser.parse_args()

cloud_tif = False

if options.cloud:
	if os.path.isfile(options.cloud):
		cloud_tif = options.cloud

# args[0] for config file
# args[1] for LANDSAT TIF
# args[2] for file prefix

config_file = False
landsat_raster = False
file_prefix = ''

if len(args) > 1:
	if os.path.isfile(args[0]):
		config_file = args[0]

	if os.path.isfile(args[1]):
		landsat_raster = args[1]

	file_prefix = args[2]


m = re.search(r"B[0-9]+",landsat_raster)
band_name = m.group()

config_data = False
if config_file:
	with open(config_file) as data_file:    
    		config_data = json.load(data_file)


keys = config_data.keys()

# ROI (Region Of Interest) coordinates

roi = False
run_title = 'untitled'
output_dir = './'

if 'roi' in keys:
	top_left = config_data['roi']['top_left']
	bottom_right = config_data['roi']['bottom_right']
	roi = True
	
if 'name' in keys:
	run_title = config_data['name']

if 'output_dir' in keys:
	output_dir = config_data['output_dir']
	
if roi:
# Create Polygon of ROI
	roi_poly = Polygon([(top_left[0], top_left[1]), (bottom_right[0], top_left[1]), (bottom_right[0], bottom_right[1]), (top_left[0], bottom_right[1])])

#
# Load and Process Rasters
#

# Load Raster 
raster = os.path.join(landsat_raster)
ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(raster) # Raster information
# ndv = no data value
data = gr.from_file(raster) # Create GeoRaster object
crs = projection.ExportToProj4() # Create a projection string in proj4 format

if roi:
	print('Clipping ROI')
	# Create GeoDataFrame of ROI polygon with correction projection
	clip_df = GeoDataFrame(crs=crs, geometry=[roi_poly])
	raster_clip = data.clip(clip_df)
	raster_data = raster_clip[0].raster
else:
	raster_data = data.raster

if cloud_tif:
	print('Preparing cloud mask')
	# Cloud mask layer
	# See 
	cloud_mask = os.path.join(cloud_tif)
	cloud_mask_gr = gr.from_file(cloud_mask)  
	cloud_clip = cloud_mask_gr.clip(clip_df)
	cloud_data = cloud_clip[0].raster

# Mask invalid data
raster_masked = np.ma.masked_invalid(raster_data, copy=True)

if cloud_tif:
	print('Running cloud mask')
	# Mask clouds, snow and shadows
	raster_processed = np.where(cloud_data == 1, raster_masked, ndv) 
else:
	raster_processed = raster_masked

#
# BCET algebra
#
print('BCETing')

s = np.mean(np.power(raster_processed,2)) # mean squared
e = np.mean(raster_processed)
l = np.min(raster_processed)
h = np.max(raster_processed)

L = 0 # output minimum
H = 255 # output maximum
E = 110 # output mean


# Find b
b_nom = ((h**2)*(E-L))-(s*(H-L))+((l**2)*(H-E))
b_den = 2*((h*(E-L))-(e*(H-L))+(l*(H-E)))

b = b_nom/b_den

# Find a
a1 = H-L
a2 = h-l
a3 = h+l-(2*b)

a = a1/(a2*a3)

# Find c
c = L-(a*(l-b)**2)

# Process raster
bcet_raster = a*((raster_processed - b)**2) + c

print('New average value:')
print(bcet_raster.mean()) # should be 110!

#
# Output
#

output_gr = gr.GeoRaster(bcet_raster,
     raster_clip[0].geot,
     nodata_value=ndv,
     projection=raster_clip[0].projection,
     datatype=raster_clip[0].datatype)

output_dir_full = os.path.join(output_dir,file_prefix+'_'+run_title)

if not os.path.exists(output_dir_full):
  os.makedirs(output_dir_full)
    
new_path = os.path.join(output_dir_full,run_title+'_'+band_name)
print('Outputing '+new_path+' ...')
# Make Geotiff
output_gr.to_tiff(new_path)



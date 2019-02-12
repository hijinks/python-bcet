#!/usr/bin/env python

# BCET Workflow 

__author__ = 'Sam Brooke'
__date__ = 'September 2017'
__copyright__ = '(C) 2017, Sam Brooke'
__email__ = "sbrooke@tuta.io"

import os
import gdal
from geopandas import GeoDataFrame
from shapely.geometry import Polygon
import georasters as gr
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser
import json
import re

parser = OptionParser()

(options, args) = parser.parse_args()

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

# Mask invalid data
raster_masked = np.ma.masked_invalid(raster_data, copy=True)

output_gr = gr.GeoRaster(raster_masked,
     raster_clip[0].geot,
     nodata_value=ndv,
     projection=raster_clip[0].projection,
     datatype=raster_clip[0].datatype)

output_dir_full = os.path.join(output_dir,file_prefix+'_'+run_title)

if not os.path.exists(output_dir_full):
  os.makedirs(output_dir_full)
    
new_path = os.path.join(output_dir_full,file_prefix+'_'+run_title+'_'+band_name)
print('Outputing '+new_path+' ...')
# Make Geotiff
output_gr.to_tiff(new_path)

# Add some metadata

ds = gdal.Open(new_path+'.tif', gdal.GA_Update)
ds.SetMetadataItem('ORIGINAL_LANDSAT', os.path.basename(landsat_raster))
ds.FlushCache()



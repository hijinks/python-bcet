#!/usr/bin/env python

# Map spectral signature of series of coordinates

__author__ = 'Sam Brooke'
__date__ = 'September 2017'
__copyright__ = '(C) 2017, Sam Brooke'
__email__ = "sbrooke@tuta.io"

import os
import csv
import georasters as gr
from optparse import OptionParser
    
parser = OptionParser()
parser.add_option("-c", "--coords", dest="coords", help="Location of coordinates csv file", metavar="COORDS")
parser.add_option("-d", "--dir", dest="dir", help="Location of coordinates csv file", metavar="DIR")
parser.add_option("-o", "--output", dest="output", help="Output directory", metavar="OUT")
(options, args) = parser.parse_args()

coord_file = False
raster_dir = False
output_dir = False

if options.coords:
	if os.path.isfile(options.coords):
		coord_file = options.coords

if options.dir:
	if os.path.isdir(options.dir):
		raster_dir = options.dir		

if options.output:
	if os.path.isdir(options.output):
		output_dir = options.output		


rasters = []
coordinates = []

with open(coord_file, 'rb') as csvfile:
	firstline = True
	csvr = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in csvr:
		if firstline:    #skip first line
			firstline = False
			continue
		coordinates.append(row)

rasters.append('./output/mojave_bcet_B3.tif.tif')

spectral_data = {}

if len(rasters) > 0 and len(coordinates) > 0:
	
	for r in rasters:
		
		raster_obj = gr.from_file(r)
		ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(r) # Raster information

		band_spectral_data = []
		
		csv_name = os.path.join(output_dir,os.path.basename(r)+'.csv')
		
		with open(csv_name,'wb') as f:
		
			csvw = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			csvw.writerow(projection.ExportToProj4())
    			csvw.writerow(['Label', 'Easting', 'Northing', 'Reflectance'])
			
			for c in coordinates:
				
				rstar = raster_obj.map_pixel(float(c[0]),float(c[1]))
				
				csvw.writerow([c[2], float(c[0]), float(c[1]), rstar])

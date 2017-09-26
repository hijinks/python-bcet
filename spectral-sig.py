#!/usr/bin/env python

# Map spectral signature of series of coordinates

__author__ = 'Sam Brooke'
__date__ = 'September 2017'
__copyright__ = '(C) 2017, Sam Brooke'
__email__ = "sbrooke@tuta.io"

import os
import fnmatch
import csv
import gdal
import georasters as gr
import re
from optparse import OptionParser
from dateutil.parser import parse

parser = OptionParser()
parser.add_option("-c", "--coords", dest="coords", help="Location of coordinates csv file", metavar="COORDS")
parser.add_option("-d", "--dir", dest="dir", help="Search directory", metavar="DIR")
parser.add_option("-o", "--output", dest="output", help="Output directory", metavar="OUT")
parser.add_option("-n", "--csv", dest="name", help="Output csv name", metavar="CSV")

(options, args) = parser.parse_args()

coord_file = False
raster_dir = False
output_dir = './'
csv_name = 'untitled'

if options.coords:
	if os.path.isfile(options.coords):
		coord_file = options.coords

if options.dir:
	if os.path.isdir(options.dir):
		raster_dir = options.dir		

if options.output:
	if os.path.isdir(options.output):
		output_dir = options.output		

if options.name:
	csv_name = options.name		


print('Coord file: '+coord_file)
print('Raster directory: '+raster_dir)
print('Output directory: '+output_dir)
print('CSV Name: '+csv_name)

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



matches = []
for root, dirnames, filenames in os.walk(raster_dir):
    for filename in fnmatch.filter(filenames, '*.tif'):
        rasters.append(os.path.join(root, filename))
        
spectral_data = {}

# Original Landsat Meta
pattern = '^(LC[0-9]+)_(L[0-9a-zA-Z]+)_([0-9]+)_(?P<datestamp>[0-9]+)_([0-9]+)_([0-9]+)_([A-Za-z0-9]+)_(?P<band>B[0-9]+).(tif|TIF)$'
ids = 0

landsat_bands = {
	'B1': [0.435, 0.451],
	'B2': [0.452, 0.512],
	'B3': [0.533, 0.590],
	'B4': [0.636, 0.673],
	'B5': [0.851, 0.879],
	'B6': [1.566, 1.651],
	'B7': [2.107, 2.294]
}

if len(rasters) > 0 and len(coordinates) > 0:

	csv_name = os.path.join(output_dir,csv_name+'.csv')
	
	with open(csv_name,'wb') as f:
		
		csvw = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csvw.writerow(['id', 'Label', 'Easting', 'Northing', 'Reflectance', 'Band', 'Wavelength', 'Date', 'Projection'])
		
		for r in rasters:
			
			raster_obj = gr.from_file(r)
			print(r)
			ds = gdal.Open(r, gdal.GA_Update)
			original_landsat = ds.GetMetadataItem('ORIGINAL_LANDSAT')
			print(original_landsat)
			m = re.match(pattern,original_landsat)
			d = parse(m.group('datestamp'))
			datestamp = d.strftime('%Y-%m-%d')
			band = m.group('band')
			
			ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(r) # Raster information
			
			band_spectral_data = []
			
			wavelengths = landsat_bands[band]
			w = (wavelengths[0]+wavelengths[1])/2 # Get average
			
			for c in coordinates:
				
				rstar = raster_obj.map_pixel(float(c[0]),float(c[1]))
				csvw.writerow([ids,c[2], float(c[0]), float(c[1]), rstar, band, w,  datestamp, '"'+projection.ExportToProj4()+'"'])
				ids = ids+1
				

#!/usr/bin/env python

# Use pixel difference and Kirsch filter to pick series of random points

import georasters as gr
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import random
import string
import csv

diff_gr = gr.from_file('./output/diff.tif')

ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info('./output/diff.tif') # Raster information

edge_gr = gr.from_file('./output/k100.tif')

raster_bounds = diff_gr.bounds

lat_range = np.linspace(raster_bounds[0]+10, raster_bounds[2]-10, num=xsize, endpoint=False, retstep=False, dtype=float)
lon_range = np.linspace(raster_bounds[1]+10, raster_bounds[3]-10, num=ysize, endpoint=False, retstep=False, dtype=float)

npz = np.zeros(diff_gr.raster.shape)

npz[np.where(edge_gr.raster < 1)] = 1
npz[np.where(diff_gr.raster > 20)] = 0

npd = ndimage.binary_erosion(npz, iterations=1)
npd = npd+1

npd[np.where(diff_gr.raster < 1)] = 0

npd_gr = gr.GeoRaster(npd,
                diff_gr.geot,
                nodata_value=ndv,
		projection=diff_gr.projection,
                datatype=diff_gr.datatype)

npd_gr.to_tiff('./npd')

lon_random = np.random.choice(ysize, 20000)
lat_random = np.random.choice(xsize, 20000)

random_coords = np.vstack((lat_random,lon_random)).transpose()
random_coords_unique = np.vstack(tuple(row) for row in random_coords)

def valid_point(v):
	if v > 1:
		return True

i = 0
p = 0

with open('random_points3.csv', 'wb') as csvfile:
	csvw = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	csvw.writerow(['Latitude', 'Longitude', 'Name'])
	while p < 1000:

		coord_r = random_coords_unique[i]
		coord_lat = lat_range[coord_r[0]]
		coord_lon = lon_range[coord_r[1]]
		print([coord_lat,coord_lon])

		if valid_point(npd_gr.map_pixel(coord_lat,coord_lon)):
			label = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			csvw.writerow([coord_lat, coord_lon, label])
			p = p+1
		i = i+1

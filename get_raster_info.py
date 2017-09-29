#!/usr/bin/env python


import georasters as gr
import numpy as np
import matplotlib.pyplot as plt
import random
import string
import csv

diff_gr = gr.from_file('./diff.tif')

ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info('./diff.tif') # Raster information

print(geot)
print('x_cell_size:'+str(geot[1]))
print('y_cell_size:'+str(geot[-1]))
print('xmin:'+str(geot[0]))
print('ymin:'+str(geot[3]))



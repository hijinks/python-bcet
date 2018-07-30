#!/usr/bin/env python

import georasters as gr
import numpy as np
import matplotlib.pyplot as plt
import random
import string
import csv

from scipy import ndimage
from scipy import signal

T1 = r"./output/inyo_bcets/20141108_mojave_bcet/20141108_mojave_bcet_B1.tif"

T1_gr = gr.from_file(T1)
ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(T1) # Raster information

tdata = T1_gr.raster.astype(int)

# Kirsch edge filter operators
k1 = np.array([[5, 5, 5],[-3, 0, -3],[-3, -3, -3]])
k2 = np.array([[5, 5, -3],[5, 0 ,-3],[-3, -3, -3]])
k3 = np.array([[5, -3, -3],[5, 0, -3],[5, -3, -3]])
k4 = np.array([[-3, -3, -3],[5, 0, -3],[5, 5, -3]])
k5 = np.array([[-3, -3, -3],[-3, 0, -3],[5, 5, 5]])
k6 = np.array([[-3, -3, -3],[-3, 0, 5],[-3, 5, 5]])
k7 = np.array([[-3, -3, 5],[-3, 0, 5],[-3, -3, 5]])
k8 = np.array([[-3, 5, 5],[-3, 0, 5],[-3, -3, -3]])

grad1 = signal.convolve2d(tdata, k1, boundary='fill', mode='same', fillvalue=0)
grad2 = signal.convolve2d(tdata, k2, boundary='fill', mode='same', fillvalue=0)
grad3 = signal.convolve2d(tdata, k3, boundary='fill', mode='same', fillvalue=0)
grad4 = signal.convolve2d(tdata, k4, boundary='fill', mode='same', fillvalue=0)
grad5 = signal.convolve2d(tdata, k5, boundary='fill', mode='same', fillvalue=0)
grad6 = signal.convolve2d(tdata, k6, boundary='fill', mode='same', fillvalue=0)
grad7 = signal.convolve2d(tdata, k7, boundary='fill', mode='same', fillvalue=0)
grad8 = signal.convolve2d(tdata, k8, boundary='fill', mode='same', fillvalue=0)

grad = grad1+grad2+grad3+grad4+grad5+grad6+grad7

gstack = np.dstack((grad1,grad2,grad3,grad4,grad5,grad6,grad7,grad8))

gmax = np.apply_along_axis(np.max,axis=2, arr=gstack)
gmax50 = gmax.copy()
gmax100 = gmax.copy()
gmax150 = gmax.copy()
gmax200 = gmax.copy()
gmax250 = gmax.copy()

gmax50[gmax50 < 50] = 0
gmax100[gmax100 < 100] = 0
gmax150[gmax150 < 150] = 0
gmax200[gmax200 < 200] = 0
gmax250[gmax250 < 250] = 0


#grad *= 255.0 / np.max(grad)  # normalize (Q&D)

output_gr = gr.GeoRaster(gmax50,
                T1_gr.geot,
                nodata_value=ndv,
                projection=T1_gr.projection,
                datatype=T1_gr.datatype)

output_gr.to_tiff('./output/k50')

output_gr = gr.GeoRaster(gmax100,
                T1_gr.geot,
                nodata_value=ndv,
                projection=T1_gr.projection,
                datatype=T1_gr.datatype)

output_gr.to_tiff('./output/k100')

output_gr = gr.GeoRaster(gmax150,
                T1_gr.geot,
                nodata_value=ndv,
                projection=T1_gr.projection,
                datatype=T1_gr.datatype)

output_gr.to_tiff('./output/k150')

output_gr = gr.GeoRaster(gmax200,
                T1_gr.geot,
                nodata_value=ndv,
                projection=T1_gr.projection,
                datatype=T1_gr.datatype)

output_gr.to_tiff('./output/k200')

output_gr = gr.GeoRaster(gmax250,
                T1_gr.geot,
                nodata_value=ndv,
                projection=T1_gr.projection,
                datatype=T1_gr.datatype)

output_gr.to_tiff('./output/k250')

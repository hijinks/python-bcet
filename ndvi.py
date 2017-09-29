#!/usr/bin/env python

import georasters as gr
import numpy as np

red_band = r"/data/Spectral-Landsat/python-bcet/output/inyo_bcets/20141108_mojave_bcet/20141108_mojave_bcet_B4.tif"
nir_band = r"/data/Spectral-Landsat/python-bcet/output/inyo_bcets/20141108_mojave_bcet/20141108_mojave_bcet_B5.tif"

r_raster = gr.from_file(red_band) # Create GeoRaster object
n_raster = gr.from_file(nir_band)

ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(red_band) # Raster information

r = r_raster.raster
n = n_raster.raster

ndvi = (n - r)/(n + r)

output_gr = gr.GeoRaster(ndvi,
     r_raster.geot,
     nodata_value = ndv,
     projection=r_raster.projection,
     datatype=r_raster.datatype)

output_gr.to_tiff('./ndvi')


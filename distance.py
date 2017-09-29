#!/usr/bin/env python

import georasters as gr
import numpy as np
import matplotlib.pyplot as plt

T1 = r"./output/inyo_bcets/20141108_mojave_bcet/20141108_mojave_bcet_B1.tif"
T2 = r"./output/inyo_bcets/20140225_mojave_bcet/20140225_mojave_bcet_B1.tif"
T3 = r"./output/inyo_bcets/20151026_mojave_bcet/20151026_mojave_bcet_B1.tif"
T4 = r"./output/inyo_bcets/20160302_mojave_bcet/20160302_mojave_bcet_B1.tif"
T5 = r"./output/inyo_bcets/20160926_mojave_bcet/20160926_mojave_bcet_B1.tif"
T6 = r"./output/inyo_bcets/20170727_mojave_bcet/20170727_mojave_bcet_B1.tif"
T7 = r"./output/inyo_bcets/20170913_mojave_bcet/20170913_mojave_bcet_B1.tif"

T1_gr = gr.from_file(T1)
T2_gr = gr.from_file(T2)
T3_gr = gr.from_file(T3)
T4_gr = gr.from_file(T4)
T5_gr = gr.from_file(T5)
T6_gr = gr.from_file(T6)
T7_gr = gr.from_file(T7)

ndv, xsize, ysize, geot, projection, datatype = gr.get_geo_info(T1) # Raster information

Tstack = np.dstack((T1_gr.raster,T2_gr.raster,T3_gr.raster,T4_gr.raster,T5_gr.raster,T6_gr.raster,T7_gr.raster))

def difference(x):
	return np.max(x)-np.min(x)

Rdiff = np.apply_along_axis(difference,axis=2, arr=Tstack)

output_gr = gr.GeoRaster(Rdiff,
     T1_gr.geot,
     nodata_value=ndv,
     projection=T1_gr.projection,
     datatype=T1_gr.datatype)

output_gr.to_tiff('./diff')








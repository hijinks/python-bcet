# Mask all nodata values in a geotiff

from osgeo import gdal
import os
import glob

source_directory = './LANDSAT8/'
output_directory = './LANDSAT8/'

files = os.path.join(source_directory, '*.TIF')


for fname in glob.glob(files):
    new_name = os.path.basename(fname).replace('.TIF', '')+'_masked.TIF'
    new_path = os.path.join(output_directory, new_name)
    gtiff = gdal.Open(fname)
    gdal.Translate(new_path, gtiff, noData = 0)
    
    

	
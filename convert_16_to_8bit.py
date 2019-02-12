#!/usr/bin/env python

# Convert 16 bit rasters to 8 bit

from optparse import OptionParser
import json
from subprocess import check_output, call


parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help="Input Tiff", metavar="itiff")
parser.add_option("-o", "--output", dest="output", help="Output Tiff", metavar="otiff")
(options, args) = parser.parse_args()


input_raster = options.input
output_raster = options.output

json_info = check_output(["gdalinfo", "-stats", "-json", input_raster])

json_data = json.loads(json_info)

src_max = json_data['bands'][0]['max']
src_min = json_data['bands'][0]['min']

print(json_data)

dst_min = 0
dst_max = 255

scale_str = str(src_min)+' '+str(src_max)+' '+str(dst_min)+' '+str(dst_max)

call(['gdal_translate', '-ot', 'Byte' ,'-of', 'Gtiff' , '-scale', str(src_min), str(src_max), str(dst_min), str(dst_max), input_raster, output_raster])

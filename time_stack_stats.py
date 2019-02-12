import rasterio
import rasterio.mask
import numpy as np
import glob
import os
import re
import cv2
import fiona

# For landsat images

search_dir = './LANDSAT8'

bands = []

fname_reg = 'LC08_L1TP_(?P<d1>[0-9]*?)_(?P<d2>[0-9]*?)_(?P<d3>[0-9]*?)_(?P<d4>[0-9]*?)_T1_(?P<band>B[0-9]*?).TIF'
images = glob.glob(os.path.join(search_dir, '**', '*.TIF'))

band_images = {}

def crop_to_aoi(crop_output, image, aoi_geometry):

	with rasterio.open(image) as source:

		out_meta = source.meta.copy()

		out_image, out_transform = rasterio.mask.mask(source, [aoi_geometry],
													crop=True)
		raster_data = source.read(1)

		out_meta.update({"driver": "GTiff",
			 "height": out_image.shape[1],
			 "width": out_image.shape[2],
			 "transform": out_transform,
			 "nodata": source.nodata,
			 "crs": source.crs})

		raster_data = out_image

		raster_masked = np.ma.masked_invalid(raster_data, copy=True)

		with rasterio.open(crop_output, "w", **out_meta) as dest:
			dest.write(raster_masked)

# Collate images
for i in images:
	im_match = re.match(fname_reg, os.path.basename(i))

	if im_match:

		out = {
			'path': i,
			'd1': im_match.group('d1'),
			'd2': im_match.group('d2'),
			'd3': im_match.group('d3')
		}

		if im_match.group('band') in band_images.keys():
			band_images[im_match.group('band')].append(out)
		else:
			band_images[im_match.group('band')] = [out]


with fiona.open('./boxes/scene_boxes/233073.shp') as aoi:

	aoi_feature = next(iter(aoi))
	aoi_geometry = aoi_feature['geometry']


for v, k in enumerate(band_images):

	current_band = band_images[k]

	band_stack = False

	crop_dir = os.path.join('./cropped', '233073', k)

	if not os.path.exists(crop_dir):
		os.makedirs(crop_dir)

	# for b in current_band:
	# 	print('yo')
		#crop_to_aoi(os.path.join(crop_dir, b['d2']+'.tif'), b['path'], aoi_geometry)

band_subdirs = list(os.walk(os.path.join('./cropped', '233073')))[0][1]
#for b in band_subdirs:
for b in ['B2']:
	b_imgs = glob.glob(os.path.join('./cropped', '233073', b, '*.tif'))

	band_stack = False
	for c in b_imgs:
		with rasterio.open(c) as source:
			band = source.read(1)

			if type(band_stack) is not np.ndarray:
				band_stack = band
				print(band_stack.shape)
			else:
				print(source.read(1).shape)
				band_stack = np.vstack((band_stack,band))

			

# with rasterio.open(image) as source:
#
# 			out_meta = source.meta.copy()
#
# 			out_image, out_transform = rasterio.mask.mask(source, [aoi_geometry],
# 														crop=True)
# 			raster_data = source.read(1)
#
# 			out_meta.update({"driver": "GTiff",
# 							 "height": out_image.shape[1],
# 							 "width": out_image.shape[2],
# 							 "transform": out_transform,
# 							 "nodata": source.nodata,
# 							 "crs": source.crs})
#
# 			raster_data = out_image
#
# 			raster_masked = np.ma.masked_invalid(raster_data, copy=True)
#
# 			with rasterio.open(rcrop_name_path, "w", **out_meta) as dest:
# 				dest.write(raster_masked)
#
#
# print(band_stack.shape)
# exit(1)

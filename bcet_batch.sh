#!/bin/bash -       
#title		:bcet_batch.sh
#description	:Script that preprocesses raw ready-downloaded LANDSAT geotifs
#author		:Sam Brooke
#email		:sbrooke@tuta.io
#
# Usage:
#
#	bash bcet_batch.sh pre_ ./LANDAT8/ 
#

file_prefix=$1 # Prefix to add before all outputted tiff files
landsat_dir=$2 # Directory containing current landsat scene files


# Produce a folder to store all the Fmask images
fmask_path=$landsat_dir'/fmask/' 
mkdir -p $fmask_path

# Workflow 
# 1) A masked set of tiffs with nodata values for extraneous regions of tile
# 2) Cloud, snow and shadow masks using Fmask (http://pythonfmask.org/en/latest/)
# 3) ROI specific BCET normalised geotiffs (http://dx.doi.org/10.1080/01431169108955241)

# Merge Landsat Rasters
echo "Merging LANDSAT rasters ..."
python ./lib/gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o "$fmask_path"ref.img "$landsat_dir"LC08*B[1-7,9].TIF
echo "Merging Thermal LANDSAT rasters"
python ./lib/gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o "$fmask_path"thermal.img "$landsat_dir"LC08*_B1[0,1].TIF


# Run cloud, shadow and snow mask
echo "Making cloud masks ..."
echo "Angles ..."
fmask_usgsLandsatMakeAnglesImage.py -m "$landsat_dir"*_MTL.txt -t "$fmask_path"ref.img -o "$fmask_path"angles.img
echo "Saturation ..."
fmask_usgsLandsatSaturationMask.py -i "$fmask_path"ref.img -m "$landsat_dir"*_MTL.txt -o "$fmask_path"saturationmask.img
echo "TOA ..."
fmask_usgsLandsatTOA.py -i "$fmask_path"ref.img -m "$landsat_dir"*_MTL.txt -z "$fmask_path"angles.img -o "$fmask_path"toa.img
echo "Stacked ..."
fmask_usgsLandsatStacked.py -t "$fmask_path"thermal.img -a "$fmask_path"toa.img -m "$landsat_dir"*_MTL.txt -z "$fmask_path"angles.img -s "$fmask_path"saturationmask.img -o "$fmask_path"cloud.tif


# Produce masked Landsat tiff folder
newpath=$landsat_dir'/masked'
mkdir -p $newpath


# BCET Bands
for f in "$landsat_dir"LC08*B[1-7].TIF
do
	fn=$(basename $f)
	f2=$newpath/$fn
	echo "Masking nodata"
	gdal_translate -of GTiff -a_nodata 0 $f $f2
	echo "BCET processing $f2 ..."
	python2.7 bcet.py ./config.json -c "$fmask_path"cloud.tif $f2 $file_prefix
done

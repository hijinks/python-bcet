#!/bin/bash -       
#title		:bcet_only.sh
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
mask=$3 # Apply cloud mask

if $mask; then
  fmask_path=$landsat_dir'/fmask/' 
  mkdir -p $fmask_path
else
  fmask_path=false
fi

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
	if $fmask_path; then
	  python2.7 bcet.py ./config.json f2 $file_prefix
	else
	  python2.7 bcet.py ./config.json -c "$fmask_path"cloud.tif $f2 $file_prefix
	fi
done

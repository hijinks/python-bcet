#!/bin/bash



# Merge Landsat Rasters
#echo "Merging LANDSAT rasters ..."
#python ./lib/gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o ref.img ./LANDSAT8/LC08*B[1-7,9].TIF
#echo "Merging Thermal LANDSAT rasters"
#python ./lib/gdal_merge.py -separate -of HFA -co COMPRESSED=YES -o thermal.img ./LANDSAT8/LC08*_B1[0,1].TIF


# Run cloud, shadow and snow mask
#echo "Making cloud masks ..."
#echo "Angles ..."
#fmask_usgsLandsatMakeAnglesImage.py -m ./LANDSAT8/*_MTL.txt -t ref.img -o angles.img
#echo "Saturation ..."
#fmask_usgsLandsatSaturationMask.py -i ref.img -m ./LANDSAT8/*_MTL.txt -o saturationmask.img
#echo "TOA ..."
#fmask_usgsLandsatTOA.py -i ref.img -m ./LANDSAT8/*_MTL.txt -z angles.img -o toa.img
#echo "Stacked ..."
#fmask_usgsLandsatStacked.py -t thermal.img -a toa.img -m ./LANDSAT8/*_MTL.txt -z angles.img -s saturationmask.img -o cloud.tif


# Produce masked Landsat tiff folder
newpath='./LANDSAT8/masked'
mkdir -p $newpath


# BCET Bands
for f in ./LANDSAT8/LC08*B[1-7].TIF
do
	fn=$(basename $f)
	f2=$newpath/$fn
	echo "Masking nodata"
	gdal_translate -of GTiff -a_nodata 0 $f $f2
	echo "BCET processing $f2 ..."
	python2.7 bcet.py ./config.json -c ./cloud.tif $f2
done
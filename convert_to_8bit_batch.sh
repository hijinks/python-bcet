#!/bin/bash -
#title		:bcet_only.sh
#description	:Script that preprocesses raw ready-downloaded LANDSAT geotifs
#author		:Sam Brooke
#email		:sbrooke@tuta.io
#
# Usage:
#
#	bash convert_to_8bit_batch.sh ./LANDSAT8/ ./LANDSAT8/8bit/
#

input_directory=$1
output_directory=$2

mkdir -p $output_directory

# BCET Bands
for f in "$input_directory"LC08*B[1-7].TIF
do
	fn=$(basename $f)
	f2=$output_directory$fn
	echo "Exporting as 8 bit"
	python convert_16_to_8bit.py -i $f -o $f2
done

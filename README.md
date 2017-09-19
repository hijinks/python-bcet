# python-bcet
Preprocess using the Fmask algorithm & Balance Constrast Enhance Technique LANDSAT 8 Geotiffs for spectral analysis

## Purpose
These scripts are used to preprocess and contrast enhance [LANDSAT 8 OLI & TIRS](https://lta.cr.usgs.gov/L8) geotiffs using the cloud, snow and shadow Fmask algorithm (Zhu, Z., Wang, S. and Woodcock, C.E., 2015) and the BCET algorithm (Liu, J.G., 1991).

With a user-specified region of interest (ROI) within the Landsat scene, each Landsat bands 1-7 will have histogram shapes conserved but with an adjusted range of 0-255 with mean intensity of 110. Doing so enables the normalised comparison of spectral signatures within the BCETed scene across each band.

### Workflow
1) Generate a masked set of tiffs to remove areas of nodata (useful with oblique LANDSAT tiles)
2) Cloud, snow and shadow masks using Fmask (http://pythonfmask.org/en/latest/)
3) Produce band-specfic ROI BCET normalised geotiffs (http://dx.doi.org/10.1080/01431169108955241)

## Requirements
Preprossing scripts require the follows scripts and their dependencies in the path:

The [GDAL](http://www.gdal.org/) library.

Including ...
- [gdal_merge.py](http://www.gdal.org/gdal_merge.html)

From [Fmask](http://pythonfmask.org/en/latest/) ...
- fmask_usgsLandsatMakeAnglesImage.py
- fmask_usgsLandsatSaturationMask.py
- fmask_usgsLandsatStacked.py
- fmask_usgsLandsatTOA.py

Python scripts require the following and their dependencies ...
- python 2.7.11+
- numpy
- matplotlib
- [RIOS](http://rios-test.readthedocs.io/en/latest/)
- [georasters 0.57](https://github.com/ozak/georasters)


## Usage
- Download a LANDSAT scene tifs and metadata and extract into LANDSAT8 directory ([like this](https://github.com/hijinks/python-bcet/blob/master/LANDSAT8/.keep)) 
- Set output, name and ROI (UTM coordinates) in [config](https://github.com/hijinks/python-bcet/blob/master/config.json)
- Preprocess and run BCET algorithm on geotiffs with [bcet_batch.sh](https://github.com/hijinks/python-bcet/blob/master/bcet_batch.sh)

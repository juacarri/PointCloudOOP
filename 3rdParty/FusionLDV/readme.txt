FUSION 3.80
August 2018

Version 3.80 Changes
Minor changes to several programs. Changes to AreaProcessor to improve performance of processing runs and added output of shapefiles showing the 
extent of the ground models and return density files used for a run. Fixed some logic in TreeSeg that clipped points in overlapping objects. Corrected
a problem in some programs that incorrectly computed the extent of data when all XY coordinate values were negative.

Version 3.70 Changes
Updated LAS file handling to fully support LAS Version 1.4 files with or without the laszip.dll. Previous versions could read LAS v1.4 using the dll
but could not write V1.4 files. This release fully supports reading and writing of v1.4 files.

Modified the TreeSeg utility to handle point data and output separate point files for every object identified in the segmentation. This allows
calculation of the full suite of FUSION metrics for individual tree objects.

Updated AreaProcessor and related programs to better monitor the status of a run. This has been an on-going challenge since the development of 
LTKProcessor. The changes in this release seem to work well even when using more than 16 cores for processing.

This distribution includes a manual that describes some of the basic operations in FUSION and the 
command line utilities. Online tutorials are available from the Forest Service Geospatial Technology 
and Applications Center (GTAC) (http://www.fs.fed.us/eng/rsac/). The tutorials cover basic operations and describe a 
variety of analysis and data processing that can be accomplished with FUSION and LTK.

The primary FUSION website is:
http://forsys.sefs.uw.edu/fusion.html

The latest version of FUSION is always available at:
http://forsys.sefs.uw.edu/fusion/fusionlatest.html

You can check for newer versions of FUSION by accessing the Help…About menu option in FUSION and 
clicking the button labeled “Check for a newer version of FUSION”. This action will open a web page on 
the FUSION server that will indicate if the version of FUSION you have is the “latest version” and provide 
a link to the latest version of both the FUSION software and the manual.

I hope you find the software interesting and useful.  If you have questions or need assistance, call or 
email me.


Bob McGaughey
RESEARCH FORESTER
USDA Forest Service
University of Washington
PO Box 352100
Seattle, WA  98195-2100
(206) 543-4713
bmcgaughey@fs.fed.us

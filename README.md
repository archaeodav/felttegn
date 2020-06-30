# FeltTegn
Public repository for FeltTegn, a Qgis Plugin for processing survey data from archaeological excavations conducted by Danish Museums.

Replicates functionality of the MapDigi plugin for MapInfo used by many museums to create polygons and other geometries from total station / GNSS points.

## How to install
Download the zip file release from github.com/archaeodav/felttegn/releases and in the top menu of Qgis choose *'plugins>manage and install plugins'* and choose *'Install from ZIP'* in the sidebar on the left

*(Note: we hope to get this into the QGIS repositories soon, so this should be much easier in the near future)*

## Reporting problems
Please either report issues on GitHub or by email

## Compatability 
We're testing on Qgis 3.10 and later

## Known issues:
 - Tabfile output is blocky as we need to set the extents properly.
 - Features not assigned unique attributes in the csv will have random garbage inserted instead
 

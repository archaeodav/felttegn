# FeltTegn
Public repository for FeltTegn, a Qgis Plugin for processing survey data from archaeological excavations conducted by Danish Museums.

Replicates functionality of the MapDigi plugin for MapInfo used by many museums to create polygons and other geometries from total station / GNSS points.

## How to install
Avialable through the Qgis repositories as an experimental plugin (you have to enable experimental plugins in settings)

This is will only be updated afeter testing of significant updates- to get the most recent version please download the zip file release from github.com/archaeodav/felttegn/releases and in the top menu of Qgis choose *'plugins>manage and install plugins'* and choose *'Install from ZIP'* in the sidebar on the left


## Reporting problems
Please either report issues on GitHub or by email

## Compatability 
We're testing on Qgis 3.10 and later. It works on earlier versions, but htere are some errors / unexpected behaviours

## Known issues:
 - Features not assigned unique attributes in the csv will have random garbage inserted instead. This goes for double numbering too.
 - Error reporting is a work in progress. Currently no 'Fejl' layer is produced.
 

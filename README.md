# FeltTegn
Public repository for FeltTegn, a Qgis Plugin for processing survey data from archaeological excavations conducted by Danish Museums.

Replicates and extends functionality of the MapDigi plugin for MapInfo used by many museums to create polygons and other geometries from total station / GNSS points.

## How to install
Avialable through the Qgis repositories as an experimental plugin (you have to enable experimental plugins in settings)

This is will only be updated afeter testing of significant updates- to get the most recent version please download the zip file release from github.com/archaeodav/felttegn/releases and in the top menu of Qgis choose *'plugins>manage and install plugins'* and choose *'Install from ZIP'* in the sidebar on the left


## Reporting problems
Please report issues on GitHub rather than by email. It's also very helpful if you can include the import text file as we need examples.

## Compatability 
We're testing on Qgis 3.10 and later. It works on earlier versions, but there may be some errors / unexpected behaviours

## Known issues:
 - Sometimes (on windows) the plugin won't overwrite a file of the same name if it's loaded in QGIS. This is apparently a quirk of the underlying OSGEO library
 

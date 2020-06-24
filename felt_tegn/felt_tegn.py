# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FeltTegn
                                 A QGIS plugin
 Plugin makes polys from oints
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Arkæologisk IT
        email                : ds@moesgaardmuseum.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtCore import QVariant

from qgis.gui import QgsFileWidget, QgsProjectionSelectionWidget

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .felt_tegn_dialog import FeltTegnDialog
import os.path

import os
import csv

from qgis.core import (
  QgsFields,
  QgsGeometry,
  QgsPoint,
  QgsPointXY,
  QgsWkbTypes,
  QgsFeatureRequest,
  QgsDistanceArea,
  QgsPolygon,
  QgsField,
  QgsVectorFileWriter,
  QgsFeature,
  QgsVectorLayer,
  Qgis,
  QgsProject,
  QgsCoordinateReferenceSystem)

class FeltTegn:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FeltTegn_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&FeltTegn')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FeltTegn', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/felt_tegn/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'take gps points make polys'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&FeltTegn'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = FeltTegnDialog()

        ifile = self.dlg.inputTextFile
            
        ifile.setStorageMode(QgsFileWidget.GetFile)
        
        #TODO constrain to txt / csv....
            
        odir = self.dlg.outputTargetDir
            
        odir.setStorageMode(QgsFileWidget.GetDirectory)
            
        proj = self.dlg.mQgsProjectionSelectionWidget
        
        proj.setCrs(QgsCoordinateReferenceSystem("EPSG:25832"))
        
        # show the dialog
        self.dlg.show()
        
        # Run the dialog event loop
        result = self.dlg.exec_()
       
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
           
            shp = self.dlg.radioButton_shp.isChecked()
            tab = self.dlg.radioButton_tab.isChecked()
            gp = self.dlg.radioButton_gp.isChecked()
            gjson = self.dlg.radioButton_gjson.isChecked()
            
            add_files = self.dlg.chk_addfiles.isChecked()

            print ('infile:', 
                   ifile.filePath(),
                   'outfile:',
                   odir.filePath(),
                   'proj:',
                   proj.crs().authid(),
                   shp,
                   tab,
                   gp,
                   gjson)
            
            print (type(proj.crs().authid()))
            
            print (proj.crs().authid())
            
            digit = Digi([ifile.filePath()])
            
            out_layers = digit.feat_export(odir.filePath(),
                                           srs=proj.crs(),
                                           shp=shp,
                                           tab=tab,
                                           gp=gp,
                                           gjson=gjson)
            
            if add_files is True:
                for l in out_layers:
                    ol = QgsVectorLayer(l,os.path.split(l)[-1].split('.')[0],"ogr")
                    QgsProject.instance().addMapLayer(ol)
            else:
                out_layers
                        
class LoadData():
    """ Class to load data from a csv file"""
    def __init__(self,
                 default_codes = True, #TODO Look for an external code file?
                 codefile = None #TODO path to codefile
                 ):
        
        """List to contain data values"""
        self.data=[]
        
        """Codes for feature types"""
        self.codes = {}
               
        self.feats_1st_pass = {}
        
        self.feats_2nd_pass = {}
        
        self.layers = {}
        
        self.errors =[]
              
        """Use default codes? if so set self.codes to use default ardigi codes.
        these are deifned as a dict with the following attributes:
             key - text string identifying code
             ...sub dict keys... 
            - lcode : if not none first letter of sting indicates point / feature.
                      e.g. A1 = Anlæg, X1= Find etc.
            - layer : output layer name to append features to
            - type : geometric type object passed to Digi class. these are:
                    poly : polygon
                    zpoly : zigzag polygon
                    upoly : delete this from intersecting polgons
                    point : point
                    pline : polyline
             - pass : what stage in the iterator are these taken in?:
                 1st pass- big trenches, fyldskift etc where people stop &
                 record anlæg etc in the middle
                 2nd pass- all the normal stuff"""
                    
        if default_codes is True:
             
            self.codes={"-ANLG":{"lcode":"A","layer":"Anlæg","type":"poly","pass":2},
                        "-ZZANLG":{"lcode":None,"layer":"Anlæg","type":"zpoly","pass":2},
                        "-ZZANLAEG":{"lcode":None,"layer":"Anlæg","type":"zpoly","pass":2},
                        "-FYLDSKIFTE":{"lcode":None,"layer":"Anlæg","type":"poly","pass":1},
                        "-PROFIL":{"lcode":None,"layer":"Anlæg","type":"poly","pass":2},
                        "-VAND":{"lcode":None,"layer":"Anlæg","type":"poly","pass":2},
                        "-FELT1":{"lcode":"F","layer":"Felt","type":"zpoly","pass":1},
                        "-FELT2":{"lcode":None,"layer":"Felt","type":"poly","pass":2},
                        "-FELTUD":{"lcode":None,"layer":"U_Felt","type":"upoly","pass":2},
                        "-NIVEAU":{"lcode":None,"layer":"Snit","type":"pline","pass":2},
                        "-SNIT":{"lcode":None,"layer":"Snit","type":"pline","pass":2},
                        "-MAALEPKT":{"lcode":"M","layer":"Målepunkter","type":"point","pass":2},
                        "-PROEVE":{"lcode":"P","layer":"Prøver","type":"point","pass":2},
                        "-FUND":{"lcode":"X","layer":"Fund","type":"point","pass":2},
                        "-KOTE":{"lcode":None,"layer":"Kote","type":"point","pass":2},
                        "-BUNDKOTE":{"lcode":None,"layer":"Kote","type":"point","pass":2},
                        "-LAG":{"lcode":"L","layer":"Lag","type":"poly","pass":2},
                        "-MANUELT":{"lcode":None,"layer":"Fejl","type":"point","pass":2}}
            
            # loop through codes to check if they have aliases
            lcodes = {}
            
            for k in self.codes.keys():
                #print (k)
                if not self.codes[k]["lcode"] is None:
                    # if they do add the code info under the alias
                    lcodes[self.codes[k]["lcode"]]=self.codes[k]
                    
                   
            for d in (lcodes):
                self.codes.update(lcodes)
                
                    
            

        else:
            ''' load code definitons from a json file. this is extra functionality 
            to be added in a bit '''
            #TODO load codefile
            
            #TODO
            '''  idea note:
                use 3rd pass to do stones wood and other materials in anlæg by 
                cutting them out of anlæg polys. Also, do edge types and such
                by snapping to vertices of poly and extracting pline between
                vertices'''
            
            pass
            
    
        
    
    def parsefile(self,
                  infile, # path to source file inluding path #TODO from GUI
                  delimiter=',', # delimiter
                  xidx=0, # index for x column in source file
                  yidx=1, # index for y column in source file
                  zidx=2, # index for z column in source file
                  ididx=3, # index for point id
                  kidx=4, # index for arkdigi code
                  nidx=5, # index for notes field
                  proj = None, # TODO handle projections from GUI
                  ):
        """
        method loads and parses file
        """
        
        unique = True
        
        #open file and iterate over lines
        with open(infile, 'r') as i:
            
            r = csv.reader(i,delimiter=delimiter)
            # restructure if needed based on args
            for row in r:
                if len(row)>0:
                    x = row[xidx]
                    y=row[yidx]
                    z=row[zidx]
                    idid =row[ididx]
                    k = row[kidx]
                    
                    #append to self.data
                    self.data.append([x,y,z,idid,k])
        # set counter
        i = 0
        
        # set up list to hold points related to feature
        current = []
        
        #loop over data
        
        l = len(self.data)
        
        for r in self.data:
            #set feature id
            fid = None
            
            #temp feature id
            #tfid = None
            
            #set point code
            kote = None
            #set attribute
            attr = None
            
            unique = True
            
            #if line starts with a dash it's a standard code...
            if r[4][0] == '-':
                
                #check for first delimiter cos people do different things 
                space = r[4].find(' ')
                
                dot = r[4].find('.')
                
                delim = None
                
                
                # find out how it's delimited
                if dot == -1 and space == -1:
                     kote = r[4]
                     
                elif dot == -1 and space > 0:
                    delim = space
                    
                elif dot > 0 and space ==-1:
                    delim = dot
                    
                elif dot>0 and space>0:
                    
                    if dot < space:
                        delim = dot
                        
                    else:
                        delim = space
                
                # slice accordingly        
                if not delim is None:
                    if not delim == len(r)-1:
                        kote = r[4][:delim]
                        fid = r[4][delim+1:]
                    else:
                        kote = r[4]
                else:
                    kote = r[4]
                    '''fall-back condition is just to take these into the code
                    if it's wrong it will get picked up by error handling when we
                    get the code'''

                if not fid is None:
                    '''split off attributes from id'''    
                    if '.' in fid:
                        fid_l = fid.split('.')
                        
                        fid = fid_l[0]
                        
                        if len(fid_l)>2:
                            attr = ' '.join(fid_l[1:])
                        
                        else:
                            attr = fid_l[-1]
                
                    
            # else the code is probably denoted by the fist letter            
            else:
                kote =r[4][0]
                
                #assign attribute if it's htere
                if '.' in r[4]:
                    fid, attr = r[4].split('.')
                
                # if it's not the feature id is the feature id
                else:
                    fid = r[4]
            
            
            if fid is None:
                
                unique = False
                
                if len(current)==0:
                    #tfid = "%s_%s" %(kote,r[3])
                    tfid = "%s" %(r[3])
                fid = tfid
              
              
            # check if code is in our code list
            if kote.upper() in self.codes.keys():
                #if so retrieve code from code list
                code = self.codes[kote.upper()]
                
                # get the appropriate layer from the code list
                layer = code["layer"]
                                               
                # if it's not in our list of layers create it pronto- we'll need it later
                if not layer in self.layers.keys():
                    self.layers[layer]={'type':code["type"]}
                    
                # append the current geometry to current feature
                current.append([float(r[0]),float(r[1]),float(r[2]),r[3]])
                
                
                
                # check this feature against the next in the list
                # if it's different we're done with this feature
               
                last_pt = False
                                    
                if not i==l-1:
                    if self.data[i+1][4] != r[4]:
                        last_pt = True
                else:
                    last_pt = True
                    
                if last_pt is True:                    
                    # ... unless it's a first pass feature
                    if code["pass"] == 1:
                        # I don't trust the feature ids from these to be unique
                        
                        feat_id = "%s_%s" %(kote, fid)
                        #feat_id = "%s" %(kote)
                        # check to see if this is a new feature or a contiuation
                        if not feat_id in self.feats_1st_pass.keys():
                            #if it's new make it
                            self.feats_1st_pass[feat_id]={}
                            self.feats_1st_pass[feat_id]["code"]=code
                            self.feats_1st_pass[feat_id]["points"]=current
                        else:
                            #if it's not new add the points to the existing feature
                            for c in current:
                                self.feats_1st_pass[feat_id]["points"].append(c)
                        #create and add attributes for feature        
                        self.feats_1st_pass[feat_id]["attr"]=attr
                    else:
                        # if this is a second pass feature create it
                        # check first to see if it has a unique id- stones etc don't
                        #print ("2 PASS")
                        #print (fid,current,code)
                        if not fid in self.feats_2nd_pass.keys():
                           
                            self.feats_2nd_pass[fid] = {}
                            self.feats_2nd_pass[fid]["points"]=current
                        
                        #elif unique is False:
                        else:
                            print ("*UNIQUEunique")
                            #if it disnae make an id from the point ids
                            print ('FID NOT UNIQUE', fid)
                            fid = "%s_%s" %(kote, current[0][3])
                            
                            print ('FID NOT UNIQUE', fid)
                            self.feats_2nd_pass[fid] = {}
                            self.feats_2nd_pass[fid]["points"]=current
                        
                        # add code info and attributes    
                        self.feats_2nd_pass[fid]["code"]=code
                        self.feats_2nd_pass[fid]["attr"]=attr
                    # reset current feature cos we're on to the next
                    current = []
            
            # if we can't find the code append to errors
            # TODO- handle this much betterer- add an error collection method
            else:
                #print('ERROR',r)
                self.errors.append(r)
                
            
            
            # increment the counter cos we done here
            i =i+1
        print ("Errors", self.errors)
        #print (self.feats_2nd_pass)
            
class Digi():
    """ 
    Class digtitises layers from points. 
    Seperate methods handle each type of feature to be digitised
    """
    
    def __init__(self, 
                 infiles, #list of csv files to load
                 split_files=True, #convert as seperate files or homogenise
                 case_delimiter = '_' # delimiter used in case- eg FHM12345_blah.csv
                 ):
        
        # The layers we'll actually use
        self.layers = None
        
        # an empty dict to hold the features
        self.features = {}
        
        self.fname = None
        
        self.errors=[]
        
        if split_files is True:
            for f in infiles:
                indata = LoadData()
                indata.parsefile(f)
                
                self.layers = indata.layers
                
                
                for d in (indata.feats_1st_pass,indata.feats_2nd_pass): 
                    self.features.update(d) 
                    
                    
                    
                if len(os.path.split(f)[-1])>2:
                    self.fname = '_'.join(os.path.split(f)[-1].split('.')[0:-1])
                
                else:
                    self.fname=os.path.split(f)[-1].split('.')[0]
                
                self.fname = self.fname.replace(' ', '_')
                
                self.feature_builder()
                
            
        # TODO make this work- same as above but user must supply filename?
        else:
            indata = LoadData()
            for f in infiles:
                indata.parsefile(f)
                
            self.layers = indata.layers
            for d in (indata.feats_1st_pass,indata.feats_2nd_pass): 
                self.features.update(d) 
                
        
                
        
    def feature_builder(self):

        for feat in self.features:
 
            f = self.features[feat]
            
            pts = []
            
            for pt in f["points"]:
                
                pts.append(QgsPointXY(pt[0],pt[1])) 
            
            tp = f["code"]["type"]
            
            l = f["code"]["layer"]
            
            attr = f["attr"]
            
            geom = None
            
            if tp == "poly":
                if len(pts)>2:
                    geom = self.point2poly(pts)
                elif len(pts)==2:
                    geom = self.twopointpoly(pts)
                else:
                    #todo handle error nicely
                    pass
            
            elif tp == "zpoly":
                geom = self.zzpoly(pts)
                
            elif tp == "point":
                geom = self.point2point(pts)
                  
            elif tp == "pline":
                geom = self.point2pline(pts)
                
            elif tp == "upoly":
                geom = self.upoly(pts)
                #TODO not implemented!
                
            if not l in self.layers:
                self.layers[l]={}
                
            
            self.layers[l][feat]={"geom":geom,"attr":attr}
                                
                  
    def feat_export(self, 
                    odir, 
                    srs, 
                    shp=True,
                    tab=False,
                    gp=False,
                    gjson=False):
                
        dr_n = None
        
        dr_ext =None
        
        o_list = []
        
        if shp is True:
            dr_n = "ESRI Shapefile"
            dr_ext=".shp"
        
        elif tab is True:
            #dr_n = "MITAB"
            '''Note- MITAB doesn't work as driver name, although according to
            docs it should. Works now with "Mapinfo File" for whatever reason. 
            I don't know either'''
            dr_n = "Mapinfo File"
            dr_ext=".tab"
        
        elif gp is True:
            dr_n = "GPKG"
            dr_ext=".gpkg"
        
        elif gjson is True:
            dr_n = "GeoJSON"
            dr_ext=".geojson"
    
        else:
            pass

              
        for l in self.layers:
                       
            name = "%s_%s" %(self.fname,l)
            
            ofname = os.path.join(odir,name+dr_ext)
            
                        
            fields = QgsFields()
            fields.append(QgsField("Nr", QVariant.String))
            fields.append(QgsField("Notes", QVariant.String))
            
            if self.layers[l]['type']=='point':
                gt=QgsWkbTypes.Point
                gt = "Point"
                
                        
            elif self.layers[l]['type']=='pline':
                gt=QgsWkbTypes.LineString
                gt = "LineString"
                        
            elif self.layers[l]['type']== 'poly' or self.layers[l]['type']=='zpoly':
                gt=QgsWkbTypes.Polygon
                gt = "Polygon"
                    
            #this is fucking retarded
            gt = "%s?crs=%s" % (gt,srs.authid())  
                
            tmp_layer = QgsVectorLayer(gt, "temp_layer", "memory") 
            
                        
            pr = tmp_layer.dataProvider()
            
            pr.addAttributes(fields)
            tmp_layer.updateFields()
            
            for feat in self.layers[l].keys():
                #print (feat)
                if feat != 'type' and feat !='attr':
                    fet = QgsFeature()
                    #print(self.layers[l][feat]["geom"],type(self.layers[l][feat]["geom"]))
                    fet.setGeometry(self.layers[l][feat]["geom"])
                    fet.setAttributes([feat, self.layers[l][feat]["attr"]])
                    #print (fet.geometry(),fet.attributes())
                    pr.addFeatures([fet])
                    tmp_layer.updateExtents()

            
            transform_context = QgsProject.instance().transformContext()
            save_options = QgsVectorFileWriter.SaveVectorOptions()
            save_options.driverName = dr_n
            save_options.fileEncoding = "UTF-8"
            save_options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
            
            q_version =int(Qgis.QGIS_VERSION.split('.')[1])
            
            if q_version >= 12:
                error = QgsVectorFileWriter.writeAsVectorFormatV2(tmp_layer,
                                                                   ofname,
                                                                   transform_context,
                                                                   save_options)
                
            else:
                error = QgsVectorFileWriter.writeAsVectorFormatV2(tmp_layer,
                                                                   ofname,
                                                                   transform_context,
                                                                   save_options)
                                                                  
                        
            if error[0] == QgsVectorFileWriter.NoError:
                print("success!")
            else:
                print(error)
                
            del error
            del tmp_layer
            
            o_list.append(ofname)
            
        return o_list
       
        
    #******************** GENERIC METHODS *************************************
    
    def point2poly(self,points):
        """ internal method to take geometry and spit out a polygon """
        
        #print ('PTS', type(points), points)
    

        ring = QgsGeometry.fromPolygonXY([points])     
        
        #print ('RING', ring)
            
        return ring
    
    def point2pline(self,points):
        """ internal method to take geometry and spit out a polyline """
        
        ln = QgsGeometry.fromPolylineXY(points)
        
        return ln
    
    def point2point(self,point):
       
        p1 = QgsGeometry.fromPointXY(point[0])
        
        return p1
    
    def splitpoly(self,feature_list):
        """ 
        method to cut out and split intersecting polygons
        """
        blah = 'blah'
        return blah
    
    def upoly(self,feature_list):
        """ 
        method to cut out bits of polys
        """
        blah = 'blah'
        return blah
    
    
    def zzpoly(self,points):
        """
        method for digitising polygons on long linear features such as trial
        trenches and drains in a 'zigzag' order.
        take points as list, then re-order alternating points by taking the left 
        and right sides by splitting the ist of points into odd and even indices, 
        then reversing the order of the evens and rejoining the two lists forming 
        a ring.
        """
               
        # extract the odd and even points from the list. 
        odds = points[0::2]
        
        evens = points[1::2]
        
        evens.reverse()
        
        pts = odds + evens
        
        poly = self.point2poly(pts)
        
        return poly
        
    def twopointpoly(self,points):
        """
        method spits out a circle from two points on perimiter of feature. 
        """
        
        ln = self.point2pline(points)
        
        #print (ln)
        
        d = ln.length()/2
        
        #c = ln.centroid().asPoint()
        c = ln.centroid()
        
        #print (c, c.type(), "!TWO POINT!")
        
        poly = c.buffer(d,25)
        
        return poly
 
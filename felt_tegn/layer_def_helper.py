#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 14:12:29 2022

@author: dav
"""


import os
import json



file = os.path.dirname(__file__)

class LayerDef():
    def __init__(self,
                 infile=None):
        
        if infile is None:
            infile = os.path.join(file,'layer_definition.json')
            
        self.infile = infile
            
        if not os.path.exists(infile) and not os.path.isfile(infile):
            raise Exception('No layer defintion file found')
            
        else:
            with open(infile, 'r') as ifile:
                self.defs = json.load(ifile)
                
                
    def save_defs(self,
                  outfile = None,
                  overwrite = True):
        
        if outfile is None and overwrite is False:
            raise Exception('You need to specifiy an output file or enable overwrite')
            
        elif outfile is None and overwrite is True:
            outfile = self.infile
        
        with open(outfile, 'w') as ofile:
            json.dump(self.defs,
                      ofile,
                      sort_keys=True,
                      indent=4,
                      ensure_ascii=False)
            
            ofile.close()
            
    def add_field(self,
                  target_layer=None,
                  target_museum = 'default',
                  all_layers = True,
                  alias_tuple=None,
                  field_defn=None):
    
        if alias_tuple is None or field_defn is None:
            raise Exception("You haven't defined fields or aliases")
            
        if target_layer is None and all_layers is False:
            raise Exception("No target layer")
            
        if not field_defn.split('"')[1] == alias_tuple[0]:
            raise Exception("Field name doesn't match alias")
        
            
        targets = []
        
        if target_layer is not None:
            targets.append(target_layer)
            
        else:
            targets = self.defs[target_museum]['layers'].keys()
        
        for t in targets:
            self.defs[target_museum]['layers'][t]["fields"].append(field_defn)
            self.defs[target_museum]['layers'][t]["field_mapping"].append(alias_tuple)
            
            
    def add_properties(self,
                       prop,
                       alias_tuple,
                       field,
                       target_museum='default'):
        
        if not 'properties' in self.defs[target_museum]:
            self.defs[target_museum]['properties']={}
            
        self.defs[target_museum]['properties'][prop]
        
        pass
        
                    
    
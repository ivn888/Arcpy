"""Module docstring.
creat_FGDB_from_FCs.PY
Long Usage:
This scripts takes files from a SDE database and copies it to a local file geodatabase.

change dir to the output directory location
change input_source to the SDE connection file'
change fc_list to point to a text file that contains feature names you want copied.
change arcgis_version to the output FGDB output version
"""

import arcpy
import os
import shutil
import sys

#set output location for FGDB
outDir = r"C:\Users\jastepha\Desktop\test"

#set input location (sde connection file)
#the pre-defined SDE connection file for input SOURCE
input_source =  r"C:\Users\jastepha\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to indeaprod2.sde"

#set the list of FCs you want to copy to FGDB
fc_list = ['indea:genmaint.idm_eds_std', 'indea:genmaint.cart_point_vas_std', 'indea:genmaint.idm_ebc_buildings']

arcgis_version = "10.0"

# set the Source Feature Class you want to bring over in a txt file list for looping - this will create one FGDB for every FC
#(list of SCHEMA.TABLENAMES)
for input_fc in fc_list:
   print input_fc
   input_fc.split(".", 2)
   input_table = input_fc.split(".")[1]
   print input_table

   arcpy.env.workspace = outDir + "\\" + input_table + ".gdb"
   
   #set the output location
   outWorkspace = arcpy.env.workspace
   output = outWorkspace + "\\" + input_table 

   # if FGDB exists then delete it.. (without prompt)
   if os.path.exists(outWorkspace):
           print "already exists so deleting FGDB first: " + outWorkspace
           shutil.rmtree(outWorkspace)   

   input = input_source + "\\" + input_fc
   print "input: " + input
   
   # set some defaults
   arcpy.env.extent = arcpy.Extent(200000,200000,1900000,1900000)
   schemaType = "NO_TEST"
   fieldMappings = ""
   subtype = ""

   #set the projection to BC Albers.
   arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3005)

   # print the environment list 
   environments = arcpy.ListEnvironments()
   
   for environment in environments:
       # Use Python's eval function to evaluate an environment's value
       envSetting = eval("arcpy.env." + environment)
       # Format and print each environment and its current setting
       print "%-30s: %s" % (environment, envSetting)


   #do it.
   try:
       print "creating FGDB"
       #create a FGDB in v10 based on table name (you could parameterized the diretory)
       arcpy.CreateFileGDB_management(outDir, input_table,arcgis_version)
       
       #set the output location
       output = outWorkspace + "\\" + input_table
             
       print "creating feature class using FCtoFC_conversion function: " + output
       print "input " + input
       print "output " + output
                 
       arcpy.FeatureClassToFeatureClass_conversion(input,  outWorkspace,  input_table)
       
   except:
       # If an error occurred while running a tool print the messages
       print arcpy.GetMessages()




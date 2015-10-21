import arcpy
import datetime
import logging
import logging.handlers
import os
import shutil
import sys
import time

########################## user defined functions ##############################

def getDatabaseItemCount(workspace):
    log = logging.getLogger("script_log")
    """returns the item count in provided database"""
    arcpy.env.workspace = workspace
    feature_classes = []
    log.info("Compiling a list of items in {0} and getting count.".format(workspace))
    for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,datatype="Any",type="Any"):
        for filename in filenames:
            feature_classes.append(os.path.join(dirpath, filename))
    log.info("There are a total of {0} items in the database".format(len(feature_classes)))
    return feature_classes, len(feature_classes)

def replicateDatabase(dbConnection, targetGDB):
    log = logging.getLogger("script_log")
    startTime = time.time()

    if arcpy.Exists(dbConnection):
        featSDE,cntSDE = getDatabaseItemCount(dbConnection)
        log.info("Geodatabase being copied: %s -- Feature Count: %s" %(dbConnection, cntSDE))
        if arcpy.Exists(targetGDB):
            featGDB,cntGDB = getDatabaseItemCount(targetGDB)
            log.info("Old Target Geodatabase: %s -- Feature Count: %s" %(targetGDB, cntGDB))
            try:
                shutil.rmtree(targetGDB)
                log.info("Deleted Old %s" %(os.path.split(targetGDB)[-1]))
            except Exception as e:
                log.info(e)

        GDB_Path, GDB_Name = os.path.split(targetGDB)
        log.info("Now Creating New %s" %(GDB_Name))
        arcpy.CreateFileGDB_management(GDB_Path, GDB_Name)

        arcpy.env.workspace = dbConnection

        # try:
        #     datasetList = [arcpy.Describe(a).name for a in arcpy.ListDatasets()]
        # except Exception, e:
        #     datasetList = []
        #     log.info(e)
        try:
            featureClasses = layerNameLst
        except Exception, e:
            featureClasses = []
            log.info(e)
        # try:
        #     tables = [arcpy.Describe(a).name for a in arcpy.ListTables()]
        # except Exception, e:
        #     tables = []
        #     log.info(e)

        #Compiles a list of the previous three lists to iterate over
        allDbData = featureClasses # + datasetList + tables

        for sourcePath in allDbData:
            targetName = sourcePath.split('.')[-1]
            targetPath = os.path.join(targetGDB, targetName)
            if not arcpy.Exists(targetPath):
                try:
                    log.info("Attempting to Copy %s to %s" %(targetName, targetPath))
                    arcpy.Copy_management(sourcePath, targetPath)
                    log.info("Finished copying %s to %s" %(targetName, targetPath))
                except Exception as e:
                    log.info("Unable to copy %s to %s" %(targetName, targetPath))
                    log.info(e)
            else:
                log.info("%s already exists....skipping....." %(targetName))

        featGDB,cntGDB = getDatabaseItemCount(targetGDB)
        log.info("Completed replication of %s -- Feature Count: %s" %(dbConnection, cntGDB))

    else:
        log.info("{0} does not exist or is not supported! \
        Please check the database path and try again.".format(dbConnection))

#####################################################################################

def formatTime(x):
    minutes, seconds_rem = divmod(x, 60)
    if minutes >= 60:
        hours, minutes_rem = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes_rem, seconds_rem)
    else:
        minutes, seconds_rem = divmod(x, 60)
        return "00:%02d:%02d" % (minutes, seconds_rem)

# Layer name list. Controls which features will be copied.
layerNameLst = ['indea:mdwilkie.indea_background_ebc_greenspace_active',
 'indea:mdwilkie.indea_background_ebc_usa_poly_active',
 'indea:mdwilkie.indea_background_ebc_communities_active',
 'indea:genmaint.idm_ebc_roads',
 'indea:genmaint.idm_eds_std',
 'indea:mdwilkie.indea_road_segments_active',
 'indea:mdwilkie.indea_background_ebc_railways_active',
 'indea:genmaint.idm_ebc_municipalities_ebc_indian_reserves',
 'indea:mdwilkie.indea_background_ebc_canada_poly_active',
 'indea:mdwilkie.indea_background_ebc_water_features_streams_active',
 'indea:mdwilkie.indea_background_ebc_water_features_areal_active',
 'indea:genmaint.cart_ebc_buildings',
 'indea:mdwilkie.indea_background_ebc_ocean_active',
 'indea:mdwilkie.indea_background_ebc_islands_active',
 'indea:mdwilkie.indea_background_ebc_parks_active',
 'indea:genmaint.cart_ebc_water_features_streams_tab']

if __name__ == "__main__":
    startTime = time.time()
    now = datetime.datetime.now()

    ############################### user variables #################################
    """Change these variables to the location of the database being copied, the target 
    database location, and where you want the log to be stored"""

    logPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "replicateSDE_Logfiles") # current location of .py file.
    databaseConnection = "PATH TO YOUR SDE CONNECTION FILE."
    targetGDB = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Replicated.gdb")

    ############################### logging items ###################################
    # Layer name list.

    # Make a global logging object.
    logName = os.path.join(logPath,(now.strftime("%Y-%m-%d_%H-%M.log")))

    log = logging.getLogger("script_log")
    log.setLevel(logging.INFO)

    h1 = logging.FileHandler(logName)
    h2 = logging.StreamHandler()

    f = logging.Formatter("[%(levelname)s] [%(asctime)s] [%(lineno)d] - %(message)s",'%m/%d/%Y %I:%M:%S %p')

    h1.setFormatter(f)
    h2.setFormatter(f)

    h1.setLevel(logging.INFO)
    h2.setLevel(logging.INFO)

    log.addHandler(h1)
    log.addHandler(h2)

    log.info('Script: {0}'.format(os.path.basename(sys.argv[0])))

    try:
        ########################## function calls ######################################

        replicateDatabase(databaseConnection, targetGDB)

        ################################################################################
    except Exception, e:
        log.exception(e)

    totalTime = formatTime((time.time() - startTime))
    log.info('----------------------------------------------------')
    log.info("Script Completed After: {0}".format(totalTime))
    log.info('----------------------------------------------------')
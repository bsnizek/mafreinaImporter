# -*- coding: UTF-8 -*-
# Creating KVINTUS Instatiationfunction
# Basic variables and functions
# HSP, June 2012
from dbfpy import dbf

from Normalizer import *

delim = ";"
indent1 = ""
indent2 = "    "
modelName = "MyModel_"
path = "C:\data\Mafreina\Data\New_Entry_Points/".replace("\\", "/")

dataPath = "C:\data\Mafreina\Data\New_Entry_Points/".replace("\\", "/")
##dataPath = "P:\PROJEKT\MaFreiNa\Data\GeoData\\".replace("\\", "/")
pointId = {}
wayPointIdList = []
wayPointFileString = ""
wayPointFileName = "WayPoints_NewP3.dbf"
wayPointIdField  = "wayPId"
##pointId["WayPoints_NewP.dbf"]     = "wayPId"
entryPointIdList = []
entryPointFileString = ""
##pointId["entryPoints_NewP.dbf"] = "entryPId"
entryPointFileName = "entryPoints_NewP.dbf"
entryPointIdField  = "entryPId"

##for id in pointId.keys():
##    wayPointFileString += id + ", "
##    db = dbf.Dbf(dataPath + id)
##    for rec in db:
##        if pointId[id] not in wayPointIdList:
##            wayPointIdList.append(rec[pointId[id]])
##    pointId[id]
##    wayPointIdList.sort()
##db.close()
db = dbf.Dbf(dataPath + wayPointFileName)
for rec in db:
    if rec[wayPointIdField] not in wayPointIdList:
        wayPointIdList.append(rec[wayPointIdField])
wayPointIdList.sort()
db.close()
db = dbf.Dbf(dataPath + entryPointFileName)
for rec in db:
    if rec[entryPointIdField] not in entryPointIdList:
        entryPointIdList.append(rec[entryPointIdField])
entryPointIdList.sort()
db.close()


entryPointLoaderName = "entryPointLoader"
entryPointIdField = "entryPointId"
entryPointSourceName = "entryPoints"
wayPointIdField = "wayPointId"
wayPointSourceName = "wayPoints"

inEPFileName = path + "entry_profile.csv"
outTTFileName = path + modelName + "timeTables.xml"
outEntryPointFileName = path + modelName + "entryPoints.xml"

inWPFileName = path + "waypointstoaim.csv"
outStateFileName = path + modelName + "States.xml"
outAgentFileName = path + modelName + "Agents.xml"
outWayPointFileName = path + modelName + "WayPoints.xml"


n = Normalizer()

def getRidOfSpecialCharacters(s):
    return n.normalize(s)
            
def genericAgentTypeName(name):
    if name in (2, "Easy hiker", "Hiker easy"):
        return "easyHiker"
    if name in (1, "Advanced hiker", "Hiker advanced"):
        return "advancedHiker"
    if name in (4, "Easy Biker", "Biker easy"):
        return "easyBiker"
    if name in (3, "Advanced Biker", "Biker advanced"):
        return "advancedBiker"
    else:
        return "foo"

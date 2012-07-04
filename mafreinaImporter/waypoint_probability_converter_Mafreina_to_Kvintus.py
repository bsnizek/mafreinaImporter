# -*- coding: UTF-8 -*-

# Creating KVINTUS Instatiationfunction: entrypoint -> waypoint probabilities
# from MAFEINA text file
# HSP, June 2012
# Rather hard coded :-)

from KvintusXML_Config import *
from Normalizer import Normalizer

class readLineStr:
    def __init__(self, inWPHdl, delim):
        self.inWPHdl = inWPHdl
        self.firstInt = ""
        self.name = ""
        self.lineNumber = 0
    def readLine(self):
        line = self.inWPHdl.readline()
        try:
            self.line = line.replace("\n", "")
            self.strLine = self.line.split(delim)
            self.firstInt = int(self.strLine[0])
            self.name = self.strLine[1]
        except:
            self.firstInt = False
            self.name = False
            pass
        if line:
            self.lineNumber += 1
            return False
        else:
            return True

def substList(list, fromElement, toElement):
    for i in range(len(list)):
        if list[i] == fromElement:
            list[i] = toElement
        try:
           if i > 1:
               list[i] = float(list[i])
        except:
            pass

def ifZeroPct (val1, val2):
    if val2 == 0.0:
        return 0
    else:
        try:
            val1 = float(val1)
        except:
            val1 = 0.0
        return int(round(100 * val1 / val2, 0))

def filterStates(entryPointID, entryPointName, wayPointProbabilities, countFunctions, agentTypes):
    i = 2
    for key in agentTypes.keys():
        agentTypes[key].genericAgentId = genericAgentTypeName(key)
        genericAgentId = agentTypes[key].genericAgentId
        propSum = 0
        for wayPoint in wayPointProbabilities:
            if wayPoint[i] > 0:
                propSum += 1
        if propSum > 0:
            entryPointName = entryPointName.replace(" ", "_")
            for wayPoint in wayPointProbabilities:
                if wayPoint[i] > 0:
                    blanks = " "
                    for cc in range(3 - len(str(wayPoint[i]))):
                        blanks += " "           
            agentTypes[key].initiateStates.append(genericAgentId + "_" + str(entryPointID) + "_" + entryPointName)
            countFunctions += 1
        i += 1
    return countFunctions

class agentParams:
    def __init__(self, genericAgentId, timeAvailable, entryTime, wayPointWait, numParti, speedAlpha, speedBeta, iconSymbol, iconSize, iconColor, iconColorPause, iconColorExit, initiateStates=[]):
        self.genericAgentId = genericAgentId
        self.timeAvailable  = timeAvailable
        self.numParti       = numParti
        self.speedAlpha     = speedAlpha
        self.speedBeta      = speedBeta
        self.wayPointWait   = wayPointWait
        self.iconSymbol     = iconSymbol
        self.iconSize       = iconSize
        self.iconColor      = iconColor
        self.iconColorPause = iconColorPause
        self.iconColorExit  = iconColorExit
        self.initiateStates = []

    def writeAgents(self, outAgentHdl):
        for state in self.initiateStates:
            outAgentHdl.write(indent2 + "\n<agentType ID= \"agent_" + state + "\" revolve=\"false\">" + "\n")
            outAgentHdl.write(indent2 + "<timeAvailable>" + str(self.timeAvailable) + "</timeAvailable>\n")
            outAgentHdl.write(indent2 + "<numberOfParticipants>" + str(self.numParti) + "</numberOfParticipants>\n")
            outAgentHdl.write(indent2 + "<stateRefTypes>\n")
            outAgentHdl.write(indent2 + indent2 + "<stateRefType order=\"1\" pctoftrip=\"75\" ref=\"" + "entryState_" + state + "\"></stateRefType>\n")
            outAgentHdl.write(indent2 + indent2 + "<stateRefType order=\"2\" pctoftrip=\"25\" ref=\"" + "exitState_" + state + "\"></stateRefType>\n")
            outAgentHdl.write(indent2 + "</stateRefTypes>\n")
            outAgentHdl.write(indent2 + "<icon>\n")
            outAgentHdl.write(indent2 + indent2 + "<primitive>" + self.iconSymbol + "</primitive>\n")
            outAgentHdl.write(indent2 + indent2 + "<size>" + str(self.iconSize) + "</size>\n")
            outAgentHdl.write(indent2 + "</icon>\n")
            outAgentHdl.write("</agentType>"+ "\n")

    def writeStates(self, outStateHdl, entryPointID, entryPointName, wayPointProbabilities, countFunctions):
        ## Entry-/waypoint probability states
        
        if entryPointID == 10101:
            pass
            # import pdb;pdb.set_trace()
        
        i = 2
        propSum = 0
        for wayPoint in wayPointProbabilities:
            if wayPoint[i] > 0:
                propSum += 1
                
        if 0 == 0:
        #if propSum > 0:
            entryPointName = entryPointName.replace(" ", "_")
            outStateHdl.write("<stateType ID=\"" + "entryState_" + self.genericAgentId + "_" + str(entryPointID) + "_" + entryPointName + "\">\n")
            outStateHdl.write(indent2 + "<iconcolour>" + self.iconColor + "</iconcolour>\n")
            outStateHdl.write(indent2 + "<speed>\n")
            outStateHdl.write(indent2 + indent2 + "<alpha>" + str(self.speedAlpha) + "</alpha>\n")                  
            outStateHdl.write(indent2 + indent2 + "<beta>" + str(self.speedBeta) + "</beta>\n")                  
            outStateHdl.write(indent2 + "</speed>\n")
            outStateHdl.write(indent2 + "<headOnFactor>1.0</headOnFactor>\n");
            outStateHdl.write(indent2 + "<agentMode>network</agentMode>\n")
            outStateHdl.write(indent2 + "<type>normal</type>\n")
            outStateHdl.write(indent2 + "<instantiationFunctions>\n" + indent2 + indent2 + "<function name=\"selectWaypoint\">\n")
            for wayPoint in wayPointProbabilities:
                if wayPoint[i] > 0:
                    blanks = " "
                    for cc in range(3 - len(str(wayPoint[i]))):
                        blanks += " " 
                    n = Normalizer()          
                    outStateHdl.write(indent2 + indent2 + "<waypoint id=\"" + str(wayPoint[0]) + "\" probability=\"" + str(wayPoint[i]) + "\" />" + blanks + "<!-- " + n.normalize(wayPoint[1]) + "-->\n")
            outStateHdl.write(indent2 + indent2 + "</function>\n" + indent2 + "</instantiationFunctions>\n")
            countFunctions += 1
            outStateHdl.write("</stateType>\n\n") 
        i += 1
        ## Pause at waypoint behaviour
        entryPointName = entryPointName.replace(" ", "_")
        outStateHdl.write("<stateType ID=\"" + "atWayPointState_" + self.genericAgentId + "_" + str(entryPointID) + "_" + entryPointName + "\">\n")
        outStateHdl.write(indent2 + "<iconcolour>" + self.iconColorPause + "</iconcolour>\n")
        outStateHdl.write(indent2 + "<speed>\n")
        outStateHdl.write(indent2 + indent2 + "<alpha>" + str(self.speedAlpha) + "</alpha>\n")                  
        outStateHdl.write(indent2 + indent2 + "<beta>" + str(self.speedBeta) + "</beta>\n")                  
        outStateHdl.write(indent2 + "</speed>\n")
        outStateHdl.write(indent2 + "<headOnFactor>1.0</headOnFactor>\n");
        outStateHdl.write(indent2 + "<agentMode>network</agentMode>\n")
        outStateHdl.write(indent2 + "<type>normal</type>\n")
        outStateHdl.write(indent2 + "<categoricTransitionFunctions>\n")
        outStateHdl.write(indent2 + indent2 + "<function name=\"waitTime\">\n")
        outStateHdl.write(indent2 + indent2 + indent2 +  "<parameter>" + str(self.wayPointWait) + "</parameter>\n")
        outStateHdl.write(indent2 + indent2 + indent2 + "<toState>" + "Exit_" + self.genericAgentId + "_" + str(entryPointID) + "_" + entryPointName + "</toState>\n")                  
        outStateHdl.write(indent2 + indent2 + "</function>\n")
        outStateHdl.write(indent2 + "</categoricTransitionFunctions>\n")
        outStateHdl.write("</stateType>\n\n") 

        ## Exit behaviour 
        outStateHdl.write("<stateType ID=\"" + "exitState_" + self.genericAgentId + "_" + str(entryPointID) + "_" + entryPointName + "\">\n")
        outStateHdl.write(indent2 + "<iconcolour>" + self.iconColorExit + "</iconcolour>\n")
        outStateHdl.write(indent2 + "<speed>\n")
        outStateHdl.write(indent2 + indent2 + "<alpha>" + str(self.speedAlpha) + "</alpha>\n")                  
        outStateHdl.write(indent2 + indent2 + "<beta>" + str(self.speedBeta) + "</beta>\n")                  
        outStateHdl.write(indent2 + "</speed>\n")
        outStateHdl.write(indent2 + "<headOnFactor>1.0</headOnFactor>\n");
        outStateHdl.write(indent2 + "<agentMode>network</agentMode>\n")
        outStateHdl.write(indent2 + "<type>normal</type>\n")
        outStateHdl.write(indent2 + "<instantiationFunctions>\n")
        outStateHdl.write(indent2 + indent2 + "<function name=\"selectWaypoint\">\n")
        outStateHdl.write(indent2 + indent2 + indent2 + "<waypoint id=\"" + str(entryPointID) + "\" probability=\"100\"/>\n")                  
        outStateHdl.write(indent2 + indent2 + "</function>\n")
        outStateHdl.write(indent2 + "</instantiationFunctions>\n")
        outStateHdl.write("</stateType>\n\n") 
        ##return countFunctions
    def dictWayPoints(self, wpDict):
        for state in self.initiateStates:
            wpParams = state.split("_")
            wpNumber = int(wpParams[1])
            if wpNumber not in wpDict.keys():
                wpName = ""
                wpNameList = wpParams[2:len(wpParams)]
                for word in wpNameList:
                    wpName += word + " "
                wpDict[wpNumber] = wpName
                ##print wpNumber
        return wpDict

## -------- MAIN EXECUTABLE --------
inWPHdl = open(inWPFileName, "r")
outStateHdl = open(outStateFileName, "w")
outAgentHdl = open(outAgentFileName, "w")
outWayPointHdl = open(outWayPointFileName, "w")

agentTypes = {}
##(self, genericAgentId, timeAvailable, entryTime, wayPointWait, numParti, speedAlpha, speedBeta, iconSymbol, iconSize, iconColor, iconColorPause, iconColorExit, initiateStates=[]):
agentTypes[1] = agentParams("xx", 240, 160, 30, 1,  5, 0, "square", 6, "rgb(250,0,0)", "rgb(250,0,255)", "rgb(0,0,0)")
agentTypes[2] = agentParams("xx", 120, 160, 30, 1,  3, 0, "square", 6, "rgb(250,0,0)", "rgb(250,0,255)", "rgb(0,0,0)")
agentTypes[3] = agentParams("xx", 240, 160, 30, 1, 16, 0, "circle", 6, "rgb(0,250,0)","rgb(250,0,255)", "rgb(0,0,0)")
agentTypes[4] = agentParams("xx", 120, 160, 30, 1, 10, 0, "circle", 6, "rgb(0,250,0)", "rgb(250,0,255)", "rgb(0,0,0)")

xx = readLineStr(inWPHdl, delim)
EOF = False
headerLine = True
rowLine = False
wayPoints = []
wayPointListAll = {}
entryPointListAll = {}
entryPointID = ""
countEntryPoints = 1
countFunctions = 1
entryPointName = "TODO"

entrypointID__waypointProbabilities = {}

#Reading in-file (waypoint distribution)
while not EOF:
    EOF = xx.readLine()
    #Reading on to next line
    if xx.firstInt and not headerLine:
        substList(xx.strLine, "", 0.0)
        wayPoints.append(xx.strLine)
        rowLine = True
    # All lines for an entrypoint found. Writing to file
    if not xx.firstInt and not headerLine and rowLine:
        advancedHikerTotal = 0.0
        easyHikerTotal     = 0.0
        advancedBikerTotal = 0.0
        easyBikerTotal     = 0.0
        for wayPoint in wayPoints:
            advancedHikerTotal += wayPoint[2]
            easyHikerTotal     += wayPoint[3]
            advancedBikerTotal += wayPoint[4]
            
            try:
                easyBikerTotal += float(wayPoint[5])
            except:
                pass
            
        wayPointProbabilities = []
        for wayPoint in wayPoints:
            advancedHikerPct  = ifZeroPct(wayPoint[2], advancedHikerTotal)
            easyHikerPct = ifZeroPct(wayPoint[3], easyHikerTotal)
            advancedBikerPct  = ifZeroPct(wayPoint[4], advancedBikerTotal)
            easyBikerPct      = ifZeroPct(wayPoint[5], easyBikerTotal)
            wayPointProbabilities.append([wayPoint[0], wayPoint[1], advancedHikerPct, easyHikerPct, advancedBikerPct, easyBikerPct])
            if wayPoint[0] not in wayPointListAll.keys():
                wayPointListAll[wayPoint[0]] = wayPoint[1]
        entryPointName = getRidOfSpecialCharacters(entryPointName)
        countFunctions = filterStates(entryPointID, entryPointName, wayPointProbabilities, countFunctions, agentTypes)
        ##print entryPointName
        if entryPointID not in wayPointListAll.keys():
            entryPointListAll[entryPointID] = entryPointName
        wayPoints = []
        headerLine = True
        rowLine = False
        
        entrypointID__waypointProbabilities[entryPointID] = wayPointProbabilities
        
    # New header line (entry point) found
    if xx.firstInt and headerLine:
        entryPointID = xx.firstInt
        entryPointName = xx.name
        wayPoints = []
        countEntryPoints += 1
        headerLine = False

countAgentTypes = 0

# Writing Agent Types
outAgentHdl.write("<agents>\n\n")
for key in agentTypes.keys():
    agentTypes[key].writeAgents(outAgentHdl)
    countAgentTypes += len(agentTypes[key].initiateStates)
outAgentHdl.write("</agents>\n\n")
                         
# Writing State Types
outStateHdl.write("<stateTypes>\n\n")

print entryPointListAll.keys()
for entryPointID in entryPointListAll.keys():
    for key in agentTypes.keys():
        agentTypes[key].writeStates(outStateHdl, entryPointID, entryPointListAll.get(entryPointID), entrypointID__waypointProbabilities.get(entryPointID), countFunctions)
        countAgentTypes += len(agentTypes[key].initiateStates)
outStateHdl.write("</stateTypes>\n\n")

# Writing Way Points
outWayPointHdl.write("<waypoints>\n\n")
outWayPointHdl.write(indent2 + "<loader type=\"point\">\n")
outWayPointHdl.write(2 * indent2 + "<geometry>\n")
outWayPointHdl.write(3 * indent2 + "<source>" + wayPointSourceName + "</source>\n")
outWayPointHdl.write(3 * indent2 + "<query></query>\n")
outWayPointHdl.write(3 * indent2 + "<id_field_id>" + wayPointIdField + "</id_field_id>\n")
outWayPointHdl.write(2 * indent2 + "</geometry>\n")
outWayPointHdl.write(indent2 + "</loader>\n\n")
outWayPointHdl.write("</waypoints>\n\n")

# Printing check af applied Way Points
wpKeys = []
for wp in wayPointListAll.keys():
    wpKeys.append(wp)
wpKeys.sort()
for wp in wpKeys:
    if int(wp) not in wayPointIdList:
        print  "ERROR in Way Point!!!", wp, wayPointListAll[wp], "Not found in DBF's: " + wayPointFileName
# Printing check af applied Entry Points
wpKeys = []
for wp in entryPointListAll.keys():
    wpKeys.append(wp)
wpKeys.sort()
for wp in wpKeys:
    if int(wp) not in entryPointIdList:
        print  "ERROR in Entry Point!!!", wp, entryPointListAll[wp], "Not found in DBF's: " + entryPointFileName

# Reporting....
print countAgentTypes, "agents, written to", outAgentFileName
print countFunctions, "state type functions, for", countEntryPoints, "entrypoints, written to:\n", outStateFileName

# Closing files
inWPHdl.close()
outStateHdl.close()
outAgentHdl.close()
outWayPointHdl.close()

# Creating KVINTUS Entry points and Timetables from MAFEINA text file
# HSP, June 2012
# Rather hard coded :-)

from KvintusXML_Config import *
from Normalizer import Normalizer

def writeEntryPointProfiles(outEntryPointHdl, entryPointName, agentTypes):
        epNumber = entryPointName.split("_")[0]
        outEntryPointHdl.write(indent1 + "\n<entrypoint ID=\"ep_" + epNumber + "\" geotype=\"point\" type=\"dynamic\">\n")
        outEntryPointHdl.write(2 * indent2 + "<loader>entry_loader</loader>\n")
        outEntryPointHdl.write(2 * indent2 + "<geometry_id>" + epNumber + "</geometry_id>\n")
        outEntryPointHdl.write(2 * indent2 + "<profiles>\n")
        for agent in agentTypes:
            n = Normalizer()
            agent = n.normalize(agent);
            outEntryPointHdl.write(3 * indent2 + "<profile>\n")
            outEntryPointHdl.write(4 * indent2 + "<agentDistribution pctofentries=\"100.0\" agent_type=\"agent_" + agent + "\"/>\n")
            outEntryPointHdl.write(4 * indent2 + "<timetableReference ref=\"tt_" + agent + "\" scaleFactor=\"1.0\"/>\n")
            outEntryPointHdl.write(3 * indent2 + "</profile>\n")
        outEntryPointHdl.write(2 * indent2 + "</profiles>\n")
        outEntryPointHdl.write(indent1 + "</entrypoint>\n")

## MAIN...
inEPHdl = open(inEPFileName, "r")
outTTHdl = open(outTTFileName, "w")
outEntryPointHdl = open(outEntryPointFileName, "w")

outTTHdl.write("<timetables>\n")
agentTypesAtEntryPoints = {}

line = inEPHdl.readline()
countProfiles = 1
countZeroProfiles = 1
while line:
    strLine = line.split(delim)
    try:
        entryPointNumber = int(strLine[0])
        epName = genericAgentTypeName(strLine[2])
        activityEntryPointName = epName + "_" + strLine[0].replace(" ", "_") + "_" + strLine[1].replace(" ", "_")
        entryPointName = strLine[0].replace(" ", "_") + "_" + strLine[1].replace(" ", "_")
        totalEntries = int(strLine[16])
        if totalEntries > 0:
            ## Generating list of agenttypes over entry points
            if not entryPointName in agentTypesAtEntryPoints.keys():
                agentTypesAtEntryPoints[entryPointName] = []
            agentTypesAtEntryPoints[entryPointName].append(activityEntryPointName)
            ## Writing Time Tables
            
            n = Normalizer()
            
            timetableHeader = "\n<timetableData ID=\"tt_" + epName + "_" + n.normalize(entryPointName) + "\">"
            timetableNote = "<!-- Time Table for Entrypoint ID: " + str(entryPointNumber) + " -->"
            timetableFooter = "</timetableData>"
            outTTHdl.write(indent1 + timetableHeader + "\n")
            outTTHdl.write(indent2 + timetableNote + "\n")
            time1 = 0
            timeIncrement = 2
            for i in range(3, 15):
                try:
                    pctCount = int(strLine[i])
                except:
                    pctCount = 0
                time2 = time1 + timeIncrement
                count = int(round(totalEntries * (pctCount / 100.0)))
                strPeriod = "<period" + "%02d" % (time1,) + "_" + "%02d" % (time2,) + ">" + str(count) + "</period" + "%02d" % (time1,) + "_" + "%02d" % (time2,) + ">"
                outTTHdl.write(indent2 + strPeriod + "\n")
                time1 = time2
            outTTHdl.write(indent1 + timetableFooter + "\n")
            ##outEntryPointHdl.write(indent1 + entrypointFooter + "\n")
            countProfiles += 1
        else:
            countZeroProfiles += 1

        line = inEPHdl.readline()
    except:
        line = inEPHdl.readline()

outEntryPointHdl.write("<entrypoints>\n")
outEntryPointHdl.write("\n<loader type=\"point\" ID=\"" + entryPointLoaderName + "\"> \n")
outEntryPointHdl.write(indent2 + "<geometry>\n")
outEntryPointHdl.write(indent2 + indent2 + "<source>" + entryPointSourceName + "</source>\n")
outEntryPointHdl.write(indent2 + indent2 + "<query></query>\n")
outEntryPointHdl.write(indent2 + indent2 + "<id_field_id>" + entryPointIdField + "</id_field_id>\n")
outEntryPointHdl.write(indent2 + "</geometry>\n")
outEntryPointHdl.write("</loader>\n")

for epName in agentTypesAtEntryPoints.keys():
    writeEntryPointProfiles(outEntryPointHdl, epName, agentTypesAtEntryPoints[epName])
    ##print epName
outEntryPointHdl.write("\n</entrypoints>\n")

outTTHdl.write("\n</timetables>")

print countProfiles, "entry profiles -", countZeroProfiles, "disregarded (due to no entries) - written to\n", outTTFileName
inEPHdl.close()
outTTHdl.close()
outEntryPointHdl.close()
        


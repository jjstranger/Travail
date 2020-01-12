import pymel.core as pmc

selGeoNameLs=[]
def trv_filterObjsByName(selGeoNameLs):
    geoLs=[]
    for item in selGeoNameLs:
        geoLs.extend(pmc.ls(item,r=1))
    if len(geoLs)!=1:
        pmc.confirmDialog(m="There are "+str(len(geoLs))+" objects fit the name '"+item+"'.")
        pmc.select(geoLs)
        return geoLs


def trv_getFrameRange():
    srartFrame=pmc.playbackOptions(q=1,min=1)
    endFrame=pmc.playbackOptions(q=1,max=1)
    return srartFrame,endFrame

def trv_getExportFilePath():
    filePath=pmc.workspace.getPath()+"/cache/Alembic/"
    fileName="AbcExprtTest_v001.abc"
    ExprtFilePath=filePath+fileName#pmc.workspace
    print ExprtFilePath
    return ExprtFilePath

def getABCOPSets():
    setsLs=pmc.ls("*AlembicOP",set=1,r=1)
    return setsLs

def trv_exportToABCAction(task,exportfilePath,exportframerange):
    
    for task in exprtJobLs:
        ExprtRootOption="-sn -uv -ws "
        for obj in task:
            ExprtRootOption+=("-rt "+obj+" ")
        ExprtFrameRange=" -fr "+str(exportframerange[0]+" "+str(exportframerange[1])
        ExprtFilePath=" -f "+

    jobCmd=""
    pmc.AbcExport(v=1,j="-stripNamespace -uv -ws -fr 1 100-rt '|XX' -f 'PATH' ")

import pymel.core as pmc

objFilterStringLs=[]
def trv_filterObjsByName(objFilterStringLs):
    filtedObjLs=[]
    for item in objFilterStringLs:
        filtedObjLs.extend(pmc.ls(item,r=1))
    if len(filtedObjLs)!=1:
        pmc.confirmDialog(m="There are "+str(len(filtedObjLs))+" objects fit the name '"+item+"'.")
        pmc.select(filtedObjLs)
    return filtedObjLs

def trv_getFrameRange():# refine to ani/static 2ways
    srartFrame=pmc.playbackOptions(q=1,min=1)
    endFrame=pmc.playbackOptions(q=1,max=1)
    return srartFrame,endFrame

def trv_getExportFilePath(fileName):
    filePath=pmc.workspace.getPath()+"/cache/Alembic/"# refine to workspace direction
    ExprtFilePath=filePath+fileName
    return ExprtFilePath

def getABCOPSets():
    setsLs=pmc.ls("*_AlembicOP*",set=1,r=1)
    setsAssemble=[]
    for item in setsLs:
        getSetName=item.replace("_AlembicOP","")
        assmb=[item,getSetName]
        setsAssemble.append(assmb)
    return setsAssemble

def getJobLst():
    try:
        len(getABCOPSets())>0
    except:
        selLst=pmc.ls(sl=1)
        try:
            len(selLst)>0
        except:
            pmc.confirmDialog(m="No Alembic Export Job is found Also no object is selected for export.")
        else:
            return selLst
    else: 
        return getABCOPSets()

def trv_exportToABCAction(exprtJobLs):
    jobStr=[]
    exportframerange=trv_getFrameRange()
    for task in exprtJobLs:
        setMembr=pmc.sets(task[0],q=1)
        ExprtRootOption=""
        ExprtFlags="-sn -uv -ws -wfs "
        for obj in setMembr:
            objStr=pmc.ls(obj,r=1)[0].longName()
            ExprtRootOption+=("-rt "+str(objStr)+" ")
        ExprtFrameRange=" -fr "+str(exportframerange[0])+" "+str(exportframerange[1])
        ExprtFilePath=" -f \""+trv_getExportFilePath(task[1])+".abc\""
        jobStr.append(ExprtFlags+ExprtRootOption+ExprtFrameRange+str(ExprtFilePath))

    pmc.AbcExport(v=1,j=jobStr)

trv_exportToABCAction(getJobLst())
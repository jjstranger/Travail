//	==================================================
//	trv_setsToAbc ver 1.0
//	by : JJ.Stranger
//	at : 2020-07-28
//	description: export the objects grouped 
//		by set to Alembic Cache.
//	==================================================
from pymel import core as pmc

MatchString="AlembicOP"
objFilterStringLs=[]

def trv_filerObjsByName(objFilterStringLs):
    filtedObjLs=[]
    for item in objFilterStringLs:
        filtedObjLs.extend(pmc.ls(item,r=1))
    if len(filtedObjLs)!=1:
        pmc.confirmDialog(m="There are "+str(len(filtedObjLs))+" objects fit the name '"+item +"'.")
        pmc.select(filtedObjLs)
    return filtedObjLs

def createNewExprtTsk():
    objSet=[]
    getSetsNameDialog=pmc.promptDialog(t="Create New Export Task", m="Enter A Name: ",b=["OK","Cancel"],db="OK",cb="Cancel",ds="Cancel")
    getSetsNameFrmInput=pmc.peomptDialog(q=1,tx=1)
    objSet.append(pmc.sets(pmc.ls(sl=1),n=getSetsNameFrmInput+"_"+MatchString))
    return objSet

def filterTskSetsLs(filtedStr):
    fLst=pmc.ls(filtedStr,sets=1,r=1)
    return fLst

def addAttrsToTskSets(setsLsToProc):
    for tskSet in setsLsToProc:
        if pmc.attributeQuery("exportEnable",n=tskSet,ex=1)==0:
            pmc.addattr(tskSet,ln="exportEnable",at="bool",dv=1)
        if pmc.attributeQuery("exportTaskTitle",n=tskSet,ex=1)==0:
            pmc.addattr(tskSet,ln="exportTaskTitle",dt="string")
            pmc.setAttr(tskSet+".exportTaskTitle",tskSet.replace("_"+MatchString,""))
        if pmc.attributeQuery("animState",n=tskSet,ex=1)==0:
            pmc.addattr(tskSet,ln="animState",at="bool",dv=1)
        if pmc.attributeQuery("exportStartFrame",n=tskSet,ex=1)==0:
            pmc.addattr(tskSet,ln="exportStartFrame",at="double",dv=pmc.playbackOptions(q=1,min=1))
        if pmc.attributeQuery("exportEndFrame",n=tskSet,ex=1)==0:
            pmc.addattr(tskSet,ln="exportEndFrame",at="double",dv=pmc.playbackOptions(q=1,max=1))
        if pmc.attributeQuery("exportFilePath",n=tskSet,ex=1)==0:
            pmc.addattr(tskSet,ln="exportFilePath",dt="string")
            pmc.setAttr(tskSet+".exportFilePath",pmc.workspace.getPath()+"/cache/alembic/"+pmc.getAttr(tskSet+".exportTaskTitle")+".abc")

def getFrameRange():
    startFrame=pmc.palybackOptions(q=1,min=1)
    endFrame=pmc.playbackOptions(q=1,max=1)
    return startFrame,endFrame

def getExportFilePath(fileName):
    filePath=pmc.workspace.getPath()+"/cache/Alembic/"
    ExprtFilePath=filePath+fileName+".abc"
    return ExprtFilePath

def getABCOPSets(setsLs):
    setsAssemble=[]
    for setName in setsLs:
        if pmc.attributeQuery("exportEnable",n=setName,ex=1):
            ExportEnable=pmc.getAttr(setName+".exportEnable")
        else:
            ExportEnable=1
        if pmc.attributeQuery("exportTaskTitle",n=setName,ex=1):
            getSetName=pmc.getAttr(setName+".exportTaskTitle")
        else:
            getSetName=setName.replace("_"+MatchString,"")
        if pmc.attributeQuery("exportStartFrame",n=setName,ex=1):
            ExportStartFrame=getAttr(setName+".exportStartFrame")
        else:
            ExportStartFrame=pmc.playbackOptions(q=1,min=1)
        if pmc.attributeQuery("exportEndFrame",n=setName,ex=1):
            ExportEndFrame=getAttr(setName+".exportEndFrame")
        else:
            ExportEndFrame=pmc.playbackOptions(q=1,max=1)
        if pmc.attributeQuery("animState",n=setName,ex=1):
            if pmc.getAttr(setName+".animState")==0:
                ExportEndFrame=ExportStartFrame
        else:
            pass
        ## LEAVE OVERIDE CHECKBOX
        if pmc.attributeQuery("exportFilePath",n=setName,ex=1):
            ExportFilePath=getAttr(setName+".exportFilePath")
        else:
            ExportFilePath=trv_getExportFilePath(getSetName)
        assmb=[setName,getSetName,ExportStartFrame,ExportEndFrame,ExportFilePath,ExportEnable]
        setAssemble.append(assmb)
    return setAssemble

def getTskLst(setsLst):
    try:
        len(getABCOPSets(setsLst))>0
    except:
        return getABCOPSets(filterTskSetsLs("*_"+MatchString+"*"))
    else:
        return getABCOPSets(setsLst)

def exportToABCAction(exprtTskLst):
    tskLs=[]
    for task in exprtTskLst:
        if task[5]==1:
            setMembr=pmc.sets(task[0],q=1)
            ExportFilePath=" -f \""+getExportFilePath(task[1])
            ExportFlags="-sn -uv -ws -wfs"
            ExportRootOption=""
            for obj in setMembr:
                objStr=pmc.ls(obj,r=1)[0].longName()
                ExportRootOption+=("-rt "+str(objStr)+" ")
            ExportFramRange=" -fr "+str(task[2]+" "+str(task[3])
            jobStr.append(ExportFlags+ExportRootOption+ExportFramRange+str(ExportFilePath))
    if pmc.pluginInfo("AbcExport",q=1,l=1)==0:
        pmc.loadPlugin("AbcExport")
    if pmc.checkboxGrp("ClbOptsCBxGrp,q=1,v1=1")==1:
        pmc.refresh(su=1)
    pmc.AbcExport(v=1,j=jobStr)
    pmc.refresh(su=0)

def addTskToLst(fLst):
    pmc.textScrollList("lstCSTsl",e=1,ra=1)
    for line in range(len(fLst)):
        fl=[]
        fl.append(fLst[line])
        tskLs=getTskLst(fl)
        tsk=tskLs[0]
        if tsk[5]!=0:
            pmc.textScrollList("lstCSTsl",e=1,append=job[1],utg=job[0],lf=((line+1),"boldLabelFont"))
        else:
            pmc.textScrollList("lstCSTsl",e=1,append=job[1],utg=job[0],lf=((line+1),"smallObliqueLabelFont"))

def selAction():
    sel=pmc.textScrollList("lstCSTsl",q=1,sl=1)
    addTskToLst(filterTskSetsLs("*_"+Matchstring+"*"))
    pmc.textScrollList("lstCSTsl",e=1,si=sel)
    pmc.select(pmc.textScrollList("lstCSTsl",q=1,sut=1),ne=1)

def doubleClickAction():
    pmc.select(pmc.textScrollList("lstCSTsl",q=1,sut=1))

def addNewExprtTskAction():
    addAttrsToTskSets(createNewExprtTsk())
    addTskToLst(filterTskSetsLs("*_"+MatchString+"*"))

def globalPathSwitch(onoff):
    pmc.textFieldButtonGrp("glbObrdPath",e=1,en=onoff)

def cacheToAbcCmd():
    exportToABCAction(getTskLst(pmc.textScrollList("lstCSTsl",q=1,sut=1)))

def exportToABCWinUI():
    

#from pymel import core as pmc
##workspace.getPath() dosen't work in maya.cmds, instead of workspace(q=1,rd=1)
from maya import cmds as mc

MatchString="AlembicOP"

objFilterStringLs=[]
def trv_filterObjsByName(objFilterStringLs):
    filtedObjLs=[]
    for item in objFilterStringLs:
        filtedObjLs.extend(mc.ls(item,r=1))
    if len(filtedObjLs)!=1:
        mc.confirmDialog(m="There are "+str(len(filtedObjLs))+" objects fit the name '"+item+"'.")
        mc.select(filtedObjLs)
    return filtedObjLs
    #print "Filted Objs: "+filtedObjLs

def filterJobSetLs(filtStr):#flst
    fLst=mc.ls(filtStr,sets=1,r=1)
    return fLst
    #mc.ls("*_AlembicOP*",sets=1,r=1)
def creatNewExprtJobSets():
    objSet=[]
    getNameDialog=mc.promptDialog(t="Create New Export Job",m="Ente A Name:",b=["OK","Cancel"],db="OK",cb="Cancel",ds="Cancel")
    getNameFrmInput=mc.promptDialog(q=1,tx=1)
    objSet.append(mc.sets(mc.ls(sl=1),n=getNameFrmInput+"_"+MatchString))
    return objSet
    
def addAttrsToExprtSets(setsToRroc):
    for objSet in setsToRroc:
        if mc.attributeQuery("exportEnable",n=objSet,ex=1)==0:
            mc.addAttr(objSet,ln="exportEnable",at="bool",dv=1)
        if mc.attributeQuery("exportJobTitle",n=objSet,ex=1)==0:
            mc.addAttr(objSet,ln="exportJobTitle",dt="string")
            mc.setAttr(objSet+".exportJobTitle",objSet.replace("_"+MatchString,""),typ="string")
        if mc.attributeQuery("animState",n=objSet,ex=1)==0:
            mc.addAttr(objSet,ln="animState",at="bool",dv=1)
        if mc.attributeQuery("exportStartFrame",n=objSet,ex=1)==0:
            mc.addAttr(objSet,ln="exportStartFrame",at="double",dv=mc.playbackOptions(q=1,min=1))
        if mc.attributeQuery("exportEndFrame",n=objSet,ex=1)==0:
            mc.addAttr(objSet,ln="exportEndFrame",at="double",dv=mc.playbackOptions(q=1,max=1))
        if mc.attributeQuery("exportFilePath",n=objSet,ex=1)==0:
            mc.addAttr(objSet,ln="exportFilePath",dt="string")
            mc.setAttr(objSet+".exportFilePath",mc.workspace(rd=1,q=1)+"/cache/alembic/"+mc.getAttr(objSet+".exportJobTitle")+".abc",typ="string")
        
def trv_getFrameRange():
    srartFrame=mc.playbackOptions(q=1,min=1)
    endFrame=mc.playbackOptions(q=1,max=1)
    return srartFrame,endFrame

def trv_getExportFilePath(fileName):
    filePath=mc.workspace(q=1,rd=1)+"/cache/Alembic/"
    ExprtFilePath=filePath+fileName
    return ExprtFilePath

def setGlobalPathOveride(objSet):
    getGlobalExprtPath=mc.textScrollList("glbOvrdPath",q=1,fi=1)
    getPathFrmAttr=mc.getAttr(setName+".exportFilePath")
    if ("/" in getPathFrmAttr) & getPathFrmAttr.endswith(".abc") !=1:
        getPathFrmAttr=mc.workspace(q=1,rd=1)+"/cache/alembic/"+mc.getAttr(objSet+".exportJobTitle")+".abc"
    if ("/" in getGlobalExprtPath):
        if (getGlobalExprtPath.endswith("/"))==0:
            getGlobalExprtPath+="/"
        import os
        ExportFilePath=getGlobalExprtPath+os.path.basename(getPathFrmAttr)
    else:
        ExportFilePath=getGlobalExprtPath+mc.getAttr(objSet+".exportJobTitle")+".abc"
    return ExportFilePath
 
def getABCOPSets(setsLs,useOvrdPth):
    setsAssemble=[]
    for setName in setsLs:
        if mc.attributeQuery("exportEnable",n=setName,ex=1):
            ExprtEnable=mc.getAttr(setName+".exportEnable")
        else:
            ExprtEnable=1
        if mc.attributeQuery("exportJobTitle",n=setName,ex=1):
            getSetName=mc.getAttr(setName+".exportJobTitle")
        else:
            getSetName=setName.replace("_AlembicOP","")
        if mc.attributeQuery("exportStartFrame",n=setName,ex=1):
            ExprtStartFrame=mc.getAttr(setName+".exportStartFrame")
        else:
            ExprtStartFrame=mc.playbackOptions(q=1,min=1)
        if mc.attributeQuery("exportEndFrame",n=setName,ex=1):
            ExprtEndFrame=mc.getAttr(setName+".exportEndFrame")
        else:
            ExprtEndFrame=mc.playbackOptions(q=1,max=1)
        if mc.attributeQuery("animState",n=setName,ex=1):
            if mc.getAttr(setName+".animState")==0:
                ExprtEndFrame=ExprtStartFrame
        else:
            pass
        if useOvrdPth:
            ExprtFilePath=setGlobalPathOveride(setName)
        else:
            if mc.attributeQuery("exportFilePath",n=setName,ex=1):
                ExprtFilePath=mc.getAttr(setName+".exportFilePath")
            else:
                ExprtFilePath=trv_getExportFilePath(getSetName)
        assmb=[setName,getSetName,ExprtStartFrame,ExprtEndFrame,ExprtFilePath,ExprtEnable]
        setsAssemble.append(assmb)
    return setsAssemble
    
def getJobLst(setsLs):
    useOvrdPth=mc.checkBoxGrp("GlbOptsCBxGrp",q=1,v2=1)
    try:
        
        len(getABCOPSets(setsLs,useOvrdPth))>0
    except:
        return getABCOPSets(filterJobSetLs("*_"+MatchString+"*"),useOvrdPth)
    else: 
        return getABCOPSets(setsLs,useOvrdPth)
        
def checkPluginsExistAndLoaded(pluginsLs):
    for plugin in pluginsLs:
        if mc.pluginInfo(plugin,q=1,l=1)==0:
            mc.loadPlugin(plugin)
            
def trv_exportToABCAction(exprtJobLs):
    jobStr=[]
    for task in exprtJobLs:
        if task[5]==1:
            setMembr=mc.sets(task[0],q=1)
            ExprtFilePath=" -f \""+task[4]
            ExprtFlags="-sn -uv -ws -wfs "
            ExprtRootOption=""
            for obj in setMembr:
                objStr=mc.ls(obj,r=1)[0].longName()
                ExprtRootOption+=("-rt "+str(objStr)+" ")
            ExprtFrameRange=" -fr "+str(task[2])+" "+str(task[3])
            jobStr.append(ExprtFlags+ExprtRootOption+ExprtFrameRange+str(ExprtFilePath))
    chkPluginLs=["AbcExport"]
    checkPluginsExistAndLoaded(chkPluginLs)
    if mc.checkBoxGrp("GlbOptsCBxGrp",q=1,v1=1)==1:
        mc.refresh(su=1)
    mc.AbcExport(v=1,j=jobStr)
    mc.refresh(su=0)
    
def cacheDir():
    getPrjDir=mc.workspace(rd=1,q=1)
    getABCSubDir=mc.workspace(fre="alembicCache")
    if getPrjDir.endswith("/")==0:
        getPrjDir+="/"
    if len(getABCSubDir)>0:
        getPrjDir+=(getABCSubDir+"/")
    return getPrjDir
        
def addJobItmToLst(fLst):
    mc.textScrollList("lstCSTsl",e=1,ra=1,ri=1)
    for line in range(len(fLst)):
        fl=[]
        fl.append(fLst[line])
        jobLs=getJobLst(fl)
        job=jobLs[0]
        if job[5]!=0:
            mc.textScrollList("lstCSTsl",e=1,append=job[0].replace("_"+MatchString,""),utg=job[0],lf=((line+1),"boldLabelFont"))
        else:
            mc.textScrollList("lstCSTsl",e=1,append=job[0].replace("_"+MatchString,""),utg=job[0],lf=((line+1),"smallObliqueLabelFont"))
            #mc.deleteUI("lstCSTsl",ctl=1)
def refreshJobLsCmd():
    addJobItmToLst(getABCOPSets(filterJobSetLs("*_"+MatchString+"*"),0))
    
def clickItmAction():#select Action
    sel=mc.textScrollList("lstCSTsl",q=1,si=1)
    #refreshJobLsCmd()#
    mc.textScrollList("lstCSTsl",e=1,si=sel)
    mc.select(mc.textScrollList("lstCSTsl",q=1,sut=1),ne=1)
    
def doubleClickAction():
    sel=mc.textScrollList("lstCSTsl",q=1,si=1)
    refreshJobLsCmd()
    mc.textScrollList("lstCSTsl",e=1,si=sel)
    mc.select(mc.textScrollList("lstCSTsl",q=1,sut=1))

def addNewExprtJobAction():
    addAttrsToExprtSets(creatNewExprtJobSets())
    addJobItmToLst(filterJobSetLs("*_"+MatchString+"*"))
    
def ovrdPathSwthCmd(onoff):
    mc.textFieldButtonGrp("glbOvrdPath",e=1,en=onoff)

def openFileDialogForOvrdPth():
    getStartDir=mc.fileDialog2(fm=3,dir=cacheDir(),cap="Choose A Folder To Cache..")
    mc.textFieldButtonGrp("glbOvrdPath",e=1,fi=getStartDir[0]+"/")

def exprtToABCWinUI():
    addAttrsToExprtSets(filterJobSetLs("*_"+MatchString+"*"))
    if mc.window("exprtToABCWin",ex=1):
        mc.deleteUI("exprtToABCWin",wnd=1)
    mc.window("exprtToABCWin",t="TVC Export to ABC")
    mc.columnLayout("tvcABCMainLyt",cat=("both",6),w=400,rs=9,adj=0)
    mc.text("jobLsTxt",l="Export Jobs List: ")
    mc.textScrollList("lstCSTsl",ams=1,nr=20,w=388,npm=3,sc="clickItmAction()",dcc="doubleClickAction()")
    mc.rowLayout("lsOprtRwLyt",w=388,nc=2)
    mc.button("addJobBtn",l="+ Add New Export Job",c="addNewExprtJobAction()",w=190,p="lsOprtRwLyt")
    mc.button("rfsJobLsBtn",l="*Refresh JobList",c="refreshJobLsCmd()",w=190,p="lsOprtRwLyt")
    mc.checkBoxGrp("GlbOptsCBxGrp",l="Global Options: ",l1="Halt viewport when caching",p="tvcABCMainLyt",
        l2="Overide export path",ncb=2,w=388,vr=1,on2="ovrdPathSwthCmd(1)",of2="ovrdPathSwthCmd(0)")
    mc.textFieldButtonGrp("glbOvrdPath",p="tvcABCMainLyt",l="Global Path:",fi=cacheDir(),bl="Browse..",bc="openFileDialogForOvrdPth()",cw3=[80,250,58],w=388,en=0)
    refreshJobLsCmd()
    mc.button("goCCCmd",l="Cache to ABC",w=388,c="trv_exportToABCAction(getJobLst()",p="tvcABCMainLyt",bgc=[0.4,0.28,0.2])
    mc.showWindow("exprtToABCWin")

exprtToABCWinUI()

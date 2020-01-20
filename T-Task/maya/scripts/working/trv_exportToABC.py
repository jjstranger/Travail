from pymel import core as pmc

objFilterStringLs=[]
def trv_filterObjsByName(objFilterStringLs):
    filtedObjLs=[]
    for item in objFilterStringLs:
        filtedObjLs.extend(pmc.ls(item,r=1))
    if len(filtedObjLs)!=1:
        pmc.confirmDialog(m="There are "+str(len(filtedObjLs))+" objects fit the name '"+item+"'.")
        pmc.select(filtedObjLs)
    return filtedObjLs
    print "Filted Objs: "+filtedObjLs

def filterJobSetLs(filtStr):#flst
    fLst=pmc.ls(filtStr,sets=1,r=1)
    return fLst
    
def creatNewExprtJobSets():
    objSet=[]
    getNameDialog=pmc.promptDialog(t="Create New Export Job",m="Ente A Name:",b=["OK","Cancel"],db="OK",cb="Cancel",ds="Cancel")
    getNamefrmInput=pmc.promptDialog(q=1,tx=1)
    objSet.append(pmc.sets(pmc.ls(sl=1),n=getNameFrmInput+"_AlembicOP"))
    return objSet
    
def addAttrsToExprtSets(setsToRroc):
    for objSet in setsToRroc:
        if pmc.attributeQuery("exportEnable",n=objSet,ex=1)==0:
            pmc.addAttr(objSet,ln="exportEnable",at="bool",dv=1)
        if pmc.attributeQuery("exportJobTitle",n=objSet,ex=1)==0:
            pmc.addAttr(objSet,ln="exportJobTitle",dt="string")
            pmc.setAttr(objSet+".exportJobTitle",objSet.replace("_AlembicOP",""))
        if pmc.attributeQuery("animState",n=objSet,ex=1)==0:
            pmc.addAttr(objSet,ln="animState",at="bool",dv=1)
        if pmc.attributeQuery("exportStartFrame",n=objSet,ex=1)==0:
            pmc.addAttr(objSet,ln="exportStartFrame",at="double",dv=pmc.playbackOptions(q=1,min=1))
        if pmc.attributeQuery("exportEndFrame",n=objSet,ex=1)==0:
            pmc.addAttr(objSet,ln="exportEndFrame",at="double",dv=pmc.playbackOptions(q=1,max=1))
        if pmc.attributeQuery("exportFilePath",n=objSet,ex=1)==0:
            pmc.addAttr(objSet,ln="exportFilePath",dt="string")
            pmc.setAttr(objSet+".exportFilePath",pmc.workspace.getPath()+"/cache/alembic/"+pmc.getAttr(objSet+".exportJobTitle")+".abc")
        
def trv_getFrameRange():
    srartFrame=pmc.playbackOptions(q=1,min=1)
    endFrame=pmc.playbackOptions(q=1,max=1)
    return srartFrame,endFrame

def trv_getExportFilePath(fileName):
    filePath=pmc.workspace.getPath()+"/cache/Alembic/"
    ExprtFilePath=filePath+fileName#pmc.workspace
    return ExprtFilePath

def setGlobalPathOveride(objSet):
    getGlobalExprtPath=pmc.textScrollList("glbOvrdPath",q=1,fi=1)
    getPathFrmAttr=pmc.getAttr(setName+".exportFilePath")
    if ("/" in getPathFrmAttr) & getPathFrmAttr.endswith(".abc") !=1:
        getPathFrmAttr=pmc.workspace.getPath()+"/cache/alembic/"+pmc.getAttr(objSet+".exportJobTitle")+".abc"
    if ("/" in getGlobalExprtPath):
        if (getGlobalExprtPath.endswith("/"))==0:
            getGlobalExprtPath+="/"
        import os
        ExportFilePath=getGlobalExprtPath+os.path.basename(getPathFrmAttr)
    else:
        ExportFilePath=getGlobalExprtPath+pmc.getAttr(objSet+".exportJobTitle")+".abc"
    return ExportFilePath
    
def getABCOPSets(setsLs,useOvrdPth):
    setsAssemble=[]
    for setName in setsLs:
        if pmc.attributeQuery("exportEnable",n=setName,ex=1):
            ExprtEnable=pmc.getAttr(setName+".exportEnable")
        else:
            ExprtEnable=1
        if pmc.attributeQuery("exportJobTitle",n=setName,ex=1):
            getSetName=pmc.getAttr(setName+".exportJobTitle")
        else:
            getSetName=setName.replace("_AlembicOP","")
        if pmc.attributeQuery("exportStartFrame",n=setName,ex=1):
            ExprtStartFrame=pmc.getAttr(setName+".exportStartFrame")
        else:
            ExprtStartFrame=pmc.playbackOptions(q=1,min=1)
        if pmc.attributeQuery("exportEndFrame",n=setName,ex=1):
            ExprtEndFrame=pmc.getAttr(setName+".exportEndFrame")
        else:
            ExprtEndFrame=pmc.playbackOptions(q=1,max=1)
        if pmc.attributeQuery("animState",n=setName,ex=1):
            if pmc.getAttr(setName+".animState")==0:
                ExprtEndFrame=ExprtStartFrame
        else:
            pass
        if useOvrdPth:
            ExprtFilePath=setGlobalPathOveride(setName)
        else:
            if pmc.attributeQuery("exportFilePath",n=setName,ex=1):
                ExprtFilePath=pmc.getAttr(setName+".exportFilePath")
            else:
                ExprtFilePath=trv_getExportFilePath(getSetName)
        assmb=[setName,getSetName,ExprtStartFrame,ExprtEndFrame,ExprtFilePath,ExprtEnable]
        setsAssemble.append(assmb)
    return setsAssemble
    
def getJobLst():
    try:
        len(getABCOPSets())>0
    except:
        return ["WTF"]
    else: 
        return getABCOPSets()
        
def makeSurePluginsExistAndLoaded(pluginsLs):
    for plugin in pluginsLs:
        if pmc.pluginInfo(plugin,q=1,l=1)==0:
            pmc.loadPlugin(plugin)
            
def trv_exportToABCAction(exprtJobLs):
    jobStr=[]
    for task in exprtJobLs:
        if task[5]==1:
            setMembr=pmc.sets(task[0],q=1)
            ExprtFilePath=" -f \""+trv_getExportFilePath(task[1])
            ExprtFlags="-sn -uv -ws -wfs "
            ExprtRootOption=""
            for obj in setMembr:
                objStr=pmc.ls(obj,r=1)[0].longName()
                ExprtRootOption+=("-rt "+str(objStr)+" ")
            ExprtFrameRange=" -fr "+str(task[2])+" "+str(task[3])
            
            jobStr.append(ExprtFlags+ExprtRootOption+ExprtFrameRange+str(ExprtFilePath))
    makeSurePluginsExistAndLoaded(["AbcExport"])
    if pmc.checkBoxGrp("GlbOptsCBxGrp",q=1,v1=1)==1:
        pmc.refresh(su=1)
    pmc.AbcExport(v=1,j=jobStr)
    pmc.refresh(su=0)
    
def cacheDir():
    getPrjDir=pmc.workspace.getPath()
    getABCSubDir=pmc.workspace(fre="alembicCache")
    if getPrjDir.endswith("/")==0:
        getPrjDir+="/"
    if len(getABCSubDir)>0:
        getPrjDir+=(getABCSubDir+"/")
    return getPrjDir
        
def addJobItmToLst(fLst):# fLst???
    pmc.textScrollList("lstCSTsl",e=1,ra=1)
    for job in fLst:
        if job[5]!=0:
            pmc.textScrollList("lstCSTsl",e=1,append=job[1],utg=job[0])
            
def refreshJobLsCmd():
    addJobItmToLst(getABCOPSets(filterJobSetLs("*_AlembicOP*"),0))
    
def clickItmAction():
    sel=pmc.textScrollList("lstCSTsl",q=1,si=1)
    #refreshJobLsCmd()#
    pmc.textScrollList("lstCSTsl",e=1,si=sel)
    pmc.select(pmc.textScrollList("lstCSTsl",q=1,sut=1),ne=1)
    
def doubleClickAction():
    sel=pmc.textScrollList("lstCSTsl",q=1,si=1)
    refreshJobLsCmd()
    pmc.textScrollList("lstCSTsl",e=1,si=sel)
    pmc.select(pmc.textScrollList("lstCSTsl",q=1,sut=1))

def addNewExprtJobAction():
    addAttrsToExprtSets(createNewExprtJobSet())
    addJobItmToLst()
    
def ovrdPathSwthCmd(onoff):
    pmc.textFieldButtonGrp("glbOvrdPath",e=1,en=onoff)

def openFileDialogForOvrdPth():
    getStartDir=pmc.fileDialog2(fm=2,dir=cacheDir())
    pmc.textFieldButtonGrp("glbOvrdPath",e=1,fi=getStartDir[0]+"/")

def exprtToABCWinUI():
    addAttrsToExprtSets(filterJobSetLs("*_AlembicOP*"))
    if pmc.window("exprtToABCWin",ex=1):
        pmc.deleteUI("exprtToABCWin",wnd=1)
    pmc.window("exprtToABCWin",t="TVC Export to ABC")
    pmc.columnLayout("tvcABCMainLyt",cat=("both",6),w=400,rs=9,adj=0)
    pmc.text("jobLsTxt",l="Export Jobs List: ")
    pmc.textScrollList("lstCSTsl",ams=1,nr=20,w=388,npm=3,sc="clickItmAction()",dcc="doubleClickAction()")
    pmc.rowLayout("lsOprtRwLyt",w=388,nc=2)
    pmc.button("addJobBtn",l="+ Add New Export Job",c="addNewExprtJobAction()",w=190,p="lsOprtRwLyt")
    pmc.button("rfsJobLsBtn",l="*Refresh JobList",c="refreshJobLsCmd()",w=190,p="lsOprtRwLyt")
    pmc.checkBoxGrp("GlbOptsCBxGrp",l="Global Options: ",l1="Halt viewport when caching",p="tvcABCMainLyt",
        l2="Overide export path",ncb=2,w=388,vr=1,on2="ovrdPathSwthCmd(1)",of2="ovrdPathSwthCmd(0)")
    pmc.textFieldButtonGrp("glbOvrdPath",p="tvcABCMainLyt",l="Global Path:",fi=cacheDir(),bl="Browse..",bc="openFileDialogForOvrdPth()",cw3=[80,250,58],w=388,en=0)
    refreshJobLsCmd()#filterJobSetLs("*_AlembicOP*"))
    pmc.button("goCCCmd",l="Cache to ABC",w=388,c="trv_exportToABCAction(getJobLst()",p="tvcABCMainLyt",bgc=[0.4,0.28,0.2])
    pmc.showWindow("exprtToABCWin")

exprtToABCWinUI()

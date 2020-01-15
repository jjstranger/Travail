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
    
def creatNewExprtJobSets():
    objSet=pmc.sets(pmc.ls(sl=1),n="objSet_AlembicOP")
    if pmc.attributeQuery("exportEnable",n=objSet,ex=1)==1:
        pmc.deleteAttr(objSet,at="exportEnable")
    pmc.addAttr(objSet,ln="exportEnable",at="bool",dv=1)
    if pmc.attributeQuery("exportJobTitle",n=objSet,ex=1)==1:
        pmc.deleteAttr(objSet,at="exportJobTitle")
    pmc.addAttr(objSet,ln="exportJobTitle",dt="string")
    pmc.setAttr(objSet+".exportJobTitle",objSet.replace("_AlembicOP",""))
    if pmc.attributeQuery("animState",n=objSet,ex=1)==1:
        pmc.deleteAttr(objSet,at="animState")
    pmc.addAttr(objSet,ln="animState",at="bool",dv=1)
    if pmc.attributeQuery("exportStartFrame",n=objSet,ex=1)==1:
        pmc.deleteAttr(objSet,at="exportStartFrame")
    pmc.addAttr(objSet,ln="exportStartFrame",at="double",dv=pmc.playbackOptions(q=1,min=1))
    if pmc.attributeQuery("exportEndFrame",n=objSet,ex=1)==1:
        pmc.deleteAttr(objSet,at="exportEndFrame")
    pmc.addAttr(objSet,ln="exportEndFrame",at="double",dv=pmc.playbackOptions(q=1,max=1))
    if pmc.attributeQuery("exportFilePath",n=objSet,ex=1)==1:
        pmc.deleteAttr(objSet,at="exportFilePath")
    pmc.addAttr(objSet,ln="exportFilePath",dt="string")
    pmc.setAttr(objSet+".exportFilePath",pmc.workspace.getPath()+"/cache/alembic/"+pmc.getAttr(objSet+".exportJobTitle")+".abc")
    
def trv_getFrameRange():
    srartFrame=pmc.playbackOptions(q=1,min=1)
    endFrame=pmc.playbackOptions(q=1,max=1)
    return srartFrame,endFrame
    print ("frameRange:"+srartFrame+","+endFrame)

def trv_getExportFilePath(fileName):
    filePath=pmc.workspace.getPath()+"/cache/Alembic/"
    #fileName="AbcExprtTest_v001.abc"
    ExprtFilePath=filePath+fileName#pmc.workspace
    return ExprtFilePath
    print "Exprt Filr Path: "+ExprtFilePath+".abc"

def getABCOPSets():
    setsLs=pmc.ls("*_AlembicOP*",set=1,r=1)
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
        if pmc.attributeQuery("exportFilePath",n=setName,ex=1):
            ExprtFilePath=pmc.getAttr(setName+".exportFilePath")
        else:
            ExprtFilePath=trv_getExportFilePath(getSetName)
        assmb=[setName,getSetName,ExprtStartFrame,ExprtEndFrame,ExprtFilePath,ExprtEnable]
        setsAssemble.append(assmb)
        
    return setsAssemble
    print "set List: "+setsAssemble

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
            print "Selection To Export: "+selLst
    else: 
        return getABCOPSets()
        print "Sets to export: "+getABCOPSets()

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

    pmc.AbcExport(v=1,j=jobStr)
    #print (jobStr)
#trv_exportToABCAction(getJobLst())
def exprtToABCWinUI():
    if pmc.window("exprtToABCWin",ex=1):
        pmc.deleteUI("exprtToABCWin",wnd=1)
    pmc.window("exprtToABCWin",t="TVC Export to ABC")
    pmc.columnLayout("tvcABCMainLyt",cat=("both",6),w=400,rs=3)
    pmc.text("jobLsTxt",l="Export Jobs List: ")
    #pmc.treeView("jobLsTrVw",ai=(["AAA",""],["BB","AAA"]),h=100,w=388,nb=1)
    pmc.textScrollList("lstCSTsl",ams=1,nr=20,w=388)
    pmc.button("goCCCmd",l="Cache to ABC",w=388,c="trv_exportToABCAction(getJobLst()")
    
    
    pmc.showWindow("exprtToABCWin")

exprtToABCWinUI()

###############################################
#     Alembic cache tool by A. Kovalev; www.alekseikovalev.com
#     Edit by:JJ.S at 2017.5.5
###############################################

import pymel.core as pmc
#import pymel.util
import maya.cmds as cmds
import maya.mel as mel
import random
from os import listdir
from os.path import isfile, join

timeSliderStart=cmds.playbackOptions(q=1,min=1)
timeSliderEnd=cmds.playbackOptions(q=1,max=1)
renderSettingStart=cmds.getAttr("defaultRenderGlobals.startFrame")
renderSettingEnd=cmds.getAttr("defaultRenderGlobals.endFrame")
currentFrame=cmds.currentTime(q=1) 

projectPath = cmds.workspace( q=True, rd=True ) + "cache/alembic/"

def add_attr_id():
    
    selectedObj = cmds.ls(sl=1,dag=1,s=1)
    if len(selectedObj)==0:
        pmc.error("You Select Nothing!")

    pmc.textFieldButtonGrp('abcPath',q=1,fi=1)
    sceneName = cmds.file ( q=True, sn=True, shn=True).split('.mb')
    getSvRoot=pmc.textFieldButtonGrp('abcPath',q=1,fi=1)
    
    
    getSvRoot.endswith('/')#<<<<<<<<<<<<<<<<<<<<<<<<<<
    if (getSvRoot.endswith('/'))!=1:#<<<<<<<<<<<<<<<<<<<<<<
        getSvRoot+='/'

    #print getSvRoot
    path = getSvRoot + "shaders/"
    pathFile = getSvRoot + str(sceneName[0]) + ".abc"
    
    print path
    print pathFile
    
    
    for i in selectedObj:
        aRandom=random.randint(0, 5000)
        bRandom=random.randint(0, 5000)
        cRandom=random.randint(0, 5000)
        id = aRandom*bRandom*cRandom
        time = cmds.date(f="YYYYMMDDhhmmss")
        id = "id" + str(id) + time
        attributes = cmds.listAttr(i)
        if "Alembic_id" in attributes:
            cmds.setAttr(i + ".Alembic_id", id, type="string")
        else:
            cmds.addAttr(i, longName='Alembic_id', dt="string")
            cmds.setAttr(i + ".Alembic_id", id, type="string")
            
        id=cmds.getAttr(i+".Alembic_id")
        interO = cmds.getAttr(i + '.intermediateObject')
        if interO != True:
            shaders_export(id, i, path)

    attrName = "Alembic_id"
    attrName_2 = "Face_id"
    #frameRange = [str(pmc.playbackOptions(min=True, q=True)), str(pmc.playbackOptions(max=True, q=True))]
    frameRange = [str(cmds.textFieldGrp('startFrame',q=1,tx=1)),str(cmds.textField('endFrame' ,q=1,tx=1))]
    alembic_export(selectedObj, frameRange[0], frameRange[1], pathFile, attrName, attrName_2)

def shaders_export(id, shape, path):

    attributes = cmds.listAttr(shape)
    shadingGrp = cmds.listConnections(shape,type='shadingEngine')
    if shadingGrp != None:
        lenShadingGrp=''
        lenShadingGrp = len(shadingGrp)
        ShapeListSG =[]
        
        if lenShadingGrp > 1:
            if "Face_id" in attributes:
                #print "ok"
                pass
            else:
                cmds.addAttr(shape, longName='Face_id', dt="string")
            
            shadingGrp = list(set(shadingGrp))
            
            for j in shadingGrp:
                cmds.hyperShade(o = j)
                assignSelected = cmds.ls(sl=1)
                SuperAttr = j + id + "#"
                
                for t in assignSelected:
                    if ".f" in t:
                        t_tmp = t.split(".f")
                        t = t_tmp[0].rpartition(':')[2]
                        t = t + ".f" + t_tmp[1]
                        vertexes = cmds.polyEvaluate( shape, v=True )
                        t = t + "$vertexes" + str(vertexes) + "$"
                        #t = "{}.f" + t_tmp[1] 
                        SuperAttr = SuperAttr + t + ","
                ShapeAttr = cmds.getAttr(shape + '.Face_id')
                
                                
                if ShapeAttr == None:
                    ShapeAttr = ''
                cmds.setAttr(shape + '.Face_id', ShapeAttr + "@" + SuperAttr, type="string")
                
            shader = cmds.ls(cmds.listConnections(shadingGrp),materials=1)
            shaderSG = shadingGrp + shader
            cmds.select(shaderSG, r=True, ne=True)
                
            cmds.file (path + id + ".mb", es=True, type='mayaBinary')

        if lenShadingGrp == 1:
            shader = cmds.ls(cmds.listConnections(shadingGrp),materials=1)
            shaderSG = shadingGrp + shader
            cmds.select(shaderSG, r=True, ne=True)
            cmds.file (path + id + ".mb", es=True, type='mayaBinary')
        print (path + id + ".mb")


def alembic_export(selectedObj, frameRange_s, frameRange_e, pathFile, attrName, attrName_2):

    if pmc.pluginInfo ('AbcExport',q=1,l=1)==0:
        pmc.loadPlugin('AbcExport')

    for r in selectedObj:
        interO = cmds.getAttr(r + '.intermediateObject')
        if interO == True:
            selectedObj.remove(r)
    cmds.select (selectedObj)
    groupName = "Alembic_data_group"
    expSelChk=pmc.checkBoxGrp('expSel',q=1,v1=1)
    if expSelChk==1:
        expSelOpt= " -sl "
    else:
        expSelOpt= ""
        
    if pmc.about(q=1,v=1)=='2014':
        dataFormat=''
    else:
        if pmc.radioButtonGrp('cacheFormat',q=1,sl=1)==1:
            dataFormat=' -df HDF'
        if pmc.radioButtonGrp('cacheFormat',q=1,sl=1)==2:
            dataFormat=' -df Ogawa'
    print expSelChk
    print dataFormat
    mel.eval('AbcExport -j "-frameRange ' + frameRange_s + ' ' + frameRange_e + expSelOpt + ' -uvWrite -ro -file ' + pathFile + dataFormat + ' -attr ' + attrName + ' -attr ' + attrName_2 + '";')
    for r in selectedObj:
        try:
            cmds.deleteAttr(r + '.Alembic_id')
        except:
            pass
        try:
            cmds.deleteAttr(r + '.Face_id')
        except:
            pass
    print "Done!"

def exportBrowse():

    #subPath = cmds.workspace( q=True, rd=True )
    
    svRoot = pmc.fileDialog2(fileMode=3, caption="Choose Folder", dir=projectPath)
    #DirPath = DirPath and os.path.normpath(DirPath[0])
    svRoot = svRoot and svRoot[0].replace('\\', '/')
    #print DirPath
    #print "_____________________"
    pmc.textFieldButtonGrp('abcPath',e=1,tx=svRoot)

def importBrowse():

    #subPath = cmds.workspace( q=True, rd=True )
    
    DirPath = cmds.fileDialog2(fileMode=3, caption="Choose Folder", dir=projectPath)
    #DirPath = DirPath and os.path.normpath(DirPath[0])
    DirPath = DirPath and DirPath[0].replace('\\', '/')
    #print DirPath
    #print "_____________________"
    import_alembic(DirPath)

def import_alembic(DirPath):
    if pmc.pluginInfo ('AbcImport',q=1,l=1)==0:
        pmc.loadPlugin('AbcImport')
        
    pathFile=''
    path = DirPath + "//shaders//"
    onlyfiles = [ f for f in listdir(DirPath) if isfile(join(DirPath,f)) ]
    #print onlyfiles
    
    for files in onlyfiles:
        if ".abc" in files:
            pathFile = DirPath + "//" + files
            
    
    cmds.group( em=True, name='Alembic_data_group' )
    groupName = '|Alembic_data_group'
    #print pathFile
    mel.eval('AbcImport -mode import -reparent "{}" "{}";'.format(groupName, pathFile))
    #print pathFile
    
    myGroup = "Alembic_data_group"
    children = cmds.listRelatives(myGroup, allDescendents=True, noIntermediate=True, fullPath=True)
    InGroup = cmds.ls(children, type="mesh")
    listFiles = cmds.getFileList( folder=path )
    
    for i in InGroup:
        id = cmds.getAttr(i + ".Alembic_id")
        for s in listFiles:
            if id in s:
                cmds.file(path + s, i=True, ns="id_" + id)
                
    AllShaders = cmds.ls(mat=True)
    
    for s in InGroup:
        #set_attrs(s)
        allAttrs = cmds.listAttr(s)
        id = cmds.getAttr(s + ".Alembic_id")
        
        if "Face_id" not in allAttrs:
            for shader in AllShaders:
                shadingGrp = cmds.listConnections(shader,type='shadingEngine')
                if shadingGrp != None:
                    if id in shadingGrp[0]:
                        cmds.sets(s, e=1, forceElement=shadingGrp[0])
                            
        if "Face_id" in allAttrs:
            finalSG =[]
            faceID = cmds.getAttr(s + ".Face_id")
            faceID_SG = faceID.split("@")
            for n in faceID_SG:
                faceID_SG = n.split("#")
                for g in faceID_SG:
                    faces_tmp = g.split(",")
                    for u in faces_tmp:
                        faces = u.split("$")
                        for e in faces:
                            if e != "":
                                if id in e:
                                    finalSG = e.split(id)
                                if ".f[" in e:
                                    FinalFaces = e
                                    if len(finalSG)>1:
                                        if finalSG[0] != "initialShadingGroup":
                                            for shader in AllShaders:
                                                shadingGrp = cmds.listConnections(shader,type='shadingEngine')
                                                if shadingGrp != None:
                                                    if finalSG[0] in shadingGrp[0]:
                                                        FinalFacesLongName = cmds.ls (s, long = True)
                                                        vertexes = cmds.polyEvaluate(FinalFacesLongName[0], v=True )
                                                        splitVertexes = faces[1].split("vertexes")
                                                        FinalFacesSplit = FinalFaces.split(".f")
                                                        FinalFacesObj = str(FinalFacesLongName[0]) + ".f" + str(FinalFacesSplit[1])
                                                        if str(vertexes) == str(splitVertexes[1]):
                                                            try:
                                                                cmds.sets(FinalFacesObj, e=1, forceElement=shadingGrp[0])
                                                            except:
                                                                pass
    renameShaders()           

def renameShaders():
    myGroup = "Alembic_data_group"
    children = cmds.listRelatives(myGroup, allDescendents=True, noIntermediate=True, fullPath=True)
    InGroup = cmds.ls(children, type="mesh")
    for i in InGroup:
        transform = cmds.listRelatives(i,type='transform',p=True)
        shadingGrp = cmds.listConnections(i,type='shadingEngine')
        shader = cmds.ls(cmds.listConnections(shadingGrp), materials=1)
        try:
            cmds.rename(shader[0], transform[0] + "_mat")
            cmds.rename(shadingGrp[0], transform[0] + "_matSG")
        except:
            pass

        
'''
def alembic_cache_tool():
    if cmds.window('alembic_cache_tool', exists=True):
        cmds.deleteUI('alembic_cache_tool', window=True)
        try:
            cmds.windowPref( 'alembic_cache_tool', r=True )
        except:
            pass
            
    win = cmds.window('alembic_cache_tool', h=52, w=300, te=300, le=500, s=0, title="Alembic Cache Tool")
    
    AllrowColumnLayout = cmds.rowColumnLayout( numberOfRows=1, rowHeight=[(1, 50)])
    
    button_create_alembic = cmds.button ('create_alembic', p=AllrowColumnLayout, label="Create Alembic Cache", h=30, w=150, bgc= (0.8, 0.7, 0.9), c="add_attr_id()")
    button_load_alembic = cmds.button ('load_alembic', p=AllrowColumnLayout, label="Load Alembic Cache", h=30, w=150, bgc= (0.8, 0.7, 0.8), c="dirBrowse()")
    
    cmds.setParent( '..' )
    cmds.showWindow( win )
    
alembic_cache_tool()
'''


def tvc_abcExpUI():
    
    if pmc.window('abcExpWin', exists=True):
        pmc.deleteUI('abcExpWin', window=True)
        try:
            pmc.windowPref('abcExpWin', r=True )
        except:
            pass
    
    abcExpWin = pmc.window('abcExpWin',title="TVC Alembic Cache Exporter v0.01 -JJ.S",w=300, h=100,s=0)
    abcExpLyt=pmc.columnLayout('abcExpLyt')
    pmc.separator(h=20)
    expSel=pmc.checkBoxGrp('expSel',ncb=1,l="Export Selected: ")
    pmc.separator(h=10,style="none")
    cacheTime=pmc.radioButtonGrp('cacheTime',numberOfRadioButtons=4,l="Cache Time: ",labelArray4=["Current Frame","Render Settings","Time Slider","Start/End"],sl=1,vr=1)
    startFrame=pmc.textFieldGrp('startFrame',l="Start/End: ",cw=[2,80],tx=int(currentFrame))
    
    endFrame=pmc.textField('endFrame',w=80,p=startFrame,tx=int(currentFrame))
    #byFrame=pmc.textFieldGrp('byFrame',l="by: ",cw=[2,80])
    pmc.separator(h=10,style="none")
    cacheFormat=pmc.radioButtonGrp('cacheFormat',numberOfRadioButtons=2,l="Cache Format: ",labelArray2=["HDF5","Ogawa"])

    abcPath=pmc.textFieldButtonGrp('abcPath',l="Save to: ",tx=projectPath,bl="Browse",bc="exportBrowse()")
    #pmc.separator(h=10,style="none")
    okBtnRwLyt=pmc.rowLayout('okBtnRwLyt',nc=2,h=40,cw2=(320,100))
    pmc.separator(h=10,style="none")
    okBtn=pmc.button(l='Go Cache!',w=80,c="add_attr_id()")
    ####Int Value####

    expSel.setValue1(1)
    startFrame.setEnable(0) 
    pmc.radioButtonGrp(cacheTime,e=1,onCommand1="pmc.textFieldGrp('startFrame',e=1,tx=int(currentFrame),en=0);pmc.textField('endFrame',e=1,tx=int(currentFrame),en=0)")
    pmc.radioButtonGrp(cacheTime,e=1,onCommand2="pmc.textFieldGrp('startFrame',e=1,tx=int(renderSettingStart),en=0);pmc.textField('endFrame',e=1,tx=int(renderSettingEnd),en=0)")
    pmc.radioButtonGrp(cacheTime,e=1,onCommand3="pmc.textFieldGrp('startFrame',e=1,tx=int(timeSliderStart),en=0);pmc.textField('endFrame',e=1,tx=int(timeSliderEnd),en=0)")
    pmc.radioButtonGrp(cacheTime,e=1,onCommand4="pmc.textFieldGrp('startFrame',e=1,en=1);pmc.textField('endFrame',e=1,en=1)")
    #byFrame.setText("1")

    if pmc.about(q=1,v=1)=='2014':
        cacheFormat.setSelect(1)
        cacheFormat.setEnable2(0)
        cacheFormat.setLabel2("Invalid for 2014")
    else:
        cacheFormat.setSelect(2)

    pmc.showWindow(abcExpWin)

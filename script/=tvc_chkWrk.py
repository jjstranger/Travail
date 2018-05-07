# coding=utf-8
# TVC Check Work
#     Ver : 0.01
#     Create by : JJS
#     at : 2017.5.16
# Check Maya files for production.

import pymel.core as pmc
import os
#from travailGlobalSettings import *
from collections import Counter  
tvcRoot = "D:/prjTst/"


def mdHistoryChk():
    dirtHistryObjLst=[]
    objLst=pmc.ls(type='mesh')
    objLst+=(pmc.ls(type='nurbsSurface'))
    histrLstNew=[]
    print '========== History Check ==========\n'
    for item in objLst:
        histrLst=pmc.listHistory(item)
        for hsItem in histrLst:
            if pmc.objectType(hsItem) not in ('groupId','mesh','shadingEngine','objectSet','nurbsSurface'):
                print '    '+hsItem
                histrLstNew.append(hsItem)

        if len(histrLstNew) >0:
            dirtHistryObjLst.append(item)
            print item+' [Mesh with History.]'
    #print len(dirtHistryObjLst)
    if len(dirtHistryObjLst)>0:
        pmc.textField('hstryChkTxF',e=1,tx=str(len(dirtHistryObjLst))+' Dirties',bgc=(1,0,0))
    else:
        pmc.textField('hstryChkTxF',e=1,tx='Good',bgc=(0,1,0))
        print 'all good!'
    print "\n";
    return dirtHistryObjLst
    
def mdHstryFxBtn():
    getMdHsrtyDrtLst=mdHistoryChk()
    pmc.delete(getMdHsrtyDrtLst,ch=1)
    
def mdHstrySlDrt():
    getMdHsrtyDrtLst=mdHistoryChk()
    pmc.select (getMdHsrtyDrtLst)
    
def mdNmRptChk():
    dirtNmRptObjLst=[]
    objLst=pmc.ls(s=0,tr=1,ca=0,lt=0)
    objLstNew=[]
    #rptNmLst=[]
    print '========== Name Repeat Check ==========\n'
    for item in objLst:
        getChildName=item.rpartition('|')
        objLstNew.append(getChildName[2])
    count=Counter(objLstNew)
    #print objLstNew
    countLst= [ str(k)+':'+str(v) for k,v in dict(count).items() if v>1]
    for item in countLst:
        rptNm=item.rpartition(':')
        dirtNmRptObjLst.append('*'+rptNm[0])
        print rptNm[0]+' ['+rptNm[2]+' objects name with it.]'
    
    print "\n"
    if len(dirtNmRptObjLst)>0:
        pmc.textField('nmRptChkTxF',e=1,tx=str(len(dirtNmRptObjLst))+' Dirties',bgc=(1,0,0))
    else:
        pmc.textField('nmRptChkTxF',e=1,tx='Good',bgc=(0,1,0))
        print 'all good!'
    return dirtNmRptObjLst
    #pmc.select(rptNmLst)

def mdMnRptFxBtn():
    pmc.confirmDialog (t='Auto Fix Repeat name objects',m='Hehe, Go fixing it yourself.')

def mdNmRptSlDrt():
    getMdRptNmDrtLst=mdNmRptChk()
    #print mdRptNmLstOP
    pmc.select (getMdRptNmDrtLst)
    
#########
def mdUfrzChk():
    objLst=pmc.ls(type='mesh'or'nurbs*')
    objLst.append(pmc.ls(type='locator'))
    objLstT=[]
    for objItem in objLst:
        objLstT.append(pmc.listRelatives(objItem,p=1))
    del objLstT[-1]

    #objLstT={}.fromkeys(objLstT).keys()#not work in 2014
    dirtUfrzObjLst=[]
    print '========== Unfreeze Check ==========\n'
    for item in objLstT:
        #shpLst=pmc.listRelatives(item,s=1)
        #print shpLst
        #if len(shpLst)>1:
        tx=pmc.getAttr(item[0]+'.tx')
        ty=pmc.getAttr(item[0]+'.ty')
        tz=pmc.getAttr(item[0]+'.tz')
        rx=pmc.getAttr(item[0]+'.rx')
        ry=pmc.getAttr(item[0]+'.ry')
        rz=pmc.getAttr(item[0]+'.rz')
        sx=pmc.getAttr(item[0]+'.sx')
        sy=pmc.getAttr(item[0]+'.sy')
        sz=pmc.getAttr(item[0]+'.sz')
        objXfm=[tx,ty,tz,rx,ry,rz,sx,sy,sz]
        if objXfm!=[0,0,0,0,0,0,1,1,1]:
            print item[0]+' [Mesh with dirty transform.]'
            dirtUfrzObjLst.append(item[0])
        
        shplst=pmc.listRelatives(item[0],s=1)
        if len(shplst)!=0:
            ptN=pmc.polyEvaluate(shplst[0],v=1)
            if(pmc.objectType(shplst[0])=='mesh') and (ptN>0):

                for i in range(0,int(ptN)):
                    ppos=pmc.getAttr(shplst[0]+'.vtx['+str(i)+']')
                    if ppos!=(0.0,0.0,0.0):
                        print item[0]+ ' [Mesh with dirt point value.]'
                        dirtUfrzObjLst.append(item[0]) 
                        break
                        
            if(pmc.objectType(shplst[0])=='nurbs*'):
                for i in range(0,int(pmc.getAttr((item[0]+'.cp'),s=1))):
                    ppos=pmc.getAttr(item[0]+'.cv['+str(i)+']')
                    if ppos!=(0.0,0.0,0.0):
                        print item[0]+ ' [Nurbs with dirt point value.]'
                        dirtUfrzObjLst.append(item[0])
                        break
    print "\n";
    #print 
    if len(dirtUfrzObjLst)>0:
        pmc.textField('ufrzTxF',e=1,tx=str(len(dirtUfrzObjLst))+' Dirties',bgc=(1,0,0))
    else:
        pmc.textField('ufrzTxF',e=1,tx='Good',bgc=(0,1,0))
        print 'all good!'
    return dirtUfrzObjLst

def msUfrzFxBtn():
    getMdUfrzDrtLst=mdUfrzChk()
    for item in getMdUfrzDrtLst:
        pmc.polyMoveVertex(item,localTranslate=(0,0,0))
        pmc.delete(item,ch=1)
    pmc.makeIdentity(getMdUfrzDrtLst,a=1,t=1,r=1,s=1)
    
def mdUnusdChk():
    dsply=pmc.ls(typ='displayLayer')
    dsply.remove('defaultLayer')
    rdly=pmc.ls(typ='renderLayer')
    rdly.remove('defaultRenderLayer')
    
    camLst=pmc.ls(ca=1)
    camLst=pmc.listRelatives(camLst,p=1)
    camLst.remove('front')
    camLst.remove('persp')
    camLst.remove('side')
    camLst.remove('top')
    if 'backShape' in camLst:
        camLst.remove('back')
    if 'bottom' in camLst:
        camLst.remove('bottom')
    if 'left' in camLst:
        camLst.remove('left')
    print '========== Cams, Lights, Display & Render Layers Check ==========\n'
    for item in camLst:
        print item +' [Unused cameras.]'
    
    lgtLst=pmc.ls(lt=1)
    lgtLst=pmc.listRelatives(lgtLst,p=1)
    for item in lgtLst:
        print item +' [Unused lights.]'
    dirtUnusd=camLst+lgtLst
    dirtLayers=[]
    for item in dsply:
        if len(str(item))!=0:
            dirtLayers.append(item)
            print item +' [display layers.]'
    for item in rdly:
        if len(str(item))!=0:
            dirtLayers.append(item)
            print item +' [render Layers.]'
    dirtUnusd=dirtLayers+dirtUnusd
    pmc.select(dirtUnusd)
    if len(dirtUnusd)>0:
        pmc.textField('mdUnuseLayerTxF',e=1,tx=str(len(camLst))+' cams, '+str(len(lgtLst))+' lights, '+str(len(dirtLayers))+' layers.',bgc=(1,0,0))
    else:
        pmc.textField('mdUnuseLayerTxF',e=1,tx='Good',bgc=(0,1,0))
        print 'all good!'
    return dirtUnusd

def mdUnusdClean():
    getDirtLayers=mdUnusdChk()
    pmc.delete(getDirtLayers)
    
def mdUnusdSL():
    getDirtLayers=unusdChk()
    pmc.select(getDirtLayers)
  
def anMasterCam():
    camLst=pmc.ls(ca=1)
    if 'backShape' in camLst:
        camLst.remove('backShape')
    if 'bottomShape' in camLst:
        camLst.remove('bottomShape')
    camLst.remove('frontShape')
    if 'leftShape' in camLst:
        camLst.remove('leftShape')
    camLst.remove('perspShape')
    camLst.remove('sideShape')
    camLst.remove('topShape')
    return camLst

def anMasterCamLsting():
    getAnCamLst=anMasterCam()
    lstCount=len(getAnCamLst)
    pmc.menuItem(l='Select Cam',p='anMasterCamLst')
    i=0
    for item in getAnCamLst:
        item=pmc.listRelatives(item,p=1)
        
        pmc.menuItem('camItm'+str(i),p='anMasterCamLst',l=item[0])
        i+=1
#####ios
def anCamChgCmd():
    if (pmc.optionMenu('anMasterCamLst',q=1,sl=1))==1:
    pmc.button('anRnmCamBtn',e=1,en=0)
    pmc.button('anLckCamBtn',e=1,en=0)
    pmc.button('anMasterCamBtn3',e=1,en=0)
    
    else:
    pmc.button('anRnmCamBtn',e=1,en=1)
    pmc.button('anLckCamBtn',e=1,en=1)
    pmc.button('anMasterCamBtn3',e=1,en=1)
    
###%%ios
def anMasterCamRename():
    if pmc.optionMenu("anMasterCamLst",q=1,sl=1)==1:
        pmc.confirmDialog (t='No Camera Selected.',m='Choose a Camera Ok?')
    else:
        if(pmc.window('camRenmWin',q=1,ex=1)):
            pmc.deleteUI('camRenmWin')
        pmc.window('camRenmWin',t='Camera Rename',h=100,w=400)
        pmc.columnLayout('camRnmClmLyt',w=400,en=1,rs=15,h=150,cw=300,cal='center')
        pmc.separator()
        pmc.textFieldGrp('camRnmTxF',en=1,l='Rename Camera:',tx='SCXXX_Cam_'+str(int(pmc.playbackOptions(q=1,min=1)))+'_'+str(int(pmc.playbackOptions(q=1,max=1))),ed=1,vis=1,w=400)
        pmc.checkBoxGrp('lckCamCB',l='Lock Camera',v1=1)
        #pmc.checkBoxGrp('delOthCam',l='Delete Other Camera',v1=1)
        pmc.rowLayout('btnRwLyt',p='camRnmClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center']],en=1,cw=[[1, 220], [2, 80], [3, 80]],nc=3)
        pmc.separator()
        pmc.button('canc',w=70,l='Cancel',c='pmc.deleteUI("camRenmWin")',p='btnRwLyt')
        pmc.button('goRnm',w=70,l='Ok',c='anMstCamRnOKBtn();pmc.deleteUI("camRenmWin")',p='btnRwLyt')
        pmc.showWindow('camRenmWin')

def anMstCamRnOKBtn():
    if pmc.checkBoxGrp('lckCamCB',q=1,v1=1):
        lckCam()
    pmc.rename(pmc.optionMenu("anMasterCamLst",q=1,v=1),pmc.textFieldGrp("camRnmTxF",q=1,tx=1))
    camSlt=pmc.optionMenu("anMasterCamLst",q=1,sl=1)
    pmc.deleteUI(pmc.optionMenu("anMasterCamLst",q=1,ils=1),mi=1)
    anMasterCamLsting()
    pmc.optionMenu("anMasterCamLst",e=1,sl=camSlt)

def lckCam():
    getSelCam=pmc.optionMenu('anMasterCamLst',q=1,v=1)
    pmc.setAttr(getSelCam+'.tx',lock=1)
    pmc.setAttr(getSelCam+'.ty',lock=1)
    pmc.setAttr(getSelCam+'.tz',lock=1)
    pmc.setAttr(getSelCam+'.rx',lock=1)
    pmc.setAttr(getSelCam+'.ry',lock=1)
    pmc.setAttr(getSelCam+'.rz',lock=1)

def unusedCam():
    if pmc.optionMenu("anMasterCamLst",q=1,sl=1)==1:
        pmc.confirmDialog (t='No Camera Selected.',m='Choose a Camera Ok?')
    else:
        getUnusdCamLst=anMasterCam()
        getUnusdCamLst=pmc.listRelatives(getUnusdCamLst,p=1)
        getUnusdCamLst.remove(pmc.optionMenu('anMasterCamLst',q=1,v=1))
        return getUnusdCamLst

def selUnusdCamBtn():
    getUnusdCamLst=unusedCam()
    pmc.select(getUnusdCamLst)
 
def anUnusdChk():
    dsply=pmc.ls(typ='displayLayer')
    dsply.remove('defaultLayer')
    rdly=pmc.ls(typ='renderLayer')
    rdly.remove('defaultRenderLayer')
    print '========== Lights, Display & Render Layers Check ==========\n'
    lgtLst=pmc.ls(lt=1)
    lgtLst=pmc.listRelatives(lgtLst,p=1)
    for item in lgtLst:
        print item +' [unused lights.]'
    dirtUnusd=lgtLst
    dirtLayers=[]
    for item in dsply:
        if len(str(item))!=0:
            dirtLayers.append(item)
            print item +' [display layers.]'
    for item in rdly:
        if len(str(item))!=0:
            dirtLayers.append(item)
            print item +' [render Layers.]'
    dirtUnusd=dirtLayers+dirtUnusd
    pmc.select(dirtLayers)
    if len(dirtLayers)>0:
        pmc.textField('anUnusdChkTxF',e=1,tx=str(len(lgtLst))+' lights, '+str(len(dirtLayers))+' layers.',bgc=(1,0,0))
    else:
        pmc.textField('anUnusdChkTxF',e=1,tx='Good',bgc=(0,1,0))
        print 'all good!'
    return dirtUnusd

def anUnusdClean():
    getDirtLayers=mdUnusdChk()
    pmc.delete(getDirtLayers)
    
def anUnusdSL():
    getDirtLayers=mdUnusdChk()
    pmc.select(getDirtLayers)

def txImgChk():
    txImgLst=pmc.ls(typ='file')
    dirtTxImgLst=[]
    print '========== Texture Images Check ==========\n'
    for item in txImgLst:
        if os.path.exists(pmc.getAttr(item+'.fileTextureName'))==0:
        print pmc.getAttr(item+'.fileTextureName')+' is missing.'
        dirtTxImgLst.append(item)
    if len(dirtTxImgLst)>0:
        pmc.textField('txChkTxF',e=1,tx=str(len(dirtTxImgLst))+' missing textures.',bgc=(1,0,0))
        pmc.textField('anTxChkTxF',e=1,tx=str(len(dirtTxImgLst))+' missing textures.',bgc=(1,0,0))
    else:
        pmc.textField('txChkTxF',e=1,tx='Good',bgc=(0,1,0))
        pmc.textField('anTxChkTxF',e=1,tx='Good',bgc=(0,1,0))
        return dirtTxImgLst
        
def txDCC():
    getTxNodNm=pmc.textScrollList('txLst',q=1,sl=1)[0].split('    ')
    pmc.select(getTxNodNm[1])
    pmc.runtime.AttributeEditor()

def txImgDtBtn(lanSW):
    pmc.runtime.FilePathEditor()
    
def txImgSlBtn():
    getDiirtTxImgLst=txImgChk()
    pmc.select(getDiirtTxImgLst)
    
def txPathResetBtn():
    getTxSlLs=pmc.textScrollList('txLst',q=1,si=1)
	for item in getTxSlLs:
	    nodeNm=item.split('    ')[1]
	    txPath=item.split('    ')[2]
    
def getPrjLst(tvcRoot):

    prjList=pmc.getFileList(folder=tvcRoot,fs="3???_*")
    
    if "3000_PN_JobName" in prjList:
        prjList.remove("3000_PN_JobName")
    if "3000_PN_JobName_Test" in prjList:
        prjList.remove("3000_PN_JobName_Test")
        prjList.sort()
        prjList.reverse()
    return prjList
    
def getAssetLst():
    assMenuItms = pmc.optionMenu('assTypLs', q=1, itemListLong=1)
    if assMenuItms:
        pmc.deleteUI(assMenuItms)
    getPrjNm=pmc.optionMenu ('prjLst',q=1,v=1)
    assPathCH=tvcRoot+getPrjNm+'/VFX/assets/models/characters/'
    assPathPR=tvcRoot+getPrjNm+'/VFX/assets/models/props/'
    assPathST=tvcRoot+getPrjNm+'/VFX/assets/models/sets/'

    assChLst=os.listdir(assPathCH)
    assPrLst=os.listdir(assPathPR)
    assStLst=os.listdir(assPathST)


    pmc.menuItem (l="Please Select...",p='assTypLs')
    pmc.menuItem (l="== Characters ==",en=0,p='assTypLs')

    for item in assChLst:
        pmc.menuItem (l=item,en=1,p='assTypLs',c='asItmTyp="Characters"')


    pmc.menuItem (l="== Props ==",en=0,p='assTypLs')
    for item in assPrLst:
        pmc.menuItem (l=item,en=1,p='assTypLs',c='asItmTyp="Props"')
    pmc.menuItem (l="== Sets ==",en=0,p='assTypLs')
    for item in assStLst:
        pmc.menuItem (l=item,en=1,p='assTypLs',c='asItmTyp="Sets"')

def getScLst():
    scMenuItms= pmc.optionMenu('anScLst', q=1, itemListLong=1)
    if scMenuItms:
        pmc.deleteUI(scMenuItms)
    getPrjNm=pmc.optionMenu ('anPrjLst',q=1,v=1)
    scPath=tvcRoot+getPrjNm+'/VFX/sequences/'
    scLst=os.listdir(scPath)
    scLst.sort()
    pmc.menuItem (l="None",p='anScLst')
    for item in scLst:
        pmc.menuItem (l=item,en=1,p='anScLst')

def getShLst():
    shMenuItms= pmc.optionMenu('anShLst', q=1, itemListLong=1)
    if shMenuItms:
        pmc.deleteUI(shMenuItms)
    getPrjNm=pmc.optionMenu ('anPrjLst',q=1,v=1)
    getScNm=pmc.optionMenu ('anScLst',q=1,v=1)
    shPath=tvcRoot+getPrjNm+'/VFX/sequences/'+getScNm+'/'
    shLst=os.listdir(shPath)
    shLst.sort()
    pmc.menuItem (l="None",p='anShLst')
    for item in shLst:
        pmc.menuItem (l=item,en=1,p='anShLst')
        
def svAssFile():
    getPrjNm=pmc.optionMenu ('prjLst',q=1,v=1)
    assLst=pmc.optionMenu('assTypLs',q=1,ill=1)
    getAssNm= pmc.optionMenu('assTypLs',q=1,v=1)
    getAssSlId=pmc.optionMenu('assTypLs',q=1,sl=1)
    getAssTypData=pmc.menuItem(assLst[getAssSlId -1],q=1,da=1)
    if getAssTypData==0:
    	asItmTyp='characters'
    if getAssTypData==1:
    	asItmTyp='props'
    if getAssTypData==2:
    	asItmTyp='sets'

    getFileTyp=pmc.optionMenu ('asSvFlType',q=1,v=1)
    getFileNm=pmc.textField('asflNm',q=1,tx=1)
    #pmc.saveAs(tvcRoot+getPrjNm+'/VFX/assets/models/'+asItmTyp+'/'+getFileTyp+'/'+getFileNm) 
    AssetFileName=tvcRoot +getPrjNm+'/VFX/assets/models'+asItmTyp+'/'+getAssNm+'/'+getFileTyp+'/'+getFileNm+'.mb'
    AssetHisPath=tvcRoot +getPrjNm+'/VFX/assets/models'+asItmTyp+'/'+getAssNm+'/'+getFileTyp+'/pubHistory/'
    if os.path.exists(AssetFileName):
    	if os.path.exists(AssetHisPath)==0:
    		os.mkdir(AssetHisPath)
    		pmc.sysFile(AssetFileName,ren=AssetHisPath+getFileNm+'_v001'+'.mb')
    	else:
    		assPubFlHisLst=pmc.getFileList(folder=AssetHisPath,fs=getFileNm+'_v???.mb')
    		if len(list(assPubFlHisLst))>0:
    			maxCurVerFlNm=max(assPubFlHisLst)
    			maxCurVerNum=maxCurVerFlNm[-6:-3]
    			fileVer='{:0>3d}'.format(int(maxCurVerNum)+1)
    			pmc.sysFile(AssetFileName,ren=AssetHisPath+getFileNm+'_v'+fileVer+'.mb')
    			print 'Current file move to: '+AssetHisPath+getFileNm+'_v'+fileVer+'.mb'
    pmc.saveAs(AssetFileName)
    print 'File published as: '+AssetFileName

def svAnFile(): 
	#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
######## UI ########

def tvcChkWrkUI():
    if(pmc.window('TVC_SubChk',q=1,ex=1)):
        pmc.deleteUI('TVC_SubChk')
    pmc.window('TVC_SubChk',s=0,t='TVC Check Work',h=430,w=600,tb=1,mb=1)
    #####  Tabs
    pmc.tabLayout('tvcChkTabLyt',en=1)
    #####  Model Chk
    pmc.columnLayout('mdChkClmLyt',w=600,en=1,rs=10,h=430)
    pmc.separator()
    ##  history
    pmc.rowLayout('hstryChkRwLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=5)
    pmc.text('hstryChkTx',w=120,en=1,al='right',l='Check herstory:')
    pmc.textField('hstryChkTxF',en=1,tx='UnChecked',ed=0,vis=1,w=200)
    pmc.button('hstryChkGochkBtn',w=70,l='Check',c='mdHistoryChk()')
    pmc.button('hstryChkAutFxBtn',w=70,l='Clean',c='mdHstryFxBtn();mdHistoryChk()')
    pmc.button('hstryChkSlFBtn',w=70,l='Select Fails',c='mdHstrySlDrt()')
    ##  name repeat
    pmc.rowLayout('nmRptChkRwLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=5)
    pmc.text('nmRptChkTx',en=1,w=120,al='right',l='Check Repeat Name:')
    pmc.textField('nmRptChkTxF',en=1,tx='UnChecked',ed=0,vis=1,w=200)
    pmc.button('nmRptChkGochkBtn',w=70,l='Check',c='mdNmRptChk()')
    pmc.button('nmRptChkAutFxBtn',w=70,l='Auto Fix',c='mdMnRptFxBtn()')
    pmc.button('nmRptChkSlFBtn',w=70,l='Select Fails',c='mdNmRptSlDrt()')
    ##  unfreezed
    pmc.rowLayout('ufrzRwLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=5)
    pmc.text('ufrzTx',en=1,w=120,al='right',l='Check Unfreezed:')
    pmc.textField('ufrzTxF',en=1,tx='UnChecked',ed=0,vis=1,w=200)
    pmc.button('ufrzGochkBtn',w=70,l='Check',c='mdUfrzChk()')
    pmc.button('ufrzAutFxBtn',w=70,l='Auto Fix',c='msUfrzFxBtn();mdUfrzChk()')
    pmc.button('ufrzSlFBtn',w=70,l='Select Fails')
    ##  Unused Objs
    pmc.rowLayout('mdUnuseLayersRwLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=5)
    pmc.text('mdUnuseLayerTx',en=1,w=120,al='right',l='Check Unused Objs:')
    pmc.textField('mdUnuseLayerTxF',en=1,w=200,tx='UnChecked',ed=0,vis=1)
    pmc.button('mdLyChk',w=70,l='Check',c='mdUnusdChk()')
    pmc.button(w=70,l='Delete All',c='mdUnusdClean();mdUnusdChk()')
    pmc.button(w=70,l='Select Fails',c='mdUnusdSL()')
    ##  texture check
    pmc.rowLayout('txChkRwLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=5)
    pmc.text('txChkTx',en=1,w=120,al='right',l='Check textures:')
    pmc.textField('txChkTx',en=1,w=200,tx='UnChecked',ed=0,vis=1,w=200)
    pmc.button('txChkGochkBtn',w=70,l='Check',c='txImgChk()')
    pmc.button('txChkAutFxBtn',w=70,l='Detail',c='txImgDtBtn(lanSw)',en=1)
    pmc.button('txChkSlFBtn',w=70,l='Select Fails',c='txImgSlBtn()')

    pmc.separator(st='in',w=600,p='mdChkClmLyt')
    ##  md batch chk all
    pmc.rowLayout('mdChkAllRwLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=4)
    pmc.separator()
    pmc.separator()
    pmc.button('mdChkAllGoChkAllBtn',w=70,l='Check All',c='mdHistoryChk();mdNmRptChk();mdUfrzChk();mdUnusdChk();print"========== Check Finished =========="')
    pmc.button('mdChkAllAutFxAllBtn',w=70,l='Auto Fix All',c='mdHstryFxBtn();mdHistoryChk();msUfrzFxBtn();mdUfrzChk();mdUnusdClean();mdUnusdChk()')
    ##### Asset Publish ########
    pmc.rowLayout('mdSbTT',p='mdChkClmLyt',nc=2)
    pmc.textField('SbTit',en=1,w=100,tx='    Asset Publish',ed=0,bgc=(.5,.5,.5),p='mdSbTT')
    pmc.separator(st='out',w=600,p='mdSbTT')
    
    pmc.rowLayout('mdPrjChsRWLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center']],en=1,cw=[[1, 120],[2, 210]],nc=2)
    pmc.text('prjChsTx',l="Project: ",w=120)
    pmc.optionMenu ('prjLst',p='mdPrjChsRWLyt',cc='getAssetLst()')
    pmc.menuItem (l="Please Select...")
    for item in getPrjLst(tvcRoot):
        pmc.menuItem (l=item)
    
    pmc.rowLayout('mdAssChsRWLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'center']],en=1,cw=[[1, 120],[2, 210]],nc=2)
    pmc.text('assLst',l="Asset: ",w=120)
    pmc.optionMenu ('assTypLs',p='mdAssChsRWLyt')


    pmc.rowLayout('mdAdAssRWLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'right'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 35],[2, 84],[3, 100],[4, 100],[5, 100]],nc=5)
    pmc.separator()
    pmc.checkBox('addAssChkBx',en=0,v=0,l='Add an asset',p='mdAdAssRWLyt',w=80,onc='pmc.optionMenu ("addAssType",e=1,en=1);pmc.textField("assNm",e=1,en=1);pmc.button("annAssBtn",e=1,en=1);pmc.optionMenu ("assTypLs",e=1,en=0)',ofc='pmc.optionMenu("addAssType",e=1,en=0);pmc.textField("assNm",e=1,en=0);pmc.button("annAssBtn",e=1,en=0);pmc.optionMenu ("assTypLs",e=1,en=1)')
    
    pmc.optionMenu('addAssType',p='mdAdAssRWLyt',w=90,en=0)
    pmc.menuItem(l="characters")
    pmc.menuItem(l="props")
    pmc.menuItem(l="sets")
    pmc.textField('assNm',pht="Give a asset name here.",w=200,p='mdAdAssRWLyt')
    pmc.button('annAssBtn',l="Add",c="goAddAssetFolders($tvcRoot)",w=100,p='mdAdAssRWLyt',en=0)
    
    pmc.rowLayout('mdSvFlLyt',p='mdChkClmLyt',cal=[[1, 'right'], [2, 'right'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 35],[2, 84],[3, 100],[4, 100],[5, 100]],nc=5)
    pmc.separator()
    pmc.text('svFlChkBx',l='Save File',p='mdSvFlLyt',w=80)
    
    pmc.optionMenu ('asSvFlType',p='mdSvFlLyt',w=90)
    pmc.menuItem (l="Mesh",en=1)
    pmc.menuItem (l="Rig",en=1)
    pmc.menuItem (l="Lighting",en=1)
    pmc.textField('asflNm',pht="Give a File name here.",tx='XXX_md.mb',w=200,p='mdSvFlLyt')
    pmc.button('annAssBtn',l="Save",c="svAssFile()",w=100,p='mdSvFlLyt')

    #pmc.rowLayout ('addAssBtLyt',numberOfColumns=2,p='mdChkClmLyt')
    #pmc.separator (w=330,st="none",p='addAssBtLyt')

    #pmc.button('addAss',l="Add it",rs=1,w=100,c="goAddAssetFolders($tvcRoot)",p='addAssBtLyt')
    #####  An Chk

    pmc.columnLayout('anChkClmLyt',p='tvcChkTabLyt',en=1,rs=10,h=150,w=600)
    pmc.separator()
    ## cam chk
    pmc.rowLayout('anMasterCam',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=5)
    pmc.text('anMasterCamTx',en=1,al='right',l='Scene Camera:',w=120)
    #pmc.textField('anMasterCamTxF',en=1,w=200,tx='UnChecked',ed=0,vis=1)
    pmc.optionMenu('anMasterCamLst',w=200)
    anMasterCamLsting()
    pmc.button('anRnmCamBtn',l='Rename',w=70,c='anMasterCamRename()')
    pmc.button('anLckCamBtn',l='Lock',w=70,c='lckCam()')
    pmc.button('anMasterCamBtn3',l='Sel Unused',w=70,c='selUnusdCamBtn()')
    ## unuesd objs
    pmc.rowLayout('anUnusdChkRwLyt',p='anChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=5)
    pmc.text('anUnusdChkTx',en=1,w=120,al='right',l='Check Unused objs:')
    pmc.textField('anUnusdChkTxF',en=1,w=200,tx='UnChecked',ed=0,vis=1)
    pmc.button('anUnusdChkBtn',w=70,l='Check',c='anUnusdChk()')
    pmc.button('anUnusdFxBtn',w=70,l='Delete All',c='anUnusdClean()')
    pmc.button('anUnusdSlBtn',w=70,l='Select Fails',c='anUnusdSL()')
    
    pmc.separator(st='in',w=600,p='anChkClmLyt')
    ## an batch
    '''
    pmc.rowLayout(p='anChkClmLyt',cal=[[1, 'right'], [2, 'center'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 120], [3, 80], [4, 80], [5, 80], [2, 210]],nc=4)
    pmc.separator()
    pmc.separator()
    pmc.button(w=70,l='Check All')
    pmc.button(w=70,l='Auto Fix All')
    '''
    ##### Shot Publish ########
    pmc.rowLayout('anSbTT',p='anChkClmLyt',nc=2)
    pmc.textField('anSbTit',en=1,w=100,tx='    Shot Publish',ed=0,bgc=(.5,.5,.5),p='anSbTT')
    pmc.separator(st='out',w=600,p='anSbTT')
    
    pmc.rowLayout('anPrjChsRWLyt',p='anChkClmLyt',cal=[[1, 'right'], [2, 'center']],en=1,cw=[[1, 120],[2, 210]],nc=2)
    pmc.text('anPrjChsTx',l="Project: ",w=120)
    pmc.optionMenu ('anPrjLst',p='anPrjChsRWLyt',cc='getScLst()')
    pmc.menuItem (l="Please Select...")
    for item in getPrjLst(tvcRoot):
        pmc.menuItem (l=item)

    pmc.rowLayout('anScShLyt',p='anChkClmLyt',cal=[[1, 'right'], [2, 'right'], [3, 'right'], [4, 'center']],en=1,cw=[[1, 120],[2, 80],[3, 50],[4, 80]],nc=4)
    pmc.text('anScTx',p='anScShLyt',l='Scene',w=120)
    pmc.optionMenu ('anScLst',p='anScShLyt',cc='getShLst()')
    pmc.text('anShTx',p='anScShLyt',l='Shot',w=80)
    pmc.optionMenu ('anShLst',p='anScShLyt',cc='chAnFlNm()')
    
    #pmc.rowLayout('anAdShRWLyt',p='anChkClmLyt',cal=[[1, 'right'], [2, 'right'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 35],[2, 84],[3, 100],[4, 100],[5, 100]],nc=5)
    #pmc.separator()
    #pmc.checkBox('addShChkBx',v=0,l='Add shots',p='anAdShRWLyt',w=80)
    #onc='pmc.optionMenu ("addAssType",e=1,en=1);pmc.textField("assNm",e=1,en=1);pmc.button("annAssBtn",e=1,en=1);pmc.optionMenu ("assTypLs",e=1,en=0)',ofc='pmc.optionMenu("addAssType",e=1,en=0);pmc.textField("assNm",e=1,en=0);pmc.button("annAssBtn",e=1,en=0);pmc.optionMenu ("assTypLs",e=1,en=1)')
    
    #pmc.optionMenu('adScLst',p='anAdShRWLyt',w=90,en=0)
    #pmc.menuItem(l="SC001")
    #pmc.menuItem(l="SC002")
    #pmc.menuItem(l="SC003")
    #pmc.textField('anNm',pht="Give a asset name here.",w=200,p='anAdShRWLyt',en=0)
    #pmc.button('annAssBtn',l="Add",c="",w=100,p='anAdShRWLyt',en=0)
    
    pmc.rowLayout('anSvFlLyt',p='anChkClmLyt',cal=[[1, 'right'], [2, 'right'], [3, 'center'], [4, 'center'], [5, 'center']],en=1,cw=[[1, 35],[2, 84],[3, 100],[4, 100],[5, 100]],nc=5)
    pmc.separator()
    pmc.text('ansvFlChkBx',l='Save File',p='anSvFlLyt',w=80)
    
    pmc.optionMenu ('addAssType',p='anSvFlLyt',w=90)
    pmc.menuItem (l="Animation",en=1)
    pmc.menuItem (l="Effect",en=1)
    pmc.menuItem (l="Lighting",en=1)
    pmc.textField('anflNm',pht="Give a File name here.",tx='XXX_SH_001_001_an_xxx_v001.mb',w=200,p='anSvFlLyt')
    pmc.button('anFlSvBtn',l="Save",c="",w=100,p='anSvFlLyt')

    #pmc.rowLayout ('addAssBtLyt',numberOfColumns=2,p='mdChkClmLyt')
    #pmc.separator (w=330,st="none",p='addAssBtLyt')

    #pmc.button('addAss',l="Add it",rs=1,w=100,c="goAddAssetFolders($tvcRoot)",p='addAssBtLyt')
    
    pmc.tabLayout('tvcChkTabLyt',e=1,tli=[[1, 'Asset'], [2, 'Shot']])
    pmc.showWindow('TVC_SubChk')

tvcChkWrkUI()
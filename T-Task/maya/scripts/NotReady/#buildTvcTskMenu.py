# -*- coding: UTF-8 -*-
import pymel.core as pmc
import maya.mel as mel
mel.eval('source "T:/tvcServe/RnD/ppl/ppl_script/tvc_addTvcTsk.mel"')
mel.eval('source "T:/tvcServe/RnD/ppl/ppl_script/tvc_attrsBatchTool.mel"')
#python "import "


def buildAddTvcTskMenu():

    if pmc.menuItem ('addTvcItm',ex=1):
        pmc.deleteUI('addTvcItm',menuItem =1)

    if pmc.menuItem ('addTvcShotMenu',ex=1):
        pmc.deleteUI ('addTvcShotMenu',menuItem =1)

    if pmc.menuItem ('addTvcAssMenu',ex=1):
        pmc.deleteUI ('addTvcAssMenu',menuItem =1)
    
    
    if (pmc.about(q=1,v=1)=="2014"):
        pmc.menuItem ('addTvcItm',d=1,p='mainCreateMenu')

    else:

        pmc.menuItem ('addTvcItm',d=1,p='mainCreateMenu',dl="Add TVC Items")
        
    pmc.menuItem ('addTvcShotMenu',l="Add TVC Shot...",p='mainCreateMenu',c="mel.eval('addTvcShotUI($tvcRoot)')") 
    pmc.menuItem ('addTvcAssMenu',l="Add TVC Asset...",p='mainCreateMenu',c="mel.eval('addTvcAssUI($tvcRoot)')")



def buildTvcAbcCacheMenu():

    if pmc.menuItem('tvcAbcTsk',ex=1):

        pmc.deleteUI ('tvcAbcTsk',menuItem=1)

    if pmc.menuItem ('tvcAbcImpMenuItm',ex=1):
        
        pmc.deleteUI ('tvcAbcImpMenuItm', menuItem=1)

    if pmc.menuItem ('tvcAbcExpMenuItm',ex=1):

        pmc.deleteUI ('tvcAbcExpMenuItm',menuItem=1)

    
    if pmc.about(q=1,v=1)=="2014":

        pmc.menuItem ('tvcAbcTsk',d=1,p='mainPipelineCacheMenu')

    else:

        pmc.menuItem ('tvcAbcTsk',d=1,p='mainPipelineCacheMenu',dl="TVC Alembic Exchange")

    
    pmc.menuItem ('tvcAbcImpMenuItm',l="TVC Abc Cache import with shader",p='mainPipelineCacheMenu',c="importBrowse()")
    pmc.menuItem ('tvcAbcExpMenuItm',l="TVC Abc Cache export with shader...",p='mainPipelineCacheMenu',c="tvc_abcExpUI()")


def buildTvcTaskMenu():

    if pmc.menu('tvcTaskMenu',ex=1):

        pmc.deleteUI ('tvcTaskMenu',menu =1)

    pmc.menu ('tvcTaskMenu',l="TVC-Task",p='MayaWindow',to=1)
    
    #Add Tasks
    if pmc.menuItem ('addTvcItmM',ex=1):

        pmc.deleteUI ('addTvcItmM',menuItem=1)

    if pmc.menuItem ('addTvcShotMenuM',ex=1):

        pmc.deleteUI ('addTvcShotMenuM',menuItem=1)

    if pmc.menuItem ('addTvcAssMenuM',ex=1):

        pmc.deleteUI ('addTvcAssMenuM',menuItem=1)
    
    
    if pmc.about(q=1,v=1)=="2014":

        pmc.menuItem ('addTvcItmM',d=1,p='tvcTaskMenu')

    else:

        pmc.menuItem ('addTvcItmM',d=1,p='tvcTaskMenu',dl="Add TVC Items") 
        
    pmc.menuItem('addTvcShotMenuM',l="Add TVC Shot...",p='tvcTaskMenu',c="mel.eval('addTvcShotUI($tvcRoot)')",ann="添加镜头文件夹结构")
    pmc.menuItem('addTvcAssMenuM',l="Add TVC Asset...",p='tvcTaskMenu',c="mel.eval('addTvcAssUI($tvcRoot)')",ann="添加资产文件夹结构")
    
    #Utilities
    if pmc.menuItem ('tvcUtils',ex=1):

        pmc.deleteUI ('tvcUtils',menuItem=1)

    
    if pmc.about(q=1,v=1)=="2014":

        pmc.menuItem ('tvcUtilsItmM',d=1,p='tvcTaskMenu') 

    else:

        pmc.menuItem ('tvcUtilsItmM',d=1,p='tvcTaskMenu',dl="TVC Utilities")
    
    if pmc.menuItem ('tvcAttrsBatchChgrMenuItmM',ex=1):

        pmc.deleteUI ('tvcAttrsBatchChgrMenuItmM',menuItem=1) 

    pmc.menuItem ('tvcAttrsBatchChgrMenuItmM',l="Attrs Batch Changer...",p='tvcTaskMenu',c="mel.eval('tvcBatchAttrts()')",ann="批量修改物体们的属性")
    
    #ABC Cache
    if pmc.menuItem ('tvcAbcTskM',ex=1):

        pmc.deleteUI ('tvcAbcTskM',menuItem=1) 

    if pmc.menuItem ('tvcAbcImpMenuItmM',ex=1):

        pmc.deleteUI ('tvcAbcImpMenuItmM',menuItem=1) 

    if pmc.menuItem ('tvcAbcExpMenuItmM',ex=1):

        pmc.deleteUI ('tvcAbcExpMenuItmM',menuItem =1)

    
    if pmc.about (q=1,v=1)=="2014":

        pmc.menuItem ('tvcAbcTskM',d=1,p='tvcTaskMenu') 

    else:

        pmc.menuItem ('tvcAbcTskM',d=1,p='tvcTaskMenu',dl="TVC Alembic Exchange") 

    pmc.menuItem ('tvcAbcImpMenuItmM',l="Import abc with shader",p='tvcTaskMenu',c="importBrowse()",ann="带材质球导入ABC缓存")
    pmc.menuItem ('tvcAbcExpMenuItmM',l="Export abc with shader...",p='tvcTaskMenu',c="tvc_abcExpUI()",ann="带材质球导出ABC缓存")

mel.eval("ModCreateMenu mainCreateMenu;")
buildAddTvcTskMenu()

mel.eval("ModCreateMenu mainPipelineCacheMenu;")
buildTvcAbcCacheMenu()

buildTvcTaskMenu()
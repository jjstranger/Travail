import pymel.core as pmc
import random

def loadLocGeoCmd():
    pmc.textScrollList('lcGeoTSL',e=1,ra=1$
    locGeos=pmc.selected()
    for item in locGeos:
        pmc.textScrollList('lcGeoTSL',e=1,a=item)
    return locGeos

def loadPrxCmd():
    pmx.textScrollList('lcPrxTSL',e=1,ra=1)
    prxGeos=pmc.selected()
    for item in prxGeos:
        pmc.textScrollList('lcPrxTSL',e=1,a=item)
    return prxGeos

def prxReplace(locGeos,prxGeos):
    if len(locGeos)==0:
        pmc.error("No location geos loaded")
    if len(prxGeos)==0:
        pmc.error("No proxies load")
    getInstHolderGeos=tuple(locGeos)
    getProxy=tuple(prxGeos)
    for item in getInstHolderGeos:
        getPos=item.getTranslation()
        getRot=item.getRotation()
        getScl=item.getScale()
        curPrc=pmc.instance(rand.choise(getProxy),leaf=1)
        pmc.xform(curPrc,r=1,t=getPos,ro=getRot,s=getScl)
        pmc.setAttr(item.visibility,0)

def prxReplaceUI():
    if pmc.window('prxRplcWin',ex=1):
        pmc.deleteUI('prxRplcWin')
    pmc.window('prxRplcWin',wh=(400,600),t='Proxies Replacement',s=0)
    pmc.columnLayout('prClmnLyt',w=390,co=('both',5),rs=10)
    pmc.separator();
    pmc.button('loadLocGeos',l='Load Location Geos',c='locGeos=loadLocGeoCmd()',h=25,w=200)
    pmc.textScrollList('lcGeosTSL',w=378,ni=10)
    pmc.button('loadPrxGeos',l='Load Proxies Geos',c='prxGeos=loadPrxCmd()',h=25,w=200)
    pmc.textScrollList('lcPrxTSL',w=378,ni=10)
    pmc.button('goReplace',l='Go Replace',c='prxReplace(locGeos,prxGeos);locGeos=prxGeos=[]',h=30,w=378)
    pmc.showWindow('prxRplcWin')

prxReplaceUI()
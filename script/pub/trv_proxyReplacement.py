//  ==============================================
//  trv_proxiesReplacement ver 1.0
//  by : JJ.Stranger
//  at : 2018.10.23
//  ==============================================
//  Description:
//      Replace locate objects with proxy objects.
//      The duplication is instancely and randomly.
//

from pymel import core as pmc
import random

def trv_prxRplc_loadLocGeoBtnCmd():
    pmc.textScrollList('lcGeoTSL',e=1,ra=1)
    locGeos=pmc.selected()
    for item in locGeos:
        pmc.textScrollList('lcGeoTSL',e=1,a=item)
    return locGeos

def trv_prxRplc_loadPrxBtnCmd():
    pmc.textScrollList('lcPrxTSL',e=1,ra=1)
    prxGeos=pmc.selected()
    for item in prxGeos:
        pmc.textScrollList('lcPrxTSL',e=1,a=item)
    return prxGeos

def trv_prxRplc_prxReplaceBtnCmd(locGeos,prxGeos):
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
        curPrc=pmc.instance(random.choice(getProxy),leaf=1)
        pmc.xform(curPrc,r=1,t=getPos,ro=getRot,s=getScl)
        pmc.setAttr(item.visibility,0)

def trv_prxReplaceUI():
    if pmc.window('prxRplcWin',ex=1):
        pmc.deleteUI('prxRplcWin')
    pmc.window('prxRplcWin',wh=(400,550),t='Proxies Replacement',s=0)
    pmc.columnLayout('prClmnLyt',w=390,co=('both',5),rs=5)
    pmc.separator(p='prClmnLyt')
    pmc.rowLayout('locBtnRwLyt',nc=2,p='prClmnLyt')
    pmc.separator(st='none',w=200,p='locBtnRwLyt')
    pmc.button('loadLocGeos',l='Load Location Geos',c='locGeos=trv_prxRplc_loadLocGeoBtnCmd()',p='locBtnRwLyt',h=25,w=180)
    pmc.textScrollList('lcGeoTSL',w=388,ni=10,p='prClmnLyt')
    pmc.separator(st='in',w=390,h=10,p='prClmnLyt')
    pmc.rowLayout('prxBtnRwLyt',nc=2,p='prClmnLyt')
    pmc.separator(st='none',w=200,p='prxBtnRwLyt')
    pmc.button('loadPrxGeos',l='Load Proxies Geos',c='prxGeos=trv_prxRplc_loadPrxBtnCmd()',p='prxBtnRwLyt',h=25,w=180)
    pmc.textScrollList('lcPrxTSL',w=388,ni=10,p='prClmnLyt')
    pmc.separator(st='in',w=390,h=10,p='prClmnLyt')
    pmc.button('goReplace',l='Go Replace',c='trv_prxRplc_prxReplaceBtnCmd(locGeos,prxGeos);locGeos=prxGeos=[]',h=30,w=390,p='prClmnLyt')
    pmc.showWindow('prxRplcWin')

trv_prxReplaceUI()
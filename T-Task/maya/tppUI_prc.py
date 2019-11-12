from pymel import core as pmc
import os

def tvcPrjPortalWinUI():
    if pmc.window("prjPortalWinUI",q=1,ex=1)==1:
        pmc.deleteUI("prjPortalWinUI",wnd=1)
    pmc.window("prjPortalWinUI",wh=(800,640),t="TVC Projects Portal", rtf=1)
    
    pmc.columnLayout("tpp_clmnLyt",w=750,h=600,adj=1)
    pmc.textFieldButtonGrp("lookInto_txFldBtnGrp",l="Look Into: ",bl="Browse..",w=750,cw3=(60,650,50))
    
    pmc.rowLayout("lstPnl_rwLyt",ct2=("both","both"),cw2=(200,500),nc=2)
    pmc.columnLayout("prjFavLst_clmnLyt",p="lstPnl_rwLyt",co=("both",5))
    pmc.separaror(st="in",h=10,w=200)
    pmc.textFieldButtonGrp("prjTitSrch_txFldBtnGrp",l="Projects:",bl="Search",p="prjFavLst_clmnLyt",cw3=(45,99,50),cl3=("left","both","right"))
    pmc.textScrollList(h=420,p="prjFavLst_clmnLyt",w=195)
    pmc.text(l="Collections:",p="prjFavLst_clmnLyt",h=20)
    pmc.textScrollList(h=120,p="prjFavLst_clmnLyt",w=195)
    
    pmc.columnLayout("rBrswClmnLyt",p="lstPnl_rwLyt",co=("left",5),h=600)
    pmc.rowLayout("pathDscrpLn",p=rBswrClmnLyt",nc=5)
    pmc.text("dbRghtIcn",l=">>",w=20,p="pathDscrpLn")
pmc.rowLayout("pathTrainCtrlRwLyt",p="pathDscrpLn",nc=20)

    for pathSect in ["3507_HJ_YLQQ","VFX","sequence","SC001","YLQQ_001_004","CG","scenes","effects"]:
        pmc.button(l=pathSect,p="pathTrainCtrlRwLyt")
        pmc.popuoMenu()
        pmc.menuItem()

tvcPrjPortalWinUI()    
pmc.showWindow("prjPortalWinUI")


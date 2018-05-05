import pymel.core as pmc

def mdHistoryChk():
    dirtObjLst=[]
    objLst=pmc.ls(g=1,s=1)
    for item in objLst:
        histryLst=len(pmc.listHistory(item))
        if histryLst >1:
            dirtObjLst.append(item)
            
    print dirtObjLst
    pmc.select(dirtObjLst)
    pmc.pickWalk(d="up")

#mdHistoryChk()
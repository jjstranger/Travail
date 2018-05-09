
    
def svAssFile():
    getPrjNm=pmc.optionMenu(‘prjLst’,q=1,v=1)
    assLst=


#
def chAssFlNm():
    getAssNm=pmc.optionMenu(“assTypLs”,q=1,v=1)
    getAssTyp=pmc.optionMenu(”addAssType”,q=1,ill=1)
    if getAssTyp==“Mesh”:
        pmc.textField(“asFlNm”,e=1,tx=getAss+”_md_”+usr,en=1)
    if getAssTyp==“Rig”:
        pmc.textField(“asFlNm”,e=1,tx=getAss+”_rg_”+usr,en=1)
    if getAssTyp==“Lighting”:
        pmc.textField(“asFlNm”,e=1,tx=getAss+”_lt_”+usr,en=1)

def chAnFlNm():
    getShName=pmc.optionMenu(‘anShLst’,q=1,v=1)
    getTskLs=pmc.optionMenu(‘addAssType’,q=1,ill=1)
    getTskSlId=pmc.optionMenu(‘addAssTyp’,q=1,sl=1)
    getTskTypId=pmc.optionMenu(getTskLs[getTskSlId-1],q=1,da=1)

    if getTskTypId==0:
        getTskTyp=‘an’
    if getTskTypId==1:
        getTskTyp=‘fx’
    if getTskTypId==2:
        getTskTyp=‘lt’
    pmc.textField(‘anflNm’,e=1,tx=getShName+’_’+getTskTyp+’_’+usr,en=1)

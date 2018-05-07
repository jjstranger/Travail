#def anUnusdSl():
#####ios
def txImgChk():
    txImgLst=pmc.ls(typ=‘file’)
    dirtTxImgLst=[]
    print ‘========== Texture Images Check ==========\n’
    for item in txImgLst:
        if os.path.exists(pmc.getAttr(item+‘.fileTextureName’))==0:
        print pmc.getAttr(item+‘.fileTextureName’)+‘ is missing.’
        dirtTxImgLst.append(item)
    if len(dirtTxImgLst)>0:
        pmc.textField(‘txChkTxF’,e=1,tx=str(len(dirtTxImgLst))+‘ missing textures.’,bgc=(1,0,0))
        pmc.textField(‘anTxChkTxF’,e=1,tx=str(len(dirtTxImgLst))+‘ missing textures.’,bgc=(1,0,0))
    else:
        pmc.textField(‘txChkTxF’,e=1,tx=‘Good’,bgc=(0,1,0))
        pmc.textField(‘anTxChkTxF’,e=1,tx=‘Good’,bgc=(0,1,0))
        return dirtTxImgLst
        
def txDCC():
    getTxNodNm=pmc.textScrollList(‘txLst’,q=1,sl=1)[0].split(“    ”)
    pmc.select(getTxNodNm[1])
    pmc.runtime.AttributeEditor()

def txImgDtBtn(lanSW):
    pmc.runtime.FilePathEditor()
    
def txImgSlBtn():
    getDiirtTxImgLst=txImgChk()
    pmc.select(getDiirtTxImgLst)
    
def txPathResetBtn():
    getTxSlLs=pmc.textScrollList(“txLst”,q=1,si=1)
for item in getTxSlLs:
    nodeNm=item.split(“    ”)[1]
    txPath=item.split(“    ”)[2]
    
    
#####ios

#def getShtLst():
    
def svAssFile():
    getPrjNm=pmc.optionMenu(‘prjLst’,q=1,v=1)
assLst=
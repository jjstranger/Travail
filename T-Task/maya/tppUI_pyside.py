from PySide2 import QtWidgets as pqw

#pthTrainSect=["3000_PN_Project","VFX","sequence","SC001","Shot_001","CG","scenes","Effects"] 
pthTrainSect=[]
##### Buid Win UI Below #####

win=pqw.QWidget()
win.setWindowTitle("TPP Win")

mainVBLyt=pqw.QVBoxLayout()

rootFndLnHBLyt=pqw.QHBoxLayout()
lb_lkIn=pqw.QLabel("Look In: ")
ln_lKIn=pqw.QLineEdit()
pb_lkIn=pqw.QPushButton("Browse..")

win.setLayout(mainVBLyt)
mainVBLyt.addLayout(rootFndLnHBLyt)
rootFndLnHBLyt.addWidget(lb_lkIn)
rootFndLnHBLyt.addWidget(ln_lKIn)
rootFndLnHBLyt.addWidget(pb_lkIn)

lsBxAreaHBLyt=pqw.QHBoxLayout()

mainVBLyt.addLayout(lsBxAreaHBLyt)
outlineVHBLyt=pqw.QVBoxLayout()
lsBxAreaHBLyt.addLayout(outlineVHBLyt)
#outlineVHBLyt.addStretch(0)


prjLsHeadHBLyt=pqw.QHBoxLayout()
outlineVHBLyt.addLayout(prjLsHeadHBLyt)

lb_prj=pqw.QLabel("Projects: ")
ln_prjSrchLn=pqw.QLineEdit()
pb_prjSrchPb=pqw.QPushButton("Search")
lw_prjLst=pqw.QListWidget()
lb_fav=pqw.QLabel("Project Content: ")
lw_favLst=pqw.QListWidget()

prjLsHeadHBLyt.addWidget(lb_prj)
prjLsHeadHBLyt.addWidget(ln_prjSrchLn)
prjLsHeadHBLyt.addWidget(pb_prjSrchPb)
outlineVHBLyt.addWidget(lw_prjLst)
outlineVHBLyt.addWidget(lb_fav)
outlineVHBLyt.addWidget(lw_favLst)

subPthBrswrVBLyt=pqw.QVBoxLayout()
pthTrainHBLyt=pqw.QHBoxLayout()
pthTrainHBLyt.setSpacing(1)
lb_pthTrainLbTx=pqw.QLabel(">>")
pthTrainHBLyt.addWidget(lb_pthTrainLbTx)
trainSectionsHBLyt=pqw.QHBoxLayout()
pthTrainHBLyt.addLayout(trainSectionsHBLyt)
for pthSec in pthTrainSect:
    pthSecPb=pqw.QPushButton(pthSec)
    #pthSecPb.setFixedHeight(22)
    trainSectionsHBLyt.addWidget(pthSecPb)
#pthTrainHBLyt.addSpacerItem(pqw.QSpacerItem(1,1))
flSrchHBLyt=pqw.QHBoxLayout()
ln_flSrchLn=pqw.QLineEdit()
pb_flSrchPb=pqw.QPushButton("Search")
trainSectionsHBLyt.addStretch()

pthTrainHBLyt.addLayout(flSrchHBLyt)
flSrchHBLyt.addWidget(ln_flSrchLn)
ln_flSrchLn.setMaximumWidth(100)
flSrchHBLyt.addWidget(pb_flSrchPb)
pb_flSrchPb.setMaximumWidth(80)

flCtntLW=pqw.QListWidget()
lsBxAreaHBLyt.addLayout(subPthBrswrVBLyt)
subPthBrswrVBLyt.addLayout(pthTrainHBLyt)
subPthBrswrVBLyt.addWidget(flCtntLW)
lsBxAreaHBLyt.setStretchFactor(outlineVHBLyt,1)
lsBxAreaHBLyt.setStretchFactor(subPthBrswrVBLyt,3)

flNmLnHBLyt=pqw.QHBoxLayout()
lb_flNm=pqw.QLabel("File:")
le_flNmLE=pqw.QLineEdit()
cb_flTyp=pqw.QComboBox()
subPthBrswrVBLyt.addLayout(flNmLnHBLyt)
flNmLnHBLyt.addWidget(lb_flNm)
flNmLnHBLyt.addWidget(le_flNmLE)
flNmLnHBLyt.addWidget(cb_flTyp)

cmdPBHBLyt=pqw.QHBoxLayout()
pb_new=pqw.QPushButton("New")
pb_load=pqw.QPushButton("Load")
pb_nest=pqw.QPushButton("Nest")
pb_nth=pqw.QPushButton("NO IDEA")

subPthBrswrVBLyt.addLayout(cmdPBHBLyt)
cmdPBHBLyt.addWidget(pb_new)
cmdPBHBLyt.addWidget(pb_load)
cmdPBHBLyt.addWidget(pb_nest)
cmdPBHBLyt.addWidget(pb_nth)

##### Build Win UI End #####

##### Setting Win UI Below #####
import os
tvcRoot="C:/PRJ/dev/"
lsDir=os.listdir(tvcRoot)
testPrjDir="C:/PRJ/dev/3001_JJS_PrjTst/"

prjLs=[]
nprjLs=[]

# filter out Prjlist and nonPrjList in prj Root
for item in lsDir:
    if (item[0:3].isdigit()) & (item.count("_")>=2) & os.path.isdir(tvcRoot+item):#filter RUles
        prjLs.append(item)
    else:
        nprjLs.append(item)

lw_prjLst.addItems(sorted(prjLs))
#lw_favLst.addItems([">>To Asset",">>To Sequence"])

def prjItmSl():
    lw_favLst.clear()
    if (os.path.exists(tvcRoot+lw_prjLst.selectedItems()[0].text()+"/VFX/assets/")):
        lw_favLst.addItem(">>To Asset")
    if (os.path.exists(tvcRoot+lw_prjLst.selectedItems()[0].text()+"/VFX/sequences/")):
        lw_favLst.addItem(">>To Sequence")
    if (os.path.exists(tvcRoot+lw_prjLst.selectedItems()[0].text()+"/VFX/")):
        lw_favLst.addItems(os.listdir(tvcRoot+lw_prjLst.selectedItems()[0].text()+"/VFX/"))

lw_prjLst.itemClicked.connect(prjItmSl)

def lsPrjOtln():
    lw_favLst.clear()
    curPrjCtntPath=tvcRoot+lw_prjLst.selectedItems()[0].text()
    curPrjCtnt=os.listdir(curPrjCtntPath)
    for item in curPrjCtnt:
        if os.path.isfile(curPrjCtntPath+"/"+item):
            curPrjCtnt.remove(item)
    if os.path.exists(curPrjCtntPath+"/VFX/assets/"):
        itm_toAss=lw_favlst.addItem(">>To Asset")
    if os.path.exists(curPrjCtntPath+"/VFX/sequences/"):
        itm_toAss=lw_favLst.addItem(">>To Sequence")
    lw_favLst.addItems(sort(curPrjCtnt))
    return curPrjCtntPath
    
def toShotcut():
    curPrjCtntPath=lsPrjOtln()
    if os.path.exists(curPrjCtntPath+"/VFX/asset/CGassets/"):
        lsToAssCtnt=os.listdir(curPrjCtntPath+"/VFX/assets/CGassets/")
        itm_shotcut_path=curPrjCtntPath+"/VFX/assets/CGassets/"
    else:
        scnLs=os.listdir(curPrjCtntPath+"/VFX/sequences/")
        for item in scnLs:
            if os.path.isfile(curPrjCtntPath+"/VFX/sequences/"+item):
                scnLs.remove(item)
        if len(lsToSeqCtnt)==1:
            scnPth=curPrjCtntPath+"/VFX/sequences/"+lsToSeqCtnt[0]
            shtLs=os.listdir(scnPth)
            for item in shtLs:
                if ((os.path.isfile(scnPth+"/"+item)) | (item.startswith("XXX_"))):
                    shtLs.remove(item)
                if len(shtLs)==1:
                    lsScence=os.listdir(scnPth+"/"+shtLs[0]+"/CG/scenes/")
                    itm_shotcut_path=scnPth+"/"+shtLs[0]+"/CG/scenes/"
                else:
                    itm_shotcut_path=scnPth
        else:
            itm_shotcut_path=curPrjCtntPath+"/VFX/sequences/"
        return itm_shotcut_path

def clickPrjOtlItm():
    toShotcut()
    flCtntLW.clear()
    getFavSlItm=lw_favLst.selectedItems()[0].text()
    if getFavSlItm.startswith(">>"):
        lsFlBrws=os.listdir(itm_shotcut_path)
        print lsFlBrws
        flCtntLW.addItems(lsFlBrws)
    else:
        pass#lsFlBrws=os.listdir(

lw_prjLst.itemClicked.connect(lsPrjOtln)
lw_favLst.itemClicked.connect(clickPrjOtlItm)
#Important: search filter and path train


win.close()
win.show()
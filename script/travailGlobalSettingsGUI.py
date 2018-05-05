import pymel.core as pmc
if pmc.window("travailGlobalSettingsWin",ex=1):
	pmc.deleteUI("travailGlobalSettingsWin")
pmc.window("travailGlobalSettingsWin",t="Travail Settings Window",w=500,h=600,s=0)
pmc.columnLayout("trvGlbStsClmnLyt",co=("both",5))
pmc.separator(h=10)
pmc.textFieldGrp("usrTx",l="Current User Name: ",tx=usr,ed=1)
pmc.textFieldGrp("usrShtTx",l="User Short Name: ",tx=usrShort)
pmc.optionMenuGrp("jobs",l="User Job: ")
pmc.menuItem("md",l="modeling")
pmc.menuItem("sd",l="shader")
pmc.menuItem("rg",l="rigging")
pmc.menuItem("an",l="animation")
pmc.menuItem("fx",l="effects")
pmc.menuItem("lt",l="lighting")
pmc.menuItem("rn",l="rendering")
pmc.textFieldButtonGrp("prjRootPath",l="Projects Root: ",fi=prjRoot)
pmc.textFieldButtonGrp("travailRootPath",l="Travail Root: ",fi=travailRoot)
pmc.rowLayout("svBtnRowLyt",nc=2,nch=2,h=50)
pmc.separator(st="none",w=280,p="svBtnRowLyt")
pmc.button("svPrefsBtn",l="Save Prefs",w=100,c="",p="svBtnRowLyt")
pmc.separator(h=50,p="trvGlbStsClmnLyt")

bottomLabTx="TRAVAIL"
bottomLabTxNew="-	"
t=0
for L in bottomLabTx:
	if t<(len(bottomLabTx)-1):
		bottomLabTxNew+=(L+"	.	")
		t+=1
	else:
		bottomLabTxNew+=(L+"	-")
pmc.text("blt",p="trvGlbStsClmnLyt",l=bottomLabTxNew,w=400,h=80)
pmc.showWindow("travailGlobalSettingsWin")
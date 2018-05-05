import pymel.core as pmc
import os
import travailGlobalSettings 
print usr
travailSettingsFile=(pmc.internalVar(upd=1)+"/travailGlobalSettings.conf")
	
def openPathBrowser(filePath):

	assignLocation=pmc.fileDialog2(fm=3,caption="Choose A Folder",dir=filePath)[0]
	#assignLocation = assignLocation and assignLocation[0].replace('\\', '/')
	if str(assignLocation).endswith("/")==0:
		assignLocation+="/"
	return assignLocation
	
def getBrwsPath(type,name):
	filePath=eval("pmc."+type+"('"+name+"',q=1,fi=1)")
	if os.path.exists(filePath)==0:
		filePath=pmc.internalVar(userWorkspaceDir=1)
	
	newLoc=openPathBrowser(filePath)
	print newLoc
	eval("pmc."+type+"('"+name+"',e=1,fi=newLoc)")
	
def svPrefs():
	usrNm=pmc.textFieldGrp("usrTx",q=1,tx=1)
	usrShNm=pmc.textFieldGrp("usrShtTx",q=1,tx=1)
	usrJob=pmc.optionMenuGrp("jobs",q=1,v=1)
	prjRoot=pmc.textFieldButtonGrp("prjRootPath",q=1,fi=1)
	tvlRoot=pmc.textFieldButtonGrp("travailRootPath",q=1,fi=1)
	lang=str(int(pmc.optionMenuGrp("lan",q=1,sl=1))-1)
	prefFileContent="import getpass\nusr='"+usrNm+"'\nusrShort='"+usrShNm+"'\nusrJob='"+usrJob+"'\nprjRoot='"+prjRoot+"'\ntravailRoot='"+tvlRoot+"'\nlang="+lang+"\nloadSettingsState=1"
	confFileOpen=open(travailSettingsFile,"w")
	confFileOpen.write(prefFileContent)
	confFileOpen.close()
	
def travailGlobalSettingsWinUI():
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
	pmc.textFieldButtonGrp("prjRootPath",l="Projects Root: ",fi=prjRoot,bl="Browse..",bc="getBrwsPath('textFieldButtonGrp','prjRootPath')")
	pmc.textFieldButtonGrp("travailRootPath",l="Travail Root: ",fi=travailRoot,bl="Browse..",bc="getBrwsPath('textFieldButtonGrp','travailRootPath')")
	pmc.optionMenuGrp("lan",l="Language: ")
	pmc.menuItem("en",l="English",da=0)
	pmc.menuItem("cn",l="Chinese",da=1)
	
	pmc.rowLayout("svBtnRowLyt",nc=2,nch=2,h=50)
	pmc.separator(st="none",w=280,p="svBtnRowLyt")
	pmc.button("svPrefsBtn",l="Save Prefs",w=100,c="svPrefs()",p="svBtnRowLyt")
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
	
#travailGlobalSettingsWinUI()
if os.path.exists(travailSettingsFile)==0:
	travailGlobalSettingsWinUI()
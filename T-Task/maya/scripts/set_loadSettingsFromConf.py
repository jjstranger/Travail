import os
from pymel import core as pmc

travailSettingsFile=(pmc.internalVar(upd=1)+"travailGlobalSettings.conf")

if (os.path.exists(travailSettingsFile)=0):
	import getpass
	projectsRoot=""
	#travailRoot=""
	trvailLocal=""
	djvRoot=travailRoot+"extention/djv/bin/"
	hbRoot=travailRoot+"extention/handbrake/"
	usr=getpass.getuser()
	usrShort=""
	usrJob=4
	lang=0
	localize=0
    import set_travailGlobalSettingGUI
	travailGlobalSettingsWinUI()
else:
	f=open(travailSettingsFile,"r")
	prefLs=f.readline()
	for item in prefLs:
		exec(item)
    print "Load pref settings for Travail Python."

import os
from pymel import core as pmc

def trv_synScrpt2Loc():
	lsTrvScrptDir=os.listdir(travailRoot+'/Script/')
	lsAllSrcScrpt=[item for item in lsTrvScrptDir if item.endswith(('.mel','.py'))]

	usrScrptDir=pmc.internalVar(usd=1)
	lsDstScrptDir=os.listdir(usrScrptDir)
	lsAllDstScrpt=[item for item in lsDstScrptDir if item.endswith(('.mel','.py'))]

	scrptToCopy=[]
	pycDel=[]
	for item in lsAllSrcScrpt:
		if item in lsAllDstScrpt:
			srcFileTCod=os.stat(travailRoot+'/Script/'+item).st_mtime
			dstFileTCod=os.stat(usrScrptDir+item).st_mtime
			if srcFileTCod!=dstFileTCod:
				if os.path.exists(usrScrptDir+item+'c'):
					pycDel.append(travailRoot+'/Script/'+item+'c')
					print '[Delete] '+usrScrptDir+item+'c'
				print '[Update] '+item
				scrptToCopy.append(travailRoot+'/Script/'+item)
		else:
			print '[New] '+item
			scrptToCopy.append(travailRoot+'/Script/'+item)
	return scrptToCopy,pycDel
trv_synScrpt2Loc()

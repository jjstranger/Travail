import trv_sceneComprehension

def trv_setPrjFrmCurScn()
	getGuessSetPrjDir=trv_guessPrjFrmCurScn()
	if len(getGuessSetPrjDir)!=1:
		pmc.workspace(getGuessSetPrjDir,o=1)
		print ("Get workspace file from : "+getGuessSetPrjDir)
	else:
		print ('No worksapce file from current scene.')
		cd=pmc.confirmDialog(t='No workspace file found.',m='No workspace file found, set project manually?',b=['OK','Cancel'],db='OK',cb='Cancel',ds='Cancel')
		if cd== 'OK':
			pmc.runtime.SetProject()
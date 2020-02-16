import os,time
from set_loadSettingsFromConf import * ## may change Name to Fit later
#from pymel import core as pmc
from maya import cmds as mc
projectRoot="C:/PRJ/dev/" ## test, remove later
job="Fx" ## test, remove later

def scenePathStateCode():
    global curSceneName,scenePathDestruc
    curSceneName=mc.file(q=1,sn=1)
    if len(curSceneName)==0:
	    return 1 # Mark as Unamed Scene.
    else:
        getPrjRoot=projectRoot
        scenePathDestruc=curSceneName.split('/')
        if len(getPrjRoot)==0:
            mc.warning('travailRoot is not set.')
        elif curSceneName.startswith(getPrjRoot):
            return 0 # Correct.
        else:
            return 2

def trv_guessFrmCurScn(): # Only available for VHQ TVC File structure
	getPrjRoot=projectRoot
	if getPrjRoot.endswith('/')==0:
		getPrjRoot+='/'
	scenePathDestruc=curSceneName[(len(projectRoot)):].split('/')
	if scenePathDestruc[2]=='sequences':
		curScInfs=[scenePathDestruc[0],scenePathDestruc[2],scenePathDestruc[3],scenePathDestruc[4]]
	elif scenePathDestruc[2]=='assets':
		curScInfs=[scenePathDestruc[0],scenePathDestruc[2],'','']
	return curScInfs

def trv_guessPrjFrmCurScn():
	searchLoop=5
	setPrjPath='1' # "1" = workspace file not found.
	if trv_guessFrmCurScn()[1]=='sequences':
		parPath=os.path.abspath(os.path.dirname(curSceneName))
		for i in range(searchLoop):
			parPath=os.path.abspath(os.path.dirname(parPath))
			wsFilePth=os.path.abspath(parPath+'/workspace.mel')
			if os.path.exists(wsFilePth):
				if '\\' in parPath:
					setPrjPath=parPath.replace('\\','/')
				break
	return setPrjPath

def trv_guessJobFrmCurScn():
	guessJob=''
	if 'Effect*' in scenePathDestruc:
		guessJob='Effect'
	elif 'Animation' in scenePathDestruc:
		guessJob='Animation'
	elif 'Lighting' in scenePathDestruc:
		guessJob='Lighting'
	if len(job)>1 and len(guessJob)==0:
		guessJob=job
	return guessJob

def trv_guessDailyFldFrmCurScn():
	fxFldLs=['Effects','Effect','effects','effect','fx','FX','efx','Efx','EFX']
	anFldLs=['Animation','Animations','animations','animation','an','An','AN','ani','Ani','anim','Anim']
	lfFldLs=['Lighting','lighting','light','Light','lgt','LGT','Lgt','lt','Lt','LT']
	nullFldLs=['']
	getGuessJob=trv_guessJobFrmCurScn()
	if curSceneName.startswith(projectRoot):
		if len(getGuessJob)>1:
			if getGuessJob=='Effect':
				mdLs=fxFldLs
			elif getGuessJob=='Animation':
				mdLs=anFldLs
			elif getGuessJob=='Lighting':
				mdLs=ltFldLs
			else:
				mdLs=nullFldLs
		else:
			mdLs=nullFldLs
		getCurDailyFolder=scenePathDestruc[0]+'/'+scenePathDestruc[1]+'/'+scenePathDestruc[2]+'/VFX_Dailies/'+time.strftime('%Y%m%d',time.localtime())
		if os.path.exists(getCurDailyFolder):
			for md in mdLs:
				if md in os.listdir(getCurDailyFolder):
					moduleNm=md
				else:
					moduleNm=mdLs[0]
			else:
				moduleNm=mdLs[0]
			getCurDailyFolder=getCurDailyFolder+'/'+moduleNm
			if getCurDailyFolder.endswith('/'):
				getCurDailyFolder=getCurDailyFolder[0:-1]
		else:
			getCurDailyFolder=''
		return getCurDailyFolder

def trv_guessRndPathFrmCurScn():
	aos=trv_guessFrmCurScn()[1]
	getGuessJob=trv_guessJobFrmCurScn()
	if aos =='sequences':
		if getGuessJob=='Effect':
			jobFld='Effects'
		elif getGuessJob=='Lighting':
			jobFld='Lighting'
		else:
			jobFld=''
		renderPath=projectRoot+trv_guessFrmCurScn()[0]+'/VFX/sequences'+trv_guessFrmCurScn()[2]+'/'+trv_guessFrmCurScn()[3]+'/Zup_renders/'+jobFld
		return renderPath

def trv_sceneComprehension():
	if scenePathStateCode()==0:
		global curPrjName,curAoS,curJob,curScene,curShot,curDailyFolder,curSetPrjDir,curRndPath
		curPrjName=trv_guessFrmCurScn()[0]
		curAoS=trv_guessFrmCurScn()[1]
		curJob=trv_guessJobFrmCurScn()
		if curAoS=='sequences':
			curScene=trv_guessFrmCurScn()[2]
			curShot=trv_guessFrmCurScn()[3]
			curDailyFolder=trv_guessDailyFldFrmCurScn()
			curSetPrjDir=trv_guessPrjFrmCurScn()
			curRndPath=trv_guessRndPathFrmCurScn()
		else:
			curScene=''
			curShot=''
			curDailyFolder=''
			curSetPrjDir=''
			curRndPath=''
		return [curPrjName,curAoS,curJob,curScene,curShot,curDailyFolder,curSetPrjDir,curRndPath]
	elif scenePathStateCode()==1:
		mc.error('Unamed Scene!')
	elif scenePathStateCode()==2:
		mc.warning('Secen File is Not in Project Root')
		curSetPrjDir=trv_guessPrjFrmCurScn()

def printInfos():
	trv_sceneComprehension()
	if scenePathStateCode()==0:
		print '========== Scene Comprehension ==========\n'
		print 'Project Name: \n\t'+curPrjName
		print '\nAsset or Sequence: \n\t'+curAoS
		print '\nCurrent Task Job: \n\t'+curJob
		if curAoS=='sequences':
			print '\nScene: \n\t'+curScene
			print '\nShot: \n\t'+curShot
			print '\nSet Project Dir: \n\t'+curSetPrjDir
			print '\nDaily Folder: \n\t'+curDailyFolder
			if os.path.exists(curDailyFolder)==0:
				print '\t[Non-Exists]'
			print  '\nRender Path: \n\t'+curRndPath
		print '\n======= Scene Comprehension Finish ======='
printInfos()
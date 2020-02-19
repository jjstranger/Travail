import os,time
from set_loadSettingsFromConf import * ## may change Name to Fit later
#from pymel import core as pmc
from maya import cmds as mc
#projectRoot="C:/PRJ/dev/" ## test remove later
#job="Fx" ## test remove later

class scenePathDecompose(object):
    def __init__(self):
        self.prjName=curPrjName
        self.workFlow=curAoS
        self.task=curJob
        self.prjDir=curSetPrjDir
        self.dailyDir=curDailyFolder
        self.renderDir=curRndPath
        if self.workFlow=="sequences":
            self.assName=None
            self.scn=curScene
            self.sht=curShot
        else:
            self.assName="Coming Later"
            self.scn=self.sht
        self.allInf=self.printInfos()
            

    def scenePathStateCode(self):
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
    
    def trv_guessFrmCurScn(self): # Only available for VHQ TVC File structure
    	getPrjRoot=projectRoot
    	if getPrjRoot.endswith('/')==0:
    		getPrjRoot+='/'
    	scenePathDestruc=curSceneName[(len(projectRoot)):].split('/')
    	if scenePathDestruc[2]=='sequences':
    		curScInfs=[scenePathDestruc[0],scenePathDestruc[2],scenePathDestruc[3],scenePathDestruc[4]]
    	elif scenePathDestruc[2]=='assets':
    		curScInfs=[scenePathDestruc[0],scenePathDestruc[2],'','']
    	return curScInfs
    
    def trv_guessPrjFrmCurScn(self):
    	searchLoop=5
    	setPrjPath='1' # "1" = workspace file not found.
    	if self.trv_guessFrmCurScn()[1]=='sequences':
    		parPath=os.path.abspath(os.path.dirname(curSceneName))
    		for i in range(searchLoop):
    			parPath=os.path.abspath(os.path.dirname(parPath))
    			wsFilePth=os.path.abspath(parPath+'/workspace.mel')
    			if os.path.exists(wsFilePth):
    				if '\\' in parPath:
    					setPrjPath=parPath.replace('\\','/')
    				break
    	return setPrjPath
    
    def trv_guessJobFrmCurScn(self):
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
    
    def trv_guessDailyFldFrmCurScn(self):
    	fxFldLs=['Effects','Effect','effects','effect','fx','FX','efx','Efx','EFX']
    	anFldLs=['Animation','Animations','animations','animation','an','An','AN','ani','Ani','anim','Anim']
    	lfFldLs=['Lighting','lighting','light','Light','lgt','LGT','Lgt','lt','Lt','LT']
    	nullFldLs=['']
    	getGuessJob=self.trv_guessJobFrmCurScn()
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
    
    def trv_guessRndPathFrmCurScn(self):
    	aos=self.trv_guessFrmCurScn()[1]
    	getGuessJob=self.trv_guessJobFrmCurScn()
    	if aos =='sequences':
    		if getGuessJob=='Effect':
    			jobFld='Effects'
    		elif getGuessJob=='Lighting':
    			jobFld='Lighting'
    		else:
    			jobFld=''
    		renderPath=projectRoot+self.trv_guessFrmCurScn()[0]+'/VFX/sequences'+self.trv_guessFrmCurScn()[2]+'/'+self.trv_guessFrmCurScn()[3]+'/Zup_renders/'+jobFld
    		return renderPath
    
    def trv_sceneComprehension(self):
    	if self.scenePathStateCode()==0:
    		global curPrjName,curAoS,curJob,curScene,curShot,curDailyFolder,curSetPrjDir,curRndPath
    		curPrjName=self.trv_guessFrmCurScn()[0]
    		curAoS=self.trv_guessFrmCurScn()[1]
    		curJob=self.trv_guessJobFrmCurScn()
    		if curAoS=='sequences':
    			curScene=self.trv_guessFrmCurScn()[2]
    			curShot=self.trv_guessFrmCurScn()[3]
    			curDailyFolder=self.trv_guessDailyFldFrmCurScn()
    			curSetPrjDir=self.trv_guessPrjFrmCurScn()
    			curRndPath=self.trv_guessRndPathFrmCurScn()
    		else:
    			curScene=''
    			curShot=''
    			curDailyFolder=''
    			curSetPrjDir=''
    			curRndPath=''
    		return [curPrjName,curAoS,curJob,curScene,curShot,curDailyFolder,curSetPrjDir,curRndPath]
    	elif self.scenePathStateCode()==1:
    		mc.error('Unamed Scene!')
    	elif self.cenePathStateCode()==2:
    		mc.warning('Secen File is Not in Project Root')
    		curSetPrjDir=self.trv_guessPrjFrmCurScn()
    
    def printInfos(self):
    	self.trv_sceneComprehension()
    	infStr=""
    	if self.scenePathStateCode()==0:
    		infStr+= '========== Scene Comprehension ==========\n'
    		infStr+=( 'Project Name: \n\t'+curPrjName)
    		infStr+=( '\nAsset or Sequence: \n\t'+curAoS)
    		infStr+=( '\nCurrent Task Job: \n\t'+curJob)
    		if curAoS=='sequences':
    			infStr+=( '\nScene: \n\t'+curScene)
    			infStr+=( '\nShot: \n\t'+curShot)
    			infStr+=( '\nSet Project Dir: \n\t'+curSetPrjDir)
    			infStr+=( '\nDaily Folder: \n\t'+curDailyFolder)
    			if len(curDailyFolder)!=0 & os.path.exists(curDailyFolder)==0:
    				infStr+=( '\t[Non-Exists]')
    			infStr+=(  '\nRender Path: \n\t'+curRndPath)
    		infStr+=( '\n======= Scene Comprehension Finish =======')
    		return infStr
#print scenePathDecompose().allInf ## test, remove later
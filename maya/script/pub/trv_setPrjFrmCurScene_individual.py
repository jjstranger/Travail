import os
import pymel.core as pmc

def trv_setPrjFrmCurScene():
    searchloop=5
    if len(pmc.sceneName())==0:
        pmc.error('Unamed Scene!')
    parPath=os.path.abspath(os.path.dirname(pmc.sceneName()))
    for i in range(searchloop):
        parPath=os.path.abspath(os.path.dirname(parPath))
        wsLoc=os.path.abspath(parPath+'/workspace.mel')
        if os.path.exists(wsLoc):
            pmc.workspace(parPath,o=1)
            print ('Get workspace file from : '+wsLoc)
            stcod=0
            break
        else:
            stcod=1
    if stcod==1:
        print('No workspace file found in '+str(searchLoop)+' levels up from current scene.')
        cd=pmc.confirmDialog(t='No workspace file found',m='No workspace file found, set manually?',b=['OK','Cancel'],db='OK',cb='Cancel',ds='Cancel')
        if cd=='OK':
            pmc.runtime.SetProject()
trv_setPrjFrmCurScene()
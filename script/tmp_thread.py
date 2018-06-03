import time,threading
import pymel.core as pmc
import maya.utils as mu

def statusFieldBtn(col):
    if col==0:
        bTxL=‘GOOD’
        bBCol=(.25,.25,.25)
    else:
        bTxL=‘BAD’
        bBCol=(.95,.25,.25)
    
    getStatusLinePar=pmc.iconTextButton(‘statusFieldButton’,q=1,p=1)
    if pmc.button(‘notiBtn’,ex=1):
        pmc.deleteUI(‘notiBtn’)
    pmc.button(‘notiBtn’,l=bTxL,bgc=bBCol,w=100,p=getStatusLinePar)

def daemonThread():
    for i in range(10):
        if i%2==0:
            col=0
        else:
            col=1
        mu.executeInMainThreadWithResult(statusFieldBtn,col)
        time.sleep(1)
daemonInstance=threading.Thread(target=daemonThread).start()

#######
def srcFilesLstUI():
    if pmc.window(‘srcFilesLsWin’, ex=1):
        pmc.deleteUI(‘srcFilesLsWin’)
    pmc.window(‘srcFilesLsWin’,wh=(610,300),t=‘Syn Files List’)
    pmc.columnLayout(‘sFLClLyt’,w=600,co=(‘both’,5))
    pmc.text(‘sFLTx’,l=‘Syn Files List:’,h=20)
    pmc.textScrollList(‘srcFileLsTSL’,w=600,ni=10)

srcFilesLstUI()
showWindow(‘srcFilesWin’)
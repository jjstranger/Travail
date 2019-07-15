import os, travailGlobalSettings
from pymel import core as pmc

def trv_synScriptsToLocal():
    lsTrvScriptsDir=os.listdir(travailRoot+"maya/scripts/")
    lsAllSrcScripts=[item for item in lsTrvScriptsDir if item.endswith((".mel",".py"))]
    
    usrScriptsDir=pmc.
    lsDstScriptsDir=os.listdir(usrScriptsDir)
    lsAllDstScripts=[item for item in lsDstScriptsDir if item.endswith((".mel",".py"))]

    scriptsToCopy=[]
    pycDel=[]
    for item in lsAllSrcScripts:
        if item in lsAllDstScripts:
            srcFileTCode=os.stat("PATH"+item).st_mtime
            dstFileTCode= os.stat("PATH"+item).st_mtime
            if srcFileTCod!=dstFileTCod:
                if os.path.exists(usrScriptsFld+item+"c"):
                    pycDel.append(item+"c")
                    print "[Delete] "+usrScriptsFld+item+"c"
                print "[Update] "+item
                scriptsToCopy.append(item)
        else:
            print "[New] "+item
            scriptsToCopy.append(item)
    return scriptsToCopy, pycDel
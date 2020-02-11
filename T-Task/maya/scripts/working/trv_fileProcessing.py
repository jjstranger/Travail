testFile="C:/PRJ/dev/3001_JJS_PrjTst/VFX/sequences/SC001/SH_001/CG/scenes/Effects/abcOpSet_Test_jjs_v001.mb"

def getFileVersionStr(fileSourcName,verNumPad=3):
    verRuleStr="[._][vV]" # version String init
    for pad in range(verNumPad):
        verRuleStr+="\d"
    import re
    strSpltLs=re.split(verRuleStr,fileSourceName)
    if len(strSpltLs)==2:
        fileVerStr=re.search(verRuleStr,fileSourcName).group()[2:]
        return [fileVerStr,strSpltLs[0],strSpltLs[1]]
    else:
        return [None,strSpltLs[0],""]

    
def filePathDestruction(filePath):
    import os
    fileDir=os.path.dirname(filePath)
    fileBaseName=os.path.basename(filePath)
    getFileNameSplit=fileBaseName.rsplit(".",1)
    fileSourcName=getFileNameSplit[0]
    fileExt=getFileNameSplit[1]
    fileVer=getFileVersionStr(fileSourcName)[0]
    verPreStr= getFileVersionStr(fileSourcName)[1]
    verPstStr= getFileVersionStr(fileSourcName)[2]
    return [fileDir,fileBaseName,fileSourceName,fileExt,fileVer,verPreStr,verPstStr]

    
filePathDestruction(testFile)

testFile="C:/PRJ/dev/3001_JJS_PrjTst/VFX/sequences/SC001/SH_001/CG/scenes/Effects/abcOpSet_Test_jjs_v001.mb"

def getFileVersionStr(fileSourcName):
    verRuleStr="[\._][vV]\d+"
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

    
def raiseVerNum(filePath):
    getFileInfs= filePathDestruction(filePath)
    getFileDir=getFileInfs[0]
    fileRule=getFileInfs[5]+"[\._][vV]\d+[\._]*"+getFileInfs[6]+"."+getFileInfs[3]
    fileLs=[f for f in os.listdir(getFileDir) if re.findall(fileRule,f)]
    verStrLs=[]
    for f in fileLs:
         erStrLs.append(int(re.findall("[\._][vV]\d+[\._]*",f)[-1][2:-1]))
    verNum=str(max(verStrLs)+1)
    return verNum.zfill(3)

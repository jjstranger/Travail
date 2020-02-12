testFile="C:/PRJ/dev/3001_JJS_PrjTst/VFX/sequences/SC001/SH_001/CG/scenes/Effects/abcOpSet_Test_jjs_v001.mb"
import os,re

verRuleStr="[\._][vV]\d+[\._]*"
def getFileVersionStr(fileSourceName,verRuleStr="[\._][vV]\d+[\._]*"):
    strSpltLs=re.split(verRuleStr,fileSourceName)
    if len(strSpltLs)==2:
        fileVerStr=re.search(verRuleStr,fileSourceName).group()[2:]
        return [fileVerStr,strSpltLs[0],strSpltLs[1]]
    else:
        return [None,strSpltLs[0],""]

def filePathDestruction(filePath,verRuleStr="[\._][vV]\d+[\._]*"):
    fileDir=os.path.dirname(filePath)
    fileBaseName=os.path.basename(filePath)
    getFileNameSplit=fileBaseName.rsplit(".",1)
    fileSourceName=getFileNameSplit[0]
    fileExt=getFileNameSplit[1]
    getVerStrLs=getFileVersionStr(fileSourceName,verRuleStr)
    fileVer=getVerStrLs[0]
    verPreStr= getVerStrLs[1]
    verPstStr= getVerStrLs[2]
    return [fileDir,fileBaseName,fileSourceName,fileExt,fileVer,verPreStr,verPstStr]

def raiseVerNum(filePath,verRuleStr="[\._][vV]\d+[\._]*"):
    getFileInfs= filePathDestruction(filePath)
    getFileDir=getFileInfs[0]
    fileRule=getFileInfs[5]+verRuleStr+getFileInfs[6]+"."+getFileInfs[3]
    fileLs=[f for f in os.listdir(getFileDir) if re.findall(fileRule,f)]
    verStrLs=[]
    for f in fileLs:
         verStrLs.append(int(re.findall(verRuleStr,f)[-1][2:-1]))
    verNum=str(max(verStrLs)+1)
    return verNum.zfill(3)

print raiseVerNum(testFile,verRuleStr)
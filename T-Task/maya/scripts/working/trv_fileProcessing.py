import os
testFile="C:/PRJ/dev/3001_JJS_PrjTst/VFX/sequences/SC001/SH_001/CG/scenes/Effects/abcOpSet_Test_jjs_v001.mb"

def getFileVersionStr(fileSourcName,verNumPad=3):
    verRuleStr="[._][vV]" # version String init
    for pad in range(verNumPad):
        verRuleStr+="\d"
    import re
    fileVerStr=re.search(verRuleStr,fileSourcName).group()[2:]
    return fileVerStr
    
def filePathDestruction(filePath):
    fileDir=os.path.dirname(filePath)
    fileBaseName=os.path.basename(filePath)
    getFileNameSplit=fileBaseName.rsplit(".",1)
    fileSourcName=getFileNameSplit[0]
    fileExt=getFileNameSplit[1]
    fileVer=int(getFileVersionStr(fileSourcName))
    print "fileDir: "+fileDir
    print "fileBaseName: "+fileBaseName
    print "fileSourcName: "+fileSourcName
    print "fileExt: "+fileExt
    print "fileVer: "+fileVer

    
filePathDestruction(testFile)

import os, re
class publishFilePath(object):
    def getFileVersionStr(self,fileCoreName,verStrRule):
	    strSpltLs=re.split(verStrRule,fileCoreName)
	    if len(strSpltLs)==2:
	        fileVerStr=re.search(verStrRule,fileCoreName).group()[2:]
	        return [fileVerStr,strSpltLs[0],strSpltLs[1]]
	    else:
	        return [None,strSpltLs[0],""]

    def composeSrcFileName(self,pubDir,srcFileName,verStrRule):
		fileCoreName=srcFileName.rsplit(".",1)[0]
		fileExt=srcFileName.rsplit(".",1)[1]
		getVerStrLs=self.getFileVersionStr(fileCoreName,verStrRule)
		fileVer=getVerStrLs[0]
		verPreStr= getVerStrLs[1]
		verPstStr= getVerStrLs[2]
		fileFilter=verPreStr+verStrRule+verPstStr+"."+fileExt
		if fileVer==None:
		    fileName_OUT=verPreStr+"_v000."+fileExt
		else:
		    fileLs=[f for f in os.listdir(pubDir) if re.findall(fileFilter,f)]
		    verStrLs=[]
		    for f in fileLs:
		        verStrLs.append(int(re.findall(verStrRule,f)[-1][2:-1]))
		    verStr="_v"+str(max(verStrLs)+1).zfill(3)
		    fileName_OUT=verPreStr+verStr+verPstStr+"."+fileExt
		return fileName_OUT
        
    def __init__(self, pubDir,srcFileName,verStrRule="[\._][vV]\d+[\._]*"):
		#super(ClassName, self).__init__()
		#self.arg = arg
		self.pubDir=pubDir
		self.sourceFile=srcFileName
		self.fileCoreName=srcFileName.rsplit(".",1)[0]
		self.fileExt=srcFileName.rsplit(".",1)[1]
		self.fileVer=self.getFileVersionStr(self.fileCoreName,verStrRule)[0]
		self.pubFile=self.composeSrcFileName(pubDir,srcFileName,verStrRule)

''' test
pubDir="C:/PRJ/dev/3001_JJS_PrjTst/VFX/sequences/SC001/SH_001/CG/scenes/Effects/"
srcFile="abcOpSet_Test_jjs_v001.mb"
print publishFilePath(pubDir,srcFile).pubFile
'''
import os

def filePathDestruction(filePath):
    fileDir=os.path.dirname(filePath)
    fileBaseName=os.path.basename(filePath)
    getFileNameSplit=fileBaseName.rsplit(".",1)
    fileSourcName=getFileNameSplit[0]
    fileExt=getFileNameSplit[1]

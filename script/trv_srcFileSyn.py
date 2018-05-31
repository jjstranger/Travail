import os
import hashlib as hl
import pymel.core as pmc

def trv_chkSrcFileUpdtCmp():
	'''
	
	'''
	##### get ref files list #####
	refFilesLs=[]
	getRefFiles= pmc.ls(rf=1)
	#pmc.select(getRefFiles)
	for item in getRefFiles:
		filePath=pmc.referenceQuery(item,f=1)
		if(os.path.exists(os.path.abspath(filePath))):
			refFilesLs.append(filePath)		
			if pmc.attributeQuery((item+".modTimeCode"),ex=1)==0:
				#pmc.addAttr(item,ln="md5Code",dt="string")
				#pmc.setAttr((item+"md5Code"),l=1)
				pmc.addAttr(item,ln=".modTimeCode",dt="string")
				getModTime=os.stat(filePath).st_mtime
				pmc.setAttr((item+"modTimeCode"),getModTimeBeg,l=1)
			else:
				getModTime=os.stat(filePath).st_mtime
				if getModTime==pmc.getAttr(item+".modTimeCode"):
					pmc.button("trv_chkSrcFileUpdtBtn",e=1,l="No!",bgc=(1,0,0))
	
	print refFilesLs
	######
	##### get tex files list #####
	txFilesLs=[]
	getTexLs=pmc.ls(type="file")
	for item in getTexLs:
		filePath=pmc.getAttr(item+'.fileTextureName')
		if(os.path.exists(os.path.abspath(filePath))):
			txFilesLs.append(filePath)
			if pmc.attributeQuery((item+".modTimeCode"),ex=1)==0:
				#pmc.addAttr(item,ln="md5Code",dt="string")
				#pmc.setAttr((item+"md5Code"),l=1)
				pmc.addAttr(item,ln="modTimeCode",dt="string")
				getModTime=os.stat(filePath).st_mtime
				pmc.setAttr((item+".modTimeCode"),getModTimeBeg,l=1)
			else:
				getModTime=os.stat(filePath).st_mtime
				if getModTime==pmc.getAttr(item+".modTimeCode"):
					pmc.button("trv_chkSrcFileUpdtBtn",e=1,l="No!",bgc=(1,0,0))
	print txFilesLs
	######
	##### get alembic files list #####
	abcFilesLs=[]
	getAbcLs=pmc.ls(type="AlembicNode")
	for item in getAbcLs:
		filePath=pmc.getAttr(item+'.abc_File')
		if(os.path.exists(os.path.abspath(filePath))):
			abcFilesLs.append(filePath)
			if pmc.attributeQuery((item+".modTimeCode"),ex=1)==0:
				#pmc.addAttr(item,ln="md5Code",dt="string")
				#pmc.setAttr((item+"md5Code"),l=1)
				pmc.addAttr(item,ln="modTimeCode",dt="string")
				getModTime=os.stat(filePath).st_mtime
				pmc.setAttr((item+".modTimeCode"),getModTimeBeg,l=1)
			else:
				getModTime=os.stat(filePath).st_mtime
				if getModTime==pmc.getAttr(item+".modTimeCode"):
					pmc.button("trv_chkSrcFileUpdtBtn",e=1,l="No!",bgc=(1,0,0))
	print abcFilesLs
	######
	
	AllTikFilesLs = refFilesLs + txFilesLs + abcFilesLs



'''
if pmc.button("trv_chkSrcFileUpdtBtn",q=1,ex=1):
	pmc.deleteUI("trv_chkSrcFileUpdtBtn")
getSTLine=pmc.iconTextButton("statusFieldButton",q=1,p=1)
pmc.button("trv_chkSrcFileUpdtBtn",l="Good!",bgc=(.25,.25,.25),w=100,p=getSTLine)
'''
trv_chkSrcFileUpdtCmp()
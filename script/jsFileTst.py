import json as js

#### write json file ####
prjPath='d:/'
pmc.select(hi=1)
getSel=pmc.selected(tr=1)

jsFile=open(prjPath+'jsFileTst.json','w')
jsdata={}
for item in getSel:
    getObjNm=item
    getTMatrix=list(item.getMatrix()[0])+ list(item.getMatrix()[1])+ list(item.getMatrix()[2])+ list(item.getMatrix()[3])
    f[str(item)]={'assPath':'','type':'','parent':str(item.getParent()),'tMatrix':getTMatrix}
jsFile.write(js.dumps(jsdata,indent=4,separators=(', ',': ')))
jsFile.close()

#### load json file ####
loadJSFile=open('PATH')
cphJSFile=js.load(loadJSFile)


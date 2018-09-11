import json as js
prjPath='d:/'
pmc.select(hi=1)
getSel=pmc.selected(tr=1)

jsFile=open(prjPath+'jsFileTst.json','w')
jsdata={}
for item in getSel:
    getObjNm=item
    f[str(item)]={'assPath':'','type':'','parent':str(item.getParent()),'translate':list(item.getTranslation()),'rotation':list(item.getRotation()),'scale':list(item.getScale())}
jsFile.write(js.dumps(jsdata,indent=4,separators=(', ',': ')))
jsFile.close()

loadJSFile=open()
cphJSFile=js.load(loadJSFile)


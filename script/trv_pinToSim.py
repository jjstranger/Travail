from pymel import core as pmc

def trv_pin2Sim():
    pinSel=pmc.selected()
    if (pmc.pluginInfo('matrixNodes',q=1,l=1)==0:
        pmc.loadPlugin('matrixNodes')
    dcmpMtrx=pmc.createNode('decomposeMatrix')

    inverseTransLoc=pmc.spaceLocator(n='InverseTransLoc')
    pinSel[0].worldInverseMatrix >>dcmpMtrx.inputMattix
    dcmpMtrx.outputTranslate >> inverseTransLoc.translate
    dcmpMtrx.outputRotate >> inverseTransLoc.rotate
    dcmoMtrx.outputScale >> inverseTransLoc.scale
    pmc.refresh(su=1)
    pmc.bakeSimulation(inverseTransLoc,sm=1,t=(pmc.playbackOptions(q=1,min=1), pmc.playbackOptions(q=1,max=1)),sb=1,at=['tx','ty','tz','rx','ry','rz'])
    pmc.refresh(su=0)
    dcmpMtrx.outputTranslate // inverseTransLoc.translate
    dcmpMtrx.outputRotate // inverseTransLoc.rotate
    dcmoMtrx.outputScale // inverseTransLoc.scale

trv_pon2Sim()


#Follicle below 
sel=pmc.selected(fl=1)
geoName=pmc.ls(sel[-1].split('.')[0])
sumVec=[0,0,0]
for item in sel:
    getPPos=item.getPosition(space='world')
    sumVec+=pmc.datatypes.Vector(getPPos)
avrPPos=sumVec/len(sel)
dist=100000
for item in sel:
    getPDis=item.getPosition(space='world').distanceTo(avrPPos)
    if getPDis<dist:
        dist=getPDis
        pMin=item.getPosion(space='world')
        pUV=item.getUV()
curLocFollic=pmc.createNode('follicle',n='locFollicShape')
curLocFollicTsfm=pmc.listRelatives(curLocFollic,p=1)
geoName[0].worldMatrix >>curLocFollic.inputWorldMatrix
geoName[0].outMesh >>curLocFollic.inputMesh
curLocFollic.parameterU.set(pUV[0])
curLocFollic.parameterV.set(pUV[1])
curLocFollic.outTranslate >> curLocFollicTsfm[0].translate
curLocFollic.outRotate >> curLocFollicTsfm[0].rotate
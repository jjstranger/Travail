from pymel import core as pmc

def trv_pin2Sim():
    slState=selectionDetect()
    pinSel=pmc.selected()
    if (pmc.pluginInfo('matrixNodes',q=1,l=1)==0:
        pmc.loadPlugin('matrixNodes')
    dcmpMtrx=pmc.createNode('decomposeMatrix')
    multScl=pmc.createNode('multiplyDivide')
    multScl.operation.set(1)
    
    inverseTransLoc=createRootCurve()
    pinSel[0].worldInverseMatrix >>dcmpMtrx.inputMattix
    if slState=='GEO':
        pinSel[0].scale >> multScl.input1
    elif slState=='CPN':
        multScl.input.set([1,1,1])
    dcmpMtrx.outputTranslate >> multScl.input2
    multScl.output >> invertTransLoc.translate
    dcmpMtrx.outputRotate >> inverseTransLoc.rotate
    pmc.refresh(su=1)
    pmc.bakeResults(inverseTransLoc,sm=1,t=(pmc.playbackOptions(q=1,min=1), pmc.playbackOptions(q=1,max=1)),sb=1,at=['tx','ty','tz','rx','ry','rz'])
    pmc.refresh(su=0)
    multScl.output // inverseTransLoc.translate
    dcmpMtrx.outputRotate // inverseTransLoc.rotate

trv_pon2Sim()


### Vertexs Selected

def componentsSelected():
	#Follicle below 
	sel=pmc.selected(fl=1)
	geoName=pmc.ls(sel[-1].split('.')[0])
	#curUVSetName=pmc.polyUVSet(geoName[0],q=1,cuv=1)
	
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
	        nearestPoint=item
	pMin=nearestPoint.getPosition(space='world')
	pUV=[nearestPoint.getUVs()[0][0],nearestPoint.getUVs()[1][1]]
	#pUV=nearestPoint.getUV()#uvSet='map1')#not work before maya 2018
	curLocFollic=pmc.createNode('follicle',n='locFollicShape')
	curLocFollicTsfm=pmc.listRelatives(curLocFollic,p=1)
	geoName[0].worldMatrix >>curLocFollic.inputWorldMatrix
	geoName[0].outMesh >>curLocFollic.inputMesh
	curLocFollic.parameterU.set(pUV[0])
	curLocFollic.parameterV.set(pUV[1])
	curLocFollic.outTranslate >> curLocFollicTsfm[0].translate
	curLocFollic.outRotate >> curLocFollicTsfm[0].rotate
	return curLocFollicTsfm

#selection detec
def selectionDetect():
    if isinstance(pmc.selected()[0],(pmc.nodetypes.Transform,pmc.nodetypes.Shape)):
	    try:
		    len(pmc.selected())=1
            return 'GEO'
	    except:
		    pmc.error('Only one object can be selected.')
	    else:
		    pass
    elif isinstance(pmc.selected()[0],(pmc.MeshVertex)):
	    componentsSelected()

    elif isinstance(pmc.selected()[0],(pmc.MeshEdge, pmc.MeshFace)):
	    pmc.select(pmc.polyListComponentConversion(pmc.selected(),tv=1))
	    componentsSelected()
        return 'CPN'
    else:
        pmc.error('wrong type selection.')

def createRootCurve():
    invertRootCurve=pmc.curve(n='invertTransRoot',d=1,p=[...])
    return invertRootCurve
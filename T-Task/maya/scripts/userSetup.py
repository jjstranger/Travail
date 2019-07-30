###trv_cleanStartUpSettings

import os,stat
from pymel import core as pmc

srcPlgPrfFl=#'file path to scripts to copy'
dstPlgPrfFl=`pmc.internalVar(upd=1)`+'pluginPrefs.mel'

os.chmod(dstPlgPrfFl,stat.S_IWRITE)
pmc.sysFile(srcPlgPrfFl,cp=dstPlgPrfFl)

os.envrion['MAYA_DISABLE_CLIC_IPM']='1'
os.envrion['MAYA_DISABLE_CIP']='1'
os.envrion['MAYA_DISABLE_CER']='1'

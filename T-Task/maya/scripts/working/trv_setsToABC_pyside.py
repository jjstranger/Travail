from pymel import core as pmc
from PySide2 import QtCore, QtWidgets, QtUiTools,QtGui
from shiboken2 import wrapInstance
from maya.OpenMayaUI import * as omui

uiFile=""
def maya_main_win():
    getMayaMainWin=omui.MQtUtil.mainWindow()
    return wrapInstance(long(getMayaMainWin),QWidget)

class setsToABCUI(QDialog):
    def __init__(self,parent=maya_main_win()):
        super(setsToABCUI,self).__init__(parent)
        self.setWindowTitle("TVC Export To ABC")
        self.readUIFile()
        self.createLayout()
        self.createConnections()
    def readUIFile(self):
        f=QFile(uiFile)
        f.open(QFile.ReadOnly)
        loader=QtUiLoader()
        self.ui=loader.load(f,parentWidget=self)
        f.close()
    def createLayout(self):
        mainLayout=QVBoxLayout(self)
        mainLayout.addWidget(self.ui)
    def createConnections(self):
        pass


    def tskLstContent(self):
        self.model=QStandardItemModel(8,5)
        self.model.setHorizontalHeaderLabels([u"TaskName",u"Enable",u"StartFrame",u"EndFrame",u"OPPath"])
        self.ui.tskLs.setModel(self.model)
        self.ui.tskLs.resizeColumnToContent(1)
        self.ui.tskLs.verticalHeader().setVisible(0)
        self.ui.tskLs.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tskLs.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.tskLs.setAlternatingRowColors(1)
        self.ui.tskLs.verticalHeader().setDefaultSectionSize(22)

if __name__=="__main__":
    try:
        setsToABCUI().close()
        setsToABCUI().deleteLater()
    except:
        pass
    setsToABCUI().setFont(QFont("Microsoft YaHei",8))
    setsToABCUI().resize(400,550)
    setsToABCUI().tskLstContent()
    setsToABCUI().show()


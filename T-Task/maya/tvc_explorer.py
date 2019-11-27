#coding=utf-8
import os #sys, datetime
#import glob
from PySide2 import QtCore as pqc
from PySide2 import QtGui as pqg
from PySide2 import QtWidgets as pqw
#iconFolder = 'D:\\PyDev\\TVC_Submit\\ico\\'
iconFolder = 'S:\\Dev\\pythonDev\\TVC_Submit\\ico\\'
currentDir = u'E:/'




def fileSizeCpt(fileFullPath):
    strx = len(str(os.path.getsize(fileFullPath)))
    rawFileSize = float(os.path.getsize(fileFullPath))
    if 1 <= strx <= 3:
        fileSize = round(rawFileSize / (1024 ** 0), 0)
        fileSizeUnit = ' B'
    elif 4 <= strx <= 6:
        fileSize = round(rawFileSize / (1024 ** 1), 2)
        fileSizeUnit = ' KB'
    elif 7 <= strx <= 9:
        fileSize = round(rawFileSize / (1024 ** 2), 2)
        fileSizeUnit = ' MB'
    elif 10 <= strx <= 12:
        fileSize = round(rawFileSize / (1024 ** 3), 2)
        fileSizeUnit = ' Gb'
    elif 13 <= strx <= 15:
        fileSize = round(rawFileSize / (1024 ** 4), 2)
        fileSizeUnit = ' TB'
    elif 16 <= strx:
        fileSize = round(rawFileSize / (1024 ** 5), 2)
        fileSizeUnit = ' PB'
    return str(fileSize) + fileSizeUnit



class tvcExporerMainWin(pqw.QMainWindow):
    def __init__(self, parent=None):
        super(tvcExporerMainWin, self).__init__(parent)
        self.resize(1600, 900)
        self.setWindowTitle('TVC Projects Explorer')

        #####Menu
        fileMenu=self.menuBar().addMenu('&File')
        editMenu=self.menuBar().addMenu('&Edit')
        viewMenu=self.menuBar().addMenu('&View')
        langMenu=self.menuBar().addMenu('&Language')
        helpMenu=self.menuBar().addMenu('&Help')


        fileMenu.addAction('Add')

        closeAct=pqw.QAction('Close',self)
        closeAct.setShortcut('Ctrl+Q')
        closeAct.triggered.connect(self.close)
        #self.connect(closeAct,SIGNAL('triggered'),self.close)
        fileMenu.addAction(closeAct)

        copyAct=pqw.QAction('Copy',self)
        editMenu.addAction(copyAct)

        pasteAct=pqw.QAction('Paste',self)
        editMenu.addAction(pasteAct)
        explrModeAct = pqw.QAction('Explorer Mode', self)
        viewMenu.addAction(explrModeAct)
        prdModeAct= pqw.QAction('Production Mode',self)
        viewMenu.addAction(prdModeAct)

        chnLangAct=pqw.QAction(u'中文',self)
        langMenu.addAction(chnLangAct)
        engLangAct=pqw.QAction('English',self)
        langMenu.addAction(engLangAct)

        aboutAct=pqw.QAction('About',self)
        helpMenu.addAction(aboutAct)

        ####End of Menu

        mainWidget=pqw.QWidget()
        self.setCentralWidget(mainWidget)


        #####PathLine Grp
        pathLineRowLayout = pqw.QHBoxLayout()
        mainWidget.label_lookIn = pqw.QLabel("Look In: ",parent=mainWidget)
        # self.upBtn.isFlat()
        mainWidget.pathLine = pqw.QLineEdit(parent=mainWidget)
        mainWidget.pathLine.setText(currentDir)

        mainWidget.brswBtn = pqw.QPushButton("Browse..",parent=mainWidget)

        
        pathLineRowLayout.addWidget(mainWidget.label_lookIn)
        pathLineRowLayout.addWidget(mainWidget.pathLine)
        pathLineRowLayout.addWidget(mainWidget.brswBtn)
        pathLineRowLayout.setStretch(1, 1)
        #####End of Path Line Grp


        #####TabelWidget_Filelist
        def fileListTable(currentDir):
            fileNameList = []
            dirNameList = []
            for name in os.listdir(currentDir):
                if os.path.isdir(currentDir + name):
                    dirNameList.append(name)

                else:
                    fileNameList.append(name)

            combNameList = dirNameList + fileNameList
            mainWidget.fileListTable = pqw.QTableWidget(len(combNameList), 6)
            mainWidget.fileListTable.setHorizontalHeaderLabels([u'File', u'Last Update', u'Type', u'Size', u'Task', u'User'])

            i = 0
            for name in combNameList:
                fileFullPath = os.path.join(currentDir + name)
                #print fileFullPath
                baseName = os.path.basename(name)
                if (os.path.isdir(fileFullPath)):
                    addIcon = pqw.QTableWidgetItem(pqg.QIcon(iconFolder + 'folder.png'), baseName)

                    getFileSize = ""
                else:
                    addIcon = pqw.QTableWidgetItem(pqg.QIcon(iconFolder + 'maya.png'), baseName)
                    addIcon.setText(baseName)
                    getFileSize = fileSizeCpt(fileFullPath)

                addFileName = pqw.QTableWidgetItem(baseName)
                addLastTime = pqw.QTableWidgetItem(
                datetime.datetime.fromtimestamp(os.path.getmtime(fileFullPath)).strftime('%Y-%m-%d %H:%M:%S'))
                addLastTime.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                addType = pqw.QTableWidgetItem('Type')
                addType.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                addSize = pqw.QTableWidgetItem(getFileSize)
                addSize.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                addTask = pqw.QTableWidgetItem('Task')
                addTask.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                addUsr = pqw.QTableWidgetItem('User')
                addUsr.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)

                mainWidget.fileListTable.setItem(i, 0, addIcon)
                mainWidget.fileListTable.setItem(i, 1, addLastTime)
                mainWidget.fileListTable.setItem(i, 2, addType)
                mainWidget.fileListTable.setItem(i, 3, addSize)
                mainWidget.fileListTable.setItem(i, 4, addTask)
                mainWidget.fileListTable.setItem(i, 5, addUsr)

                i += 1

            mainWidget.fileListTable.setShowGrid(False)
            mainWidget.fileListTable.resizeColumnToContents(True)
            # mainWidget.fileListTable.horizontalHeader().setStretchLastSection(True)
            mainWidget.fileListTable.horizontalHeader().setHighlightSections(False)
            mainWidget.fileListTable.verticalHeader().setVisible(False)
            mainWidget.fileListTable.horizontalHeader().resizeSection(0, 250)
            mainWidget.fileListTable.setSelectionBehavior(pqw.QAbstractItemView.SelectRows)
            mainWidget.fileListTable.setSelectionMode(pqw.QAbstractItemView.ExtendedSelection)
            mainWidget.fileListTable.setAlternatingRowColors(True)
            mainWidget.fileListTable.verticalHeader().setDefaultSectionSize(50)
            mainWidget.fileListTable.setIconSize(pqc.QSize(48,48))

        fileListTable(currentDir)




        # mainWidget.fileListTable.doubleClicked()

        #####End of TabelWidget

        mainWidget.prjLabHBLyt=pqw.QHBoxLayout()
        mainWidget.prjNavLabel=pqw.QLabel('Projects: ')
        mainWidget.prjSrchTxtField=pqw.QLineEdit()
        mainWidget.prjSrchBtn=pqw.QPushButton("Search")
        mainWidget.prjList = pqw.QListWidget()
        lb_prjOutline=pqw.QLabel("Project Outline: ")
        tw_prjOutline=pqw.QTreeWidget()
        #mainWidget.prjList.addItem('TVC Root')
        #mainWidget.prjList.show()
        mainWidget.prjLabHBLyt.addWidget(mainWidget.prjNavLabel)
        mainWidget.prjLabHBLyt.addWidget(mainWidget.prjSrchTxtField)
        mainWidget.prjLabHBLyt.addWidget(mainWidget.prjSrchBtn)

        mainWidget.prvFiled = pqw.QWidget()
        mainWidget.prvFiled.setFixedSize(320, 240)
        #mainWidget.prvFiled.show()
        
        #add in
        mainWidget.subPthBrswrVBLyt=pqw.QVBoxLayout()
        mainWidget.pthTrainHBLyt=pqw.QHBoxLayout()
        mainWidget.pthTrainHBLyt.setSpacing(1)
        mainWidget.lb_pthTrainLbTx=pqw.QLabel(">>")
        mainWidget.pthTrainHBLyt.addWidget(mainWidget.lb_pthTrainLbTx)
        mainWidget.trainSectionsHBLyt=pqw.QHBoxLayout()
        mainWidget.pthTrainHBLyt.addLayout(mainWidget.trainSectionsHBLyt)
        for pthSec in pthTrainSect:
            pthSecPb=pqw.QPushButton(pthSec)
            #pthSecPb.setFixedHeight(22)
            trainSectionsHBLyt.addWidget(pthSecPb)
            
        mainWidget.flSrchHBLyt=pqw.QHBoxLayout()
        mainWidget.ln_flSrchLn=pqw.QLineEdit()
        mainWidget.pb_flSrchPb=pqw.QPushButton("Search")
        mainWidget.trainSectionsHBLyt.addStretch()

        mainWidget.pthTrainHBLyt.addLayout(mainWidget.flSrchHBLyt)
        mainWidget.flSrchHBLyt.addWidget(mainWidget.ln_flSrchLn)
        mainWidget.ln_flSrchLn.setMaximumWidth(200)
        mainWidget.flSrchHBLyt.addWidget(mainWidget.pb_flSrchPb)
        mainWidget.pb_flSrchPb.setMaximumWidth(80)
        ##add in End
        
        #file List
        mainWidget.prptTable = pqw.QTableWidget(8, 2)
        mainWidget.prptTable.verticalHeader().setVisible(False)
        mainWidget.prptTable.setHorizontalHeaderLabels([u'Property', u'Value'])
        mainWidget.prptTable.horizontalHeader().setStretchLastSection(True)
        prptNameItem=pqw.QTableWidgetItem('Name')
        prptNameItem.setTextAlignment(pqc.Qt.AlignLeft)
        mainWidget.prptTable.setItem(0,0,prptNameItem)
        prptTypeItem=pqw.QTableWidgetItem('Type')
        prptTypeItem.setTextAlignment(pqc.Qt.AlignLeft)
        mainWidget.prptTable.setItem(1,0,prptTypeItem)
        prptSizeItem = pqw.QTableWidgetItem('Size')
        prptSizeItem.setTextAlignment(pqc.Qt.AlignLeft)
        mainWidget.prptTable.setItem(2,0, prptSizeItem)
        prptLstdItem=pqw.QTableWidgetItem('Last Update')
        prptLstdItem.setTextAlignment(pqc.Qt.AlignLeft)
        mainWidget.prptTable.setItem(3,0,prptLstdItem)
        prptTskItem = pqw.QTableWidgetItem('Task')
        prptTskItem.setTextAlignment(pqc.Qt.AlignLeft)
        mainWidget.prptTable.setItem(4, 0, prptTskItem)
        prptUsrItem=pqw.QTableWidgetItem('User')
        prptUsrItem.setTextAlignment(pqc.Qt.AlignLeft)
        mainWidget.prptTable.setItem(5,0,prptUsrItem)

        mainWidget.prptTable.setShowGrid(False)
        mainWidget.prptTable.resizeColumnToContents(True)
        mainWidget.prptTable.setShowGrid(False)
        mainWidget.prptTable.setEditTriggers(pqw.QAbstractItemView.NoEditTriggers)
        mainWidget.prptTable.setSelectionMode(pqw.QAbstractItemView.NoSelection)

        # mainWidget.prptTable.horizontalHeader().setStretchLastSection(True)
        #mainWidget.prptTable.show()
        # file List End
        
        # fileName & Buttons
        flNmLnHBLyt=pqw.QHBoxLayout()
        lb_flNm=pqw.QLabel("File:")
        le_flNmLE=pqw.QLineEdit()
        cb_flTyp=pqw.QComboBox()
        
        flNmLnHBLyt.addWidget(lb_flNm)
        flNmLnHBLyt.addWidget(le_flNmLE)
        flNmLnHBLyt.addWidget(cb_flTyp)
        
        cmdPBHBLyt=pqw.QHBoxLayout()
        pb_new=pqw.QPushButton("New")
        pb_load=pqw.QPushButton("Load")
        pb_nest=pqw.QPushButton("Nest")
        pb_nth=pqw.QPushButton("Save")
        
        
        cmdPBHBLyt.addWidget(pb_new)
        cmdPBHBLyt.addWidget(pb_load)
        cmdPBHBLyt.addWidget(pb_nest)
        cmdPBHBLyt.addWidget(pb_nth)
        

        prptLayout = pqw.QVBoxLayout()
        prptLayout.addWidget(mainWidget.prvFiled)
        prptLayout.addWidget(mainWidget.prptTable)
        navColmnLayout = pqw.QVBoxLayout()
        navColmnLayout.addLayout(mainWidget.prjLabHBLyt)
        navColmnLayout.addWidget(mainWidget.prjList)
        navColmnLayout.addWidget(lb_prjOutline)
        navColmnLayout.addWidget(tw_prjOutline)
        
        rightBrswPanel=pqw.QVBoxLayout()
        rightBrswPanel.addLayout(mainWidget.pthTrainHBLyt)
        rightBrswPanel.addWidget(mainWidget.fileListTable)
        rightBrswPanel.addLayout(flNmLnHBLyt)
        rightBrswPanel.addLayout(cmdPBHBLyt)
        
        rowLstLayout = pqw.QHBoxLayout()
        rowLstLayout.addLayout(navColmnLayout)
        rowLstLayout.addLayout(rightBrswPanel)
        #rowLstLayout.addLayout(prptLayout)
        rowLstLayout.setStretch(1, 1)
        rowLstLayout.setStretchFactor(mainWidget.prjList,2)
        rowLstLayout.setStretchFactor(rightBrswPanel, 5)
        rowLstLayout.setStretchFactor(prptLayout, 3)



        mainLayout = pqw.QVBoxLayout()
        #mainLayout.addWidget(menuBar)
        mainLayout.addLayout(pathLineRowLayout)
        mainLayout.addLayout(rowLstLayout)
        mainWidget.setLayout(mainLayout)

        mainWidget.setParent(self)
        mainWidget.setLayoutDirection(pqc.Qt.LayoutDirectionAuto)
        #mainWidget.show()


        #$$$%^&&^&^(*&_^_&+(*(^&$%@!^#@&$$$^%)(*&+)(+*(&*(^&$$#$!@#$!
        #mainWidget.fileListTable.setRangeSelected(QTableWidgetSelectionRange(0, 0, 1, 1), True)

        def selectShowPrpt (self):

            for idx in mainWidget.fileListTable.selectionModel().selectedRows():
                rowNum= idx.row()
                nameInfo=mainWidget.fileListTable.item(rowNum,0)
                typeInfo=mainWidget.fileListTable.item(rowNum,2)
                sizeInfo=mainWidget.fileListTable.item(rowNum,3)
                lastUpdtInfo= mainWidget.fileListTable.item(rowNum,1)
                tskInfo=mainWidget.fileListTable.item(rowNum,4)
                usrInfo=mainWidget.fileListTable.item(rowNum,5)


                addPrptName=pqw.QTableWidgetItem(nameInfo.text())
                addPrptName.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                mainWidget.prptTable.setItem(0, 1, addPrptName)

                addPrptType=pqw.QTableWidgetItem(typeInfo.text())
                addPrptType.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                mainWidget.prptTable.setItem(1, 1, addPrptType)

                addPrptSize = pqw.QTableWidgetItem(sizeInfo.text())
                addPrptSize.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                mainWidget.prptTable.setItem(2, 1, addPrptSize)

                addPrptLstUpdt = pqw.QTableWidgetItem(lastUpdtInfo.text())
                addPrptLstUpdt.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                mainWidget.prptTable.setItem(3, 1, addPrptLstUpdt)

                addPrptTsk=pqw.QTableWidgetItem(tskInfo.text())
                addPrptTsk.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                mainWidget.prptTable.setItem(4, 1, addPrptTsk)

                addPrptUsr=pqw.QTableWidgetItem(usrInfo.text())
                addPrptUsr.setTextAlignment(pqc.Qt.AlignRight | pqc.Qt.AlignCenter)
                mainWidget.prptTable.setItem(5, 1, addPrptUsr)

        def openFileOfItem(self):
            for idx in mainWidget.fileListTable.selectionModel().selectedRows():
                rowNum = idx.row()
                nameInfo = mainWidget.fileListTable.item(rowNum, 0)
                if os.path.isdir(currentDir+nameInfo.text())==0:
                    os.startfile(currentDir+nameInfo.text())#Windows
                    #subprocess.call(["xdg-open", file])#linux
                    #subprocess.call(["open", file])#mac
                else:
                    currentDir=currentDir+nameInfo.text()+'/'
                    fileListTable(currentDir)



        mainWidget.fileListTable.itemClicked.connect(selectShowPrpt)
        mainWidget.fileListTable.doubleClicked.connect(openFileOfItem)
        #self.connect(mainWidget.fileListTable, SIGNAL("itemClicked (QTableWidgetItem*)"), outSelect# )
        #mainWidget.fileListTable.cellActivated.connect(openFileOfItem)



if __name__ == '__main__':
    #tvcExplrApp = QApplication(sys.argv)#disable In Maya
    #tvcExplrApp.setFont(QFont('Microsoft YaHei', 10))  # set default font

    tvcExplrWin = tvcExporerMainWin()
    #tvcExplrWin.languageChange()
    tvcExplrWin.setFont(pqg.QFont('Microsoft YaHei', 9))  # set default font

    tvcExplrWin.show()
    #sys.exit(tvcExplrApp.exec_())
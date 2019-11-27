# coding=utf-8
import sys, os, datetime
import glob
from PySide.QtCore import *
from PySide.QtGui import *
#iconFolder = 'D:\\PyDev\\TVC_Submit\\ico\\'
iconFolder = 'S:\\Dev\\pythonDev\\TVC_Submit\\ico\\'
currentDir = u'd:/'




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



class tvcExporerMainWin(QMainWindow):
    def __init__(self, parent=None):

        super(tvcExporerMainWin, self).__init__(parent)



        self.resize(1284, 845)
        self.setWindowTitle('TVC Projects Explorer')

        #####Menu
        fileMenu=self.menuBar().addMenu('&File')
        editMenu=self.menuBar().addMenu('&Edit')
        viewMenu=self.menuBar().addMenu('&View')
        langMenu=self.menuBar().addMenu('&Language')
        helpMenu=self.menuBar().addMenu('&Help')


        fileMenu.addAction('Add')

        closeAct=QAction('Close',self)
        closeAct.setShortcut('Ctrl+Q')
        closeAct.triggered.connect(self.close)
        #self.connect(closeAct,SIGNAL('triggered'),self.close)
        fileMenu.addAction(closeAct)

        copyAct=QAction('Copy',self)
        editMenu.addAction(copyAct)

        pasteAct=QAction('Paste',self)
        editMenu.addAction(pasteAct)
        explrModeAct = QAction('Explorer Mode', self)
        viewMenu.addAction(explrModeAct)
        prdModeAct= QAction('Production Mode',self)
        viewMenu.addAction(prdModeAct)

        chnLangAct=QAction(u'中文',self)
        langMenu.addAction(chnLangAct)
        engLangAct=QAction('English',self)
        langMenu.addAction(engLangAct)

        aboutAct=QAction('About',self)
        helpMenu.addAction(aboutAct)

        ####End of Menu

        mainWidget=QWidget()
        self.setCentralWidget(mainWidget)



        #####PathLine Grp
        mainWidget.upBtn = QPushButton(parent=mainWidget)
        mainWidget.upBtn.setIcon(QIcon(iconFolder + 'up.png'))
        mainWidget.upBtn.setText('UP')
        # self.upBtn.isFlat()
        mainWidget.pathLine = QLineEdit(parent=mainWidget)
        mainWidget.pathLine.setText(currentDir)

        mainWidget.srchLine = QLineEdit(parent=mainWidget)

        pathLineRowLayout = QHBoxLayout()
        pathLineRowLayout.addWidget(mainWidget.upBtn)
        pathLineRowLayout.addWidget(mainWidget.pathLine)
        pathLineRowLayout.addWidget(mainWidget.srchLine)
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
            mainWidget.fileListTable = QTableWidget(len(combNameList), 6)
            mainWidget.fileListTable.setHorizontalHeaderLabels([u'File', u'Last Update', u'Type', u'Size', u'Task', u'User'])

            i = 0
            for name in combNameList:
                fileFullPath = os.path.join(currentDir + name)
                #print fileFullPath
                baseName = os.path.basename(name)
                if (os.path.isdir(fileFullPath)):
                    addIcon = QTableWidgetItem(QIcon(iconFolder + 'folder.png'), baseName)

                    getFileSize = ""
                else:
                    addIcon = QTableWidgetItem(QIcon(iconFolder + 'maya.png'), baseName)
                    addIcon.setText(baseName)
                    getFileSize = fileSizeCpt(fileFullPath)

                addFileName = QTableWidgetItem(baseName)
                addLastTime = QTableWidgetItem(
                datetime.datetime.fromtimestamp(os.path.getmtime(fileFullPath)).strftime('%Y-%m-%d %H:%M:%S'))
                addLastTime.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                addType = QTableWidgetItem('Type')
                addType.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                addSize = QTableWidgetItem(getFileSize)
                addSize.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                addTask = QTableWidgetItem('Task')
                addTask.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                addUsr = QTableWidgetItem('User')
                addUsr.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

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
            mainWidget.fileListTable.setSelectionBehavior(QAbstractItemView.SelectRows)
            mainWidget.fileListTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
            mainWidget.fileListTable.setAlternatingRowColors(True)
            mainWidget.fileListTable.verticalHeader().setDefaultSectionSize(50)
            mainWidget.fileListTable.setIconSize(QSize(48,48))

        fileListTable(currentDir)




        # mainWidget.fileListTable.doubleClicked()

        #####End of TabelWidget

        mainWidget.navLabel=QLabel('Navigator')
        mainWidget.guideList = QListWidget()
        mainWidget.guideList.addItem('TVC Root')
        mainWidget.guideList.show()

        mainWidget.prvFiled = QWidget()
        mainWidget.prvFiled.setFixedSize(320, 240)
        mainWidget.prvFiled.show()

        mainWidget.prptTable = QTableWidget(8, 2)
        mainWidget.prptTable.verticalHeader().setVisible(False)
        mainWidget.prptTable.setHorizontalHeaderLabels([u'Property', u'Value'])
        mainWidget.prptTable.horizontalHeader().setStretchLastSection(True)
        prptNameItem=QTableWidgetItem('Name')
        prptNameItem.setTextAlignment(Qt.AlignLeft)
        mainWidget.prptTable.setItem(0,0,prptNameItem)
        prptTypeItem=QTableWidgetItem('Type')
        prptTypeItem.setTextAlignment(Qt.AlignLeft)
        mainWidget.prptTable.setItem(1,0,prptTypeItem)
        prptSizeItem = QTableWidgetItem('Size')
        prptSizeItem.setTextAlignment(Qt.AlignLeft)
        mainWidget.prptTable.setItem(2,0, prptSizeItem)
        prptLstdItem=QTableWidgetItem('Last Update')
        prptLstdItem.setTextAlignment(Qt.AlignLeft)
        mainWidget.prptTable.setItem(3,0,prptLstdItem)
        prptTskItem = QTableWidgetItem('Task')
        prptTskItem.setTextAlignment(Qt.AlignLeft)
        mainWidget.prptTable.setItem(4, 0, prptTskItem)
        prptUsrItem=QTableWidgetItem('User')
        prptUsrItem.setTextAlignment(Qt.AlignLeft)
        mainWidget.prptTable.setItem(5,0,prptUsrItem)

        mainWidget.prptTable.setShowGrid(False)
        mainWidget.prptTable.resizeColumnToContents(True)
        mainWidget.prptTable.setShowGrid(False)
        mainWidget.prptTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        mainWidget.prptTable.setSelectionMode(QAbstractItemView.NoSelection)



        # mainWidget.prptTable.horizontalHeader().setStretchLastSection(True)
        mainWidget.prptTable.show()

        prptLayout = QVBoxLayout()
        prptLayout.addWidget(mainWidget.prvFiled)
        prptLayout.addWidget(mainWidget.prptTable)
        navColmnLayout = QVBoxLayout()
        navColmnLayout.addWidget(mainWidget.navLabel)
        navColmnLayout.addWidget(mainWidget.guideList)
        rowLstLayout = QHBoxLayout()
        rowLstLayout.addLayout(navColmnLayout)
        rowLstLayout.addWidget(mainWidget.fileListTable)
        rowLstLayout.addLayout(prptLayout)
        rowLstLayout.setStretch(1, 1)
        rowLstLayout.setStretchFactor(mainWidget.guideList,2)
        rowLstLayout.setStretchFactor(mainWidget.fileListTable, 5)
        rowLstLayout.setStretchFactor(prptLayout, 3)



        mainLayout = QVBoxLayout()
        #mainLayout.addWidget(menuBar)
        mainLayout.addLayout(pathLineRowLayout)
        mainLayout.addLayout(rowLstLayout)
        mainWidget.setLayout(mainLayout)

        mainWidget.setParent(self)
        mainWidget.setLayoutDirection(Qt.LayoutDirectionAuto)
        mainWidget.show()


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


                addPrptName=QTableWidgetItem(nameInfo.text())
                addPrptName.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                mainWidget.prptTable.setItem(0, 1, addPrptName)

                addPrptType=QTableWidgetItem(typeInfo.text())
                addPrptType.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                mainWidget.prptTable.setItem(1, 1, addPrptType)

                addPrptSize = QTableWidgetItem(sizeInfo.text())
                addPrptSize.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                mainWidget.prptTable.setItem(2, 1, addPrptSize)

                addPrptLstUpdt = QTableWidgetItem(lastUpdtInfo.text())
                addPrptLstUpdt.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                mainWidget.prptTable.setItem(3, 1, addPrptLstUpdt)

                addPrptTsk=QTableWidgetItem(tskInfo.text())
                addPrptTsk.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                mainWidget.prptTable.setItem(4, 1, addPrptTsk)

                addPrptUsr=QTableWidgetItem(usrInfo.text())
                addPrptUsr.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
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
    tvcExplrWin.setFont(QFont('Microsoft YaHei', 10))  # set default font

    tvcExplrWin.show()
    #sys.exit(tvcExplrApp.exec_())
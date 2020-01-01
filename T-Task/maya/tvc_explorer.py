#coding=utf-8
import os, datetime #sys,
#import glob
from PySide2 import QtCore as pqc
from PySide2 import QtGui as pqg
from PySide2 import QtWidgets as pqw
#iconFolder = 'D:\\PyDev\\TVC_Submit\\ico\\'
#iconFolder = 'S:\\Dev\\pythonDev\\TVC_Submit\\ico\\'
prjRoot = u'E:/'
pthTrainSect={}#Remove Late

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

        ##### prjRootFinder
        prjRootFinderHBLyt = pqw.QHBoxLayout()
        prjRootFinderHBLyt_label_lookIn = pqw.QLabel("Look In: ",parent=mainWidget)
        # self.upBtn.isFlat()
        prjRootFinderHBLyt_pathLine = pqw.QLineEdit(parent=mainWidget)
        prjRootFinderHBLyt_pathLine.setText(prjRoot)
        prjRootFinderHBLyt_PBtn_brwsBtn = pqw.QPushButton("Browse..",parent=mainWidget)
        prjRootFinderHBLyt.addWidget(prjRootFinderHBLyt_label_lookIn)
        prjRootFinderHBLyt.addWidget(prjRootFinderHBLyt_pathLine)
        prjRootFinderHBLyt.addWidget(prjRootFinderHBLyt_PBtn_brwsBtn)
        prjRootFinderHBLyt.setStretch(1, 1)
        #####End of Path Line Grp

        navigatorBVLyt_prjSrchHBlyt=pqw.QHBoxLayout()
        prjSrchHBlyt_label_prj=pqw.QLabel('Projects: ')
        prjSrchHBlyt_lineEdit_prjSrchText=pqw.QLineEdit()
        prjSrchHBlyt_PBtn_prjSrchBtn=pqw.QPushButton("Search")
        navigatorBVLyt_lst_prjLst = pqw.QListWidget()
        navigatorBVLyt_label_prjOtln=pqw.QLabel("Project Outline: ")
        navigatorBVLyt_treeWidget_prjOtlnLst=pqw.QTreeWidget()
        navigatorBVLyt_prjSrchHBlyt.addWidget(prjSrchHBlyt_label_prj)
        navigatorBVLyt_prjSrchHBlyt.addWidget(prjSrchHBlyt_lineEdit_prjSrchText)
        navigatorBVLyt_prjSrchHBlyt.addWidget(prjSrchHBlyt_PBtn_prjSrchBtn)

        #mainWidget.prvFiled = pqw.QWidget()
        #mainWidget.prvFiled.setFixedSize(320, 240)
        #mainWidget.prvFiled.show()
        
        fileLstOperatorVBLyt=pqw.QVBoxLayout()
        fileLstOperatorVBLyt_pthTrainAndFileSrchHBLyt=pqw.QHBoxLayout()
        pthTrainAndFileSrchHBLyt_pthTrainHBLyt=pqw.QHBoxLayout()
        pthTrainAndFileSrchHBLyt_pthTrainHBLyt.setSpacing(1)
        pthTrainHBLyt_label_pthTrainLabelText=pqw.QLabel(">>")
        pthTrainAndFileSrchHBLyt_pthTrainHBLyt.addWidget(pthTrainHBLyt_label_pthTrainLabelText)
        pthTrainHBLyt_trainSecsHBLyt=pqw.QHBoxLayout()
        pthTrainAndFileSrchHBLyt_pthTrainHBLyt.addLayout(pthTrainHBLyt_trainSecsHBLyt)
        for pthSec in pthTrainSect:
            pthTrainHBLyt_pthSecPb=pqw.QPushButton(pthSec)
            #pthTrainHBLyt_pthSecPb.setFixedHeight(22)
            trainSectionsHBLyt.addWidget(pthTrainHBLyt_pthSecPb)
            
        trainSectionsHBLyt_flSrchHBLyt=pqw.QHBoxLayout()
        flSrchHBLyt_lineEdit_fileSrchText=pqw.QLineEdit()
        flSrchHBLyt_PBtn_flSrchPBtn=pqw.QPushButton("Search")
        pthTrainHBLyt_trainSecsHBLyt.addStretch()

        pthTrainAndFileSrchHBLyt_pthTrainHBLyt.addLayout(trainSectionsHBLyt_flSrchHBLyt)
        trainSectionsHBLyt_flSrchHBLyt.addWidget(flSrchHBLyt_lineEdit_fileSrchText)
        flSrchHBLyt_lineEdit_fileSrchText.setMaximumWidth(200)
        trainSectionsHBLyt_flSrchHBLyt.addWidget(flSrchHBLyt_PBtn_flSrchPBtn)
        flSrchHBLyt_PBtn_flSrchPBtn.setMaximumWidth(80)
        
        fileLstOperatorVBLyt_fileListTable = pqw.QTableWidget(20, 6)
        fileLstOperatorVBLyt_fileListTable.setHorizontalHeaderLabels([u'File', u'Type', u'Size', u'Last Update',u'Task', u'User'])
        fileLstOperatorVBLyt_fileListTable.setShowGrid(False)
        fileLstOperatorVBLyt_fileListTable.resizeColumnToContents(True)
        # fileLstOperatorVBLyt_fileListTable.horizontalHeader().setStretchLastSection(True)
        fileLstOperatorVBLyt_fileListTable.horizontalHeader().setHighlightSections(False)
        fileLstOperatorVBLyt_fileListTable.verticalHeader().setVisible(False)
        fileLstOperatorVBLyt_fileListTable.horizontalHeader().resizeSection(0, 250)
        fileLstOperatorVBLyt_fileListTable.setSelectionBehavior(pqw.QAbstractItemView.SelectRows)
        fileLstOperatorVBLyt_fileListTable.setSelectionMode(pqw.QAbstractItemView.ExtendedSelection)
        fileLstOperatorVBLyt_fileListTable.setAlternatingRowColors(True)
        fileLstOperatorVBLyt_fileListTable.verticalHeader().setDefaultSectionSize(50)
        fileLstOperatorVBLyt_fileListTable.setIconSize(pqc.QSize(48,48))
        
        '''
        #property List
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
        '''

        # fileNameEditor & Buttons
        fileLstOperatorVBLyt_fileNameEditorHBLyt=pqw.QHBoxLayout()
        fileNameEditorHBLyt_label_file=pqw.QLabel("File:")
        fileNameEditorHBLyt_lineEdit_fileNameText=pqw.QLineEdit()
        fileNameEditorHBLyt_comboBox_fileTypeFilter=pqw.QComboBox()
        
        fileLstOperatorVBLyt_fileNameEditorHBLyt.addWidget(fileNameEditorHBLyt_label_file)
        fileLstOperatorVBLyt_fileNameEditorHBLyt.addWidget(fileNameEditorHBLyt_lineEdit_fileNameText)
        fileLstOperatorVBLyt_fileNameEditorHBLyt.addWidget(fileNameEditorHBLyt_comboBox_fileTypeFilter)
        
        fileLstOperatorVBLyt_cmdPBtnHBLyt=pqw.QHBoxLayout()
        cmdPBtnHBLyt_PBtn_new=pqw.QPushButton("New")
        cmdPBtnHBLyt_PBtn_load=pqw.QPushButton("Load")
        cmdPBtnHBLyt_PBtn_nest=pqw.QPushButton("Nest")
        cmdPBtnHBLyt_PBtn_save=pqw.QPushButton("Save")
        
        fileLstOperatorVBLyt_cmdPBtnHBLyt.addWidget(cmdPBtnHBLyt_PBtn_new)
        fileLstOperatorVBLyt_cmdPBtnHBLyt.addWidget(cmdPBtnHBLyt_PBtn_load)
        fileLstOperatorVBLyt_cmdPBtnHBLyt.addWidget(cmdPBtnHBLyt_PBtn_nest)
        fileLstOperatorVBLyt_cmdPBtnHBLyt.addWidget(cmdPBtnHBLyt_PBtn_save)

        #prptLayout = pqw.QVBoxLayout()
        #prptLayout.addWidget(mainWidget.prvFiled)
        #prptLayout.addWidget(mainWidget.prptTable)
        navigatorBVLyt = pqw.QVBoxLayout()
        navigatorBVLyt.addLayout(navigatorBVLyt_prjSrchHBlyt)
        navigatorBVLyt.addWidget(navigatorBVLyt_lst_prjLst)
        navigatorBVLyt.addWidget(navigatorBVLyt_label_prjOtln)
        navigatorBVLyt.addWidget(navigatorBVLyt_treeWidget_prjOtlnLst)
               
        fileLstOperatorVBLyt.addLayout(pthTrainAndFileSrchHBLyt_pthTrainHBLyt)
        fileLstOperatorVBLyt.addWidget(fileLstOperatorVBLyt_fileListTable)
        fileLstOperatorVBLyt.addLayout(fileLstOperatorVBLyt_fileNameEditorHBLyt)
        fileLstOperatorVBLyt.addLayout(fileLstOperatorVBLyt_cmdPBtnHBLyt)
        
        rowLstLayout = pqw.QHBoxLayout()
        rowLstLayout.addLayout(navigatorBVLyt)
        rowLstLayout.addLayout(fileLstOperatorVBLyt)
        #rowLstLayout.addLayout(prptLayout)
        rowLstLayout.setStretch(1, 1)
        rowLstLayout.setStretchFactor(navigatorBVLyt_lst_prjLst,2)
        rowLstLayout.setStretchFactor(fileLstOperatorVBLyt, 5)
        #rowLstLayout.setStretchFactor(prptLayout, 3)

        mainLayout = pqw.QVBoxLayout()
        #mainLayout.addWidget(menuBar)
        mainLayout.addLayout(prjRootFinderHBLyt)
        mainLayout.addLayout(rowLstLayout)
        mainWidget.setLayout(mainLayout)

        mainWidget.setParent(self)
        mainWidget.setLayoutDirection(pqc.Qt.LayoutDirectionAuto)
        #mainWidget.show()

        #$$$%^&&^&^(*&_^_&+(*(^&$%@!^#@&$$$^%)(*&+)(+*(&*(^&$$#$!@#$!
        #fileLstOperatorVBLyt_fileListTable.setRangeSelected(QTableWidgetSelectionRange(0, 0, 1, 1), True)

        '''
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
            fileLstOperatorVBLyt_fileListTable = pqw.QTableWidget(len(combNameList), 6)
            fileLstOperatorVBLyt_fileListTable.setHorizontalHeaderLabels([u'File', u'Last Update', u'Type', u'Size', u'Task', u'User'])

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

                fileLstOperatorVBLyt_fileListTable.setItem(i, 0, addIcon)
                fileLstOperatorVBLyt_fileListTable.setItem(i, 1, addLastTime)
                fileLstOperatorVBLyt_fileListTable.setItem(i, 2, addType)
                fileLstOperatorVBLyt_fileListTable.setItem(i, 3, addSize)
                fileLstOperatorVBLyt_fileListTable.setItem(i, 4, addTask)
                fileLstOperatorVBLyt_fileListTable.setItem(i, 5, addUsr)

                i += 1

            fileLstOperatorVBLyt_fileListTable.setShowGrid(False)
            fileLstOperatorVBLyt_fileListTable.resizeColumnToContents(True)
            # fileLstOperatorVBLyt_fileListTable.horizontalHeader().setStretchLastSection(True)
            fileLstOperatorVBLyt_fileListTable.horizontalHeader().setHighlightSections(False)
            fileLstOperatorVBLyt_fileListTable.verticalHeader().setVisible(False)
            fileLstOperatorVBLyt_fileListTable.horizontalHeader().resizeSection(0, 250)
            fileLstOperatorVBLyt_fileListTable.setSelectionBehavior(pqw.QAbstractItemView.SelectRows)
            fileLstOperatorVBLyt_fileListTable.setSelectionMode(pqw.QAbstractItemView.ExtendedSelection)
            fileLstOperatorVBLyt_fileListTable.setAlternatingRowColors(True)
            fileLstOperatorVBLyt_fileListTable.verticalHeader().setDefaultSectionSize(50)
            fileLstOperatorVBLyt_fileListTable.setIconSize(pqc.QSize(48,48))

        fileListTable(currentDir)




        # fileLstOperatorVBLyt_fileListTable.doubleClicked()

        #####End of TabelWidget
        '''

        def selectShowPrpt (self):

            for idx in fileLstOperatorVBLyt_fileListTable.selectionModel().selectedRows():
                rowNum= idx.row()
                nameInfo=fileLstOperatorVBLyt_fileListTable.item(rowNum,0)
                typeInfo=fileLstOperatorVBLyt_fileListTable.item(rowNum,2)
                sizeInfo=fileLstOperatorVBLyt_fileListTable.item(rowNum,3)
                lastUpdtInfo= fileLstOperatorVBLyt_fileListTable.item(rowNum,1)
                tskInfo=fileLstOperatorVBLyt_fileListTable.item(rowNum,4)
                usrInfo=fileLstOperatorVBLyt_fileListTable.item(rowNum,5)


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
            for idx in fileLstOperatorVBLyt_fileListTable.selectionModel().selectedRows():
                rowNum = idx.row()
                nameInfo = fileLstOperatorVBLyt_fileListTable.item(rowNum, 0)
                if os.path.isdir(currentDir+nameInfo.text())==0:
                    os.startfile(currentDir+nameInfo.text())#Windows
                    #subprocess.call(["xdg-open", file])#linux
                    #subprocess.call(["open", file])#mac
                else:
                    currentDir=currentDir+nameInfo.text()+'/'
                    fileListTable(currentDir)



        fileLstOperatorVBLyt_fileListTable.itemClicked.connect(selectShowPrpt)
        fileLstOperatorVBLyt_fileListTable.doubleClicked.connect(openFileOfItem)
        #self.connect(fileLstOperatorVBLyt_fileListTable, SIGNAL("itemClicked (QTableWidgetItem*)"), outSelect# )
        #fileLstOperatorVBLyt_fileListTable.cellActivated.connect(openFileOfItem)



if __name__ == '__main__':
    #tvcExplrApp = QApplication(sys.argv)#disable In Maya
    #tvcExplrApp.setFont(QFont('Microsoft YaHei', 10))  # set default font

    tvcExplrWin = tvcExporerMainWin()
    #tvcExplrWin.languageChange()
    tvcExplrWin.setFont(pqg.QFont('Microsoft YaHei', 9))  # set default font

    tvcExplrWin.show()
    #sys.exit(tvcExplrApp.exec_())
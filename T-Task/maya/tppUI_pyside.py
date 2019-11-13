from PySide2 import QtWidgets as pqw

win=pqw.QWidget()
win.setWindowTitle("TPP Win")

mainVBLyt=pqw.QVBoxLayout()

rootFndLnHBLyt=pqw.QHBoxLayout()
lb_lkIn=pqw.QLabel("Look In: ")
ln_lKIn=pqw.QLineEdit()
pb_lkIn=pqw.QPushButton("Browse..")

win.setLayout(mainVBLyt)
mainVBLyt.addLayout(rootFndLnHBLyt)
rootFndLnHBLyt.addWidget(lb_lkIn)
rootFndLnHBLyt.addWidget(ln_lKIn)
rootFndLnHBLyt.addWidget(pb_lkIn)

lsBxAreaHBLyt=pqw.QHBoxLayout()
mainVBLyt.addLayout(lsBxAreaHBLyt)
outlineVHBLyt=pqw.QVBoxLayout()
lsBxAreaHBLyt.addLayout(outlineVHBLyt)

prjLsHeadHBLyt=pqw.QHBoxLayout()
outlineVHBLyt.addLayout(prjLsHeadHBLyt)

lb_prj=pqw.QLabel("Projects: ")
ln_prjSrchLn=pqw.QLineEdit()
pb_prjSrchPb=pqw.QPushButton("Search")
lw_prjLst=pqw.QListWidget()
lb_fav=pqw.QLabel("Collections: ")
lw_favLst=pqw.QListWidget()

prjLsHeadHBLyt.addWidget(lb_prj)
prjLsHeadHBLyt.addWidget(ln_prjSrchLn)
prjLsHeadHBLyt.addWidget(pb_prjSrchPb)
outlineVHBLyt.addWidget(lw_prjLst)
outlineVHBLyt.addWidget(lb_fav)
outlineVHBLyt.addWidget(lw_favLst)


win.show()
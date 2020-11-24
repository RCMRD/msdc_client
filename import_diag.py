# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_diag.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_importDiag(object):
    def setupUi(self, importDiag):
        importDiag.setObjectName("importDiag")
        importDiag.resize(643, 403)
        self.layoutWidget = QtWidgets.QWidget(importDiag)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 151, 22))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.recordsFound = QtWidgets.QLabel(self.layoutWidget)
        self.recordsFound.setFrameShape(QtWidgets.QFrame.Box)
        self.recordsFound.setText("")
        self.recordsFound.setObjectName("recordsFound")
        self.horizontalLayout_2.addWidget(self.recordsFound)
        self.layoutWidget1 = QtWidgets.QWidget(importDiag)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 100, 611, 241))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.importList = QtWidgets.QListWidget(self.layoutWidget1)
        self.importList.setObjectName("importList")
        self.verticalLayout.addWidget(self.importList)
        self.layoutWidget2 = QtWidgets.QWidget(importDiag)
        self.layoutWidget2.setGeometry(QtCore.QRect(400, 360, 231, 31))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.importBtn2 = QtWidgets.QPushButton(self.layoutWidget2)
        self.importBtn2.setObjectName("importBtn2")
        self.horizontalLayout_3.addWidget(self.importBtn2)
        self.closeBtn2 = QtWidgets.QPushButton(self.layoutWidget2)
        self.closeBtn2.setObjectName("closeBtn2")
        self.horizontalLayout_3.addWidget(self.closeBtn2)
        self.browseBtn1 = QtWidgets.QPushButton(importDiag)
        self.browseBtn1.setGeometry(QtCore.QRect(20, 10, 611, 31))
        self.browseBtn1.setObjectName("browseBtn1")
        self.layoutWidget3 = QtWidgets.QWidget(importDiag)
        self.layoutWidget3.setGeometry(QtCore.QRect(200, 60, 231, 25))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.removeBtn = QtWidgets.QPushButton(self.layoutWidget3)
        self.removeBtn.setObjectName("removeBtn")
        self.horizontalLayout.addWidget(self.removeBtn)
        self.clearBtn = QtWidgets.QPushButton(self.layoutWidget3)
        self.clearBtn.setObjectName("clearBtn")
        self.horizontalLayout.addWidget(self.clearBtn)

        self.retranslateUi(importDiag)
        QtCore.QMetaObject.connectSlotsByName(importDiag)

    def retranslateUi(self, importDiag):
        _translate = QtCore.QCoreApplication.translate
        importDiag.setWindowTitle(_translate("importDiag", "Import Tablet Data "))
        self.label_2.setText(_translate("importDiag", "Records Found"))
        self.importBtn2.setText(_translate("importDiag", "Import"))
        self.closeBtn2.setText(_translate("importDiag", "Cancel"))
        self.browseBtn1.setText(_translate("importDiag", "Select Files to Import"))
        self.removeBtn.setText(_translate("importDiag", "Remove Selected"))
        self.clearBtn.setText(_translate("importDiag", "Clear"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exportdata_diag.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_exportdataDiag(object):
    def setupUi(self, exportdataDiag):
        exportdataDiag.setObjectName("exportdataDiag")
        exportdataDiag.resize(627, 382)
        self.layoutWidget = QtWidgets.QWidget(exportdataDiag)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 601, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.destination = QtWidgets.QLineEdit(self.layoutWidget)
        self.destination.setObjectName("destination")
        self.horizontalLayout.addWidget(self.destination)
        self.browseExports = QtWidgets.QPushButton(self.layoutWidget)
        self.browseExports.setObjectName("browseExports")
        self.horizontalLayout.addWidget(self.browseExports)
        self.layoutWidget1 = QtWidgets.QWidget(exportdataDiag)
        self.layoutWidget1.setGeometry(QtCore.QRect(250, 340, 361, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.exportBtn = QtWidgets.QPushButton(self.layoutWidget1)
        self.exportBtn.setObjectName("exportBtn")
        self.horizontalLayout_2.addWidget(self.exportBtn)
        self.clearExports = QtWidgets.QPushButton(self.layoutWidget1)
        self.clearExports.setObjectName("clearExports")
        self.horizontalLayout_2.addWidget(self.clearExports)
        self.cancelBtn = QtWidgets.QPushButton(self.layoutWidget1)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_2.addWidget(self.cancelBtn)
        self.layoutWidget2 = QtWidgets.QWidget(exportdataDiag)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 60, 601, 221))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.exportList = QtWidgets.QListWidget(self.layoutWidget2)
        self.exportList.setObjectName("exportList")
        self.verticalLayout.addWidget(self.exportList)
        self.layoutWidget3 = QtWidgets.QWidget(exportdataDiag)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 290, 201, 22))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.recordSelected = QtWidgets.QLabel(self.layoutWidget3)
        self.recordSelected.setFrameShape(QtWidgets.QFrame.Box)
        self.recordSelected.setObjectName("recordSelected")
        self.horizontalLayout_3.addWidget(self.recordSelected)

        self.retranslateUi(exportdataDiag)
        QtCore.QMetaObject.connectSlotsByName(exportdataDiag)

    def retranslateUi(self, exportdataDiag):
        _translate = QtCore.QCoreApplication.translate
        exportdataDiag.setWindowTitle(_translate("exportdataDiag", "Export Data to Tablet"))
        self.label.setText(_translate("exportdataDiag", "Destination"))
        self.browseExports.setText(_translate("exportdataDiag", "Browse"))
        self.exportBtn.setText(_translate("exportdataDiag", "Export"))
        self.clearExports.setText(_translate("exportdataDiag", "Clear"))
        self.cancelBtn.setText(_translate("exportdataDiag", "Close"))
        self.label_2.setText(_translate("exportdataDiag", "Records Exported"))
        self.recordSelected.setText(_translate("exportdataDiag", "0"))

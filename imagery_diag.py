# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagery_diag.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_imageryDiag(object):
    def setupUi(self, imageryDiag):
        imageryDiag.setObjectName("imageryDiag")
        imageryDiag.resize(474, 438)
        self.layoutWidget = QtWidgets.QWidget(imageryDiag)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 451, 54))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(imageryDiag)
        self.layoutWidget1.setGeometry(QtCore.QRect(220, 390, 241, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.layoutWidget2 = QtWidgets.QWidget(imageryDiag)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 100, 451, 271))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.layoutWidget2)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(imageryDiag)
        QtCore.QMetaObject.connectSlotsByName(imageryDiag)

    def retranslateUi(self, imageryDiag):
        _translate = QtCore.QCoreApplication.translate
        imageryDiag.setWindowTitle(_translate("imageryDiag", "Export Imagery to Tablet"))
        self.label.setText(_translate("imageryDiag", "Source "))
        self.pushButton.setText(_translate("imageryDiag", "Browse"))
        self.label_2.setText(_translate("imageryDiag", "Destination"))
        self.pushButton_2.setText(_translate("imageryDiag", "Browse"))
        self.pushButton_3.setText(_translate("imageryDiag", "Export"))
        self.pushButton_4.setText(_translate("imageryDiag", "Close"))

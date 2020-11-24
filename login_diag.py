# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_diag.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(321, 301)
        self.layoutWidget = QtWidgets.QWidget(LoginDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(138, 260, 181, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loginBtn2 = QtWidgets.QPushButton(self.layoutWidget)
        self.loginBtn2.setObjectName("loginBtn2")
        self.horizontalLayout.addWidget(self.loginBtn2)
        self.exitBtn2 = QtWidgets.QPushButton(self.layoutWidget)
        self.exitBtn2.setObjectName("exitBtn2")
        self.horizontalLayout.addWidget(self.exitBtn2)
        self.layoutWidget1 = QtWidgets.QWidget(LoginDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 22, 281, 231))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtUsername = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtUsername.setObjectName("txtUsername")
        self.gridLayout.addWidget(self.txtUsername, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txtPassword = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtPassword.setObjectName("txtPassword")
        self.gridLayout.addWidget(self.txtPassword, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txtHost = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtHost.setObjectName("txtHost")
        self.gridLayout.addWidget(self.txtHost, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.txtPort = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtPort.setObjectName("txtPort")
        self.gridLayout.addWidget(self.txtPort, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.txtDb = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtDb.setObjectName("txtDb")
        self.gridLayout.addWidget(self.txtDb, 4, 1, 1, 1)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "MSDC Database Settings"))
        self.loginBtn2.setText(_translate("LoginDialog", "Test Connection"))
        self.exitBtn2.setText(_translate("LoginDialog", "Cancel"))
        self.label.setText(_translate("LoginDialog", "Username"))
        self.txtUsername.setText(_translate("LoginDialog", "postgres"))
        self.label_2.setText(_translate("LoginDialog", "Password"))
        self.txtPassword.setText(_translate("LoginDialog", "postgres"))
        self.label_3.setText(_translate("LoginDialog", "Host"))
        self.txtHost.setText(_translate("LoginDialog", "localhost"))
        self.label_4.setText(_translate("LoginDialog", "Port"))
        self.txtPort.setText(_translate("LoginDialog", "5432"))
        self.label_5.setText(_translate("LoginDialog", "Database"))
        self.txtDb.setText(_translate("LoginDialog", "msdc"))

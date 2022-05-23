# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 90)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 78))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.status = QtWidgets.QLabel(self.layoutWidget)
        self.status.setObjectName("status")
        self.verticalLayout.addWidget(self.status)
        self.actions = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.actions.setOrientation(QtCore.Qt.Horizontal)
        self.actions.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.actions.setObjectName("actions")
        self.verticalLayout.addWidget(self.actions)

        self.retranslateUi(Dialog)
        self.actions.accepted.connect(Dialog.accept)
        self.actions.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка"))
        self.status.setText(_translate("Dialog", "..."))

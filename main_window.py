# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(449, 344)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.playlist = QtWidgets.QTableWidget(self.centralwidget)
        self.playlist.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.playlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.playlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.playlist.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.playlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.playlist.setRowCount(0)
        self.playlist.setColumnCount(2)
        self.playlist.setObjectName("playlist")
        item = QtWidgets.QTableWidgetItem()
        self.playlist.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.playlist.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.playlist)
        self.lengthBar = QtWidgets.QProgressBar(self.centralwidget)
        self.lengthBar.setProperty("value", 0)
        self.lengthBar.setObjectName("lengthBar")
        self.verticalLayout.addWidget(self.lengthBar)
        self.trackSlider = QtWidgets.QSlider(self.centralwidget)
        self.trackSlider.setOrientation(QtCore.Qt.Horizontal)
        self.trackSlider.setObjectName("trackSlider")
        self.verticalLayout.addWidget(self.trackSlider)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playBtn = QtWidgets.QToolButton(self.centralwidget)
        self.playBtn.setCheckable(True)
        self.playBtn.setChecked(False)
        self.playBtn.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.playBtn.setObjectName("playBtn")
        self.horizontalLayout.addWidget(self.playBtn)
        self.previousBtn = QtWidgets.QToolButton(self.centralwidget)
        self.previousBtn.setCheckable(False)
        self.previousBtn.setObjectName("previousBtn")
        self.horizontalLayout.addWidget(self.previousBtn)
        self.pauseBtn = QtWidgets.QToolButton(self.centralwidget)
        self.pauseBtn.setCheckable(True)
        self.pauseBtn.setObjectName("pauseBtn")
        self.horizontalLayout.addWidget(self.pauseBtn)
        self.nextBtn = QtWidgets.QToolButton(self.centralwidget)
        self.nextBtn.setCheckable(False)
        self.nextBtn.setObjectName("nextBtn")
        self.horizontalLayout.addWidget(self.nextBtn)
        self.stopBtn = QtWidgets.QToolButton(self.centralwidget)
        self.stopBtn.setCheckable(True)
        self.stopBtn.setChecked(True)
        self.stopBtn.setObjectName("stopBtn")
        self.horizontalLayout.addWidget(self.stopBtn)
        self.volumeDial = QtWidgets.QDial(self.centralwidget)
        self.volumeDial.setMinimum(0)
        self.volumeDial.setMaximum(100)
        self.volumeDial.setProperty("value", 100)
        self.volumeDial.setInvertedControls(False)
        self.volumeDial.setObjectName("volumeDial")
        self.horizontalLayout.addWidget(self.volumeDial)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.radioMenu = QtWidgets.QMenu(self.menubar)
        self.radioMenu.setObjectName("radioMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openFile = QtWidgets.QAction(MainWindow)
        self.openFile.setObjectName("openFile")
        self.openUrl = QtWidgets.QAction(MainWindow)
        self.openUrl.setObjectName("openUrl")
        self.openPlaylist = QtWidgets.QAction(MainWindow)
        self.openPlaylist.setObjectName("openPlaylist")
        self.clearPlaylist = QtWidgets.QAction(MainWindow)
        self.clearPlaylist.setObjectName("clearPlaylist")
        self.menu.addAction(self.openFile)
        self.menu.addAction(self.openUrl)
        self.menu_2.addAction(self.openPlaylist)
        self.menu_2.addAction(self.clearPlaylist)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.radioMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Musli Player"))
        item = self.playlist.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Название"))
        item = self.playlist.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Длительность"))
        self.playBtn.setText(_translate("MainWindow", "Играть"))
        self.previousBtn.setText(_translate("MainWindow", "Предыдущий"))
        self.pauseBtn.setText(_translate("MainWindow", "Пауза"))
        self.nextBtn.setText(_translate("MainWindow", "Следующий"))
        self.stopBtn.setText(_translate("MainWindow", "Стоп"))
        self.volumeDial.setToolTip(_translate("MainWindow", "100%"))
        self.menu.setTitle(_translate("MainWindow", "Медиа"))
        self.menu_2.setTitle(_translate("MainWindow", "Плейлист"))
        self.radioMenu.setTitle(_translate("MainWindow", "Радио"))
        self.openFile.setText(_translate("MainWindow", "Открыть файл"))
        self.openUrl.setText(_translate("MainWindow", "Открыть ссылку"))
        self.openPlaylist.setText(_translate("MainWindow", "Открыть"))
        self.clearPlaylist.setText(_translate("MainWindow", "Очистить"))

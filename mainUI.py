# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1116, 836)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnLast = QtWidgets.QPushButton(self.centralwidget)
        self.btnLast.setGeometry(QtCore.QRect(20, 350, 93, 28))
        self.btnLast.setObjectName("btnLast")
        self.btnNext = QtWidgets.QPushButton(self.centralwidget)
        self.btnNext.setGeometry(QtCore.QRect(980, 370, 93, 28))
        self.btnNext.setObjectName("btnNext")
        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(980, 560, 93, 28))
        self.btnSave.setObjectName("btnSave")
        self.btnOpen = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpen.setGeometry(QtCore.QRect(20, 10, 93, 28))
        self.btnOpen.setObjectName("btnOpen")
        self.imageBox = QtWidgets.QLabel(self.centralwidget)
        self.imageBox.setGeometry(QtCore.QRect(150, 20, 768, 768))
        self.imageBox.setObjectName("imageBox")
        self.imageBox_Mouse = imageBox(self.centralwidget)
        self.imageBox_Mouse.setGeometry(QtCore.QRect(150, 20, 768, 768))
        self.imageBox_Mouse.setObjectName("imageBox_Mouse")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(1000, 20, 51, 211))
        self.listWidget.setObjectName("listWidget")
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setGeometry(QtCore.QRect(980, 240, 93, 28))
        self.btnDelete.setObjectName("btnDelete")
        self.imageBox.raise_()
        self.btnLast.raise_()
        self.btnNext.raise_()
        self.btnSave.raise_()
        self.btnOpen.raise_()
        self.imageBox_Mouse.raise_()
        self.listWidget.raise_()
        self.btnDelete.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1116, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnLast.setText(_translate("MainWindow", "Last"))
        self.btnNext.setText(_translate("MainWindow", "Next"))
        self.btnSave.setText(_translate("MainWindow", "Save"))
        self.btnOpen.setText(_translate("MainWindow", "Open"))
        self.imageBox.setText(_translate("MainWindow", "image"))
        self.imageBox_Mouse.setText(_translate("MainWindow", "image"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
from imageBox import imageBox

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\add_folder.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(440, 286)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet("background: #151515;")
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(25, 25, 25, 25)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setStyleSheet("background: #191919;\n"
"border-radius: 11px;\n"
"border: 0;\n"
"\n"
"padding: 5px 3px 5px 3px;\n"
"\n"
"font-family: \'Inter\';\n"
"font-style: normal;\n"
"font-weight: 400;\n"
"font-size: 16px;\n"
"line-height: 19px;\n"
"/* identical to box height, or 121% */\n"
"\n"
"\n"
"color: #FFFFFF;")
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("font-family: \'Inter\';\n"
"font-style: normal;\n"
"font-weight: 700;\n"
"font-size: 24px;\n"
"line-height: 29px;\n"
"color: #FFFFFF;")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Dialog", "Привет"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("Dialog", "Добавить в папку"))

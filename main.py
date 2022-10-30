# -*- coding: utf-8 -*-
import sqlite3
import sys
import src

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel


# Класс на отслеживание кликов на QLabel
class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


class Ui_MainWindow(object):
    """Этот класс используется для настройки интерфейса"""

    def __init__(self):
        self.db = sqlite3.connect('data/tasker_data.db')
        self.cur = self.db.cursor()

    def header_btn_setup(self):
        """Настройка кнопок папок"""
        BTN_HEADER_BASE = 47
        BTN_HEADER_HEIGHT = 37
        BTN_HEADER_SPACING = 10

        _translate = QtCore.QCoreApplication.translate  # Не трогать
        folders = self.cur.execute('''SELECT * FROM folders''').fetchall()

        self.btn_menu_main = QtWidgets.QPushButton(self.buttons)
        self.btn_menu_main.setGeometry(QtCore.QRect(0, 0, 219, 37))
        self.btn_menu_main.setMaximumSize(QtCore.QSize(219, 37))
        self.btn_menu_main.setStyleSheet("background: #1490AA;\n"
                                         "border-radius: 11px;\n"
                                         "font-family: \'Inter\';\n"
                                         "font-style: normal;\n"
                                         "font-weight: 400;\n"
                                         "font-size: 16px;\n"
                                         "line-height: 19px;\n"
                                         "text-align: left;\n"
                                         "color: #FFFFFF;\n"
                                         "padding: 8px 0 8px 15px;")
        self.btn_menu_main.setObjectName("btn_menu_main")

        for index, folder in enumerate(folders):
            button = QtWidgets.QPushButton(self.buttons)
            button.setGeometry(QtCore.QRect(0, BTN_HEADER_BASE + ((BTN_HEADER_HEIGHT + BTN_HEADER_SPACING) * index),
                                            219, 37))
            button.setMaximumSize(QtCore.QSize(219, 37))
            button.setStyleSheet("background: #282828;\n"
                                 "border-radius: 11px;\n"
                                 "font-family: \'Inter\';\n"
                                 "font-style: normal;\n"
                                 "font-weight: 400;\n"
                                 "font-size: 16px;\n"
                                 "line-height: 19px;\n"
                                 "text-align: left;\n"
                                 "color: #FFFFFF;\n"
                                 "padding: 8px 0 8px 15px;")
            button.setObjectName(f"btn_menu{index}")
            button.setText(_translate("MainWindow", folder[1]))

    def main_page_setup(self):
        """Настройка главной вкладки"""

        # - Настройка scrollArea
        self.scrollArea = QtWidgets.QScrollArea(self.main_page)
        self.scrollArea.setGeometry(QtCore.QRect(0, 20, 708, 698))
        self.scrollArea.setMinimumSize(QtCore.QSize(708, 698))
        self.scrollArea.setMaximumSize(QtCore.QSize(708, 698))
        self.scrollArea.setStyleSheet("border: 0;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 708, 698))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        # - Настройка gridLayout
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout.setContentsMargins(25, 25, 25, 25)
        self.gridLayout.setObjectName("gridLayout")

        # - Titles
        # 1
        self.title_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.title_1.setMaximumSize(QtCore.QSize(16777215, 29))
        self.title_1.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.title_1.setObjectName("title_1")
        self.gridLayout.addWidget(self.title_1, 0, 0, 1, 1)
        # 2
        self.title_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.title_2.setMaximumSize(QtCore.QSize(16777215, 29))
        self.title_2.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.title_2.setObjectName("title_2")
        self.gridLayout.addWidget(self.title_2, 0, 1, 1, 1)
        # 3
        self.title_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.title_3.setMaximumSize(QtCore.QSize(16777215, 29))
        self.title_3.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.title_3.setObjectName("title_3")
        self.gridLayout.addWidget(self.title_3, 3, 0, 1, 1)
        # 4
        self.title_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.title_4.setMaximumSize(QtCore.QSize(16777215, 29))
        self.title_4.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.title_4.setObjectName("title_4")
        self.gridLayout.addWidget(self.title_4, 3, 1, 1, 1)
        # 5
        self.title_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.title_5.setMaximumSize(QtCore.QSize(16777215, 29))
        self.title_5.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.title_5.setObjectName("title_5")
        self.gridLayout.addWidget(self.title_5, 5, 0, 1, 1)
        # 6
        self.title_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.title_6.setMaximumSize(QtCore.QSize(16777215, 29))
        self.title_6.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.title_6.setObjectName("title_6")
        self.gridLayout.addWidget(self.title_6, 5, 1, 1, 1)
        # 7
        self.title_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.title_7.setMaximumSize(QtCore.QSize(16777215, 29))
        self.title_7.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.title_7.setObjectName("title_7")
        self.gridLayout.addWidget(self.title_7, 7, 0, 1, 1)

        # - tasks
        # 1
        self.tasks_1 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.tasks_1.setObjectName("tasks_1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tasks_1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.task_1_1 = QtWidgets.QFormLayout()
        self.task_1_1.setContentsMargins(-1, 10, -1, -1)
        self.task_1_1.setObjectName("task_1_1")
        self.task_btn_1_1 = QtWidgets.QToolButton(self.tasks_1)
        self.task_btn_1_1.setMaximumSize(QtCore.QSize(18, 18))
        self.task_btn_1_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.task_btn_1_1.setStyleSheet("border: 1px solid #FFFFFF;\n"
                                        "border-radius: 5px;")
        self.task_btn_1_1.setObjectName("task_btn_1_1")
        self.task_description_1_1 = QtWidgets.QLabel(self.tasks_1)
        self.task_description_1_1.setStyleSheet("font-family: \'Inter\';\n"
                                                "font-style: normal;\n"
                                                "font-weight: 400;\n"
                                                "font-size: 16px;\n"
                                                "line-height: 16px;\n"
                                                "/* identical to box height, or 100% */\n"
                                                "\n"
                                                "letter-spacing: -0.055em;\n"
                                                "\n"
                                                "color: #FFFFFF;")
        self.task_description_1_1.setWordWrap(False)
        self.task_description_1_1.setObjectName("task_description_1_1")
        self.task_1_1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.task_btn_1_1)
        self.task_1_1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.task_description_1_1)
        self.verticalLayout.addLayout(self.task_1_1)
        self.gridLayout.addWidget(self.tasks_1, 1, 0, 1, 1)
        # 2
        self.tasks_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.tasks_2.setTitle("")
        self.tasks_2.setObjectName("tasks_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tasks_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.task_2_1 = QtWidgets.QFormLayout()
        self.task_2_1.setContentsMargins(-1, 10, -1, -1)
        self.task_2_1.setObjectName("task_2_1")
        self.verticalLayout_2.addLayout(self.task_2_1)
        self.gridLayout.addWidget(self.tasks_2, 1, 1, 1, 1)
        # 3
        self.tasks_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.tasks_3.setTitle("")
        self.tasks_3.setObjectName("tasks_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tasks_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.tasks_3)
        self.label.setStyleSheet("font-family: \'Inter\';\n"
                                 "font-style: normal;\n"
                                 "font-weight: 400;\n"
                                 "font-size: 16px;\n"
                                 "line-height: 16px;\n"
                                 "/* identical to box height, or 100% */\n"
                                 "\n"
                                 "letter-spacing: -0.055em;\n"
                                 "\n"
                                 "color: #A3A3A3;")
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.gridLayout.addWidget(self.tasks_3, 4, 0, 1, 1)
        # 4
        self.tasks_4 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.tasks_4.setTitle("")
        self.tasks_4.setObjectName("tasks_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tasks_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tasks_4)
        self.label_2.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 400;\n"
                                   "font-size: 16px;\n"
                                   "line-height: 16px;\n"
                                   "/* identical to box height, or 100% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #A3A3A3;")
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.verticalLayout_5.addLayout(self.formLayout_3)
        self.gridLayout.addWidget(self.tasks_4, 4, 1, 1, 1)
        # 5
        self.tasks_5 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.tasks_5.setTitle("")
        self.tasks_5.setObjectName("tasks_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tasks_5)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_3 = QtWidgets.QLabel(self.tasks_5)
        self.label_3.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 400;\n"
                                   "font-size: 16px;\n"
                                   "line-height: 16px;\n"
                                   "/* identical to box height, or 100% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #A3A3A3;")
        self.label_3.setObjectName("label_3")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.verticalLayout_6.addLayout(self.formLayout_4)
        self.gridLayout.addWidget(self.tasks_5, 6, 0, 1, 1)
        # 6
        self.tasks_6 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.tasks_6.setTitle("")
        self.tasks_6.setObjectName("tasks_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tasks_6)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_4 = QtWidgets.QLabel(self.tasks_6)
        self.label_4.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 400;\n"
                                   "font-size: 16px;\n"
                                   "line-height: 16px;\n"
                                   "/* identical to box height, or 100% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #A3A3A3;")
        self.label_4.setObjectName("label_4")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.verticalLayout_7.addLayout(self.formLayout_5)
        self.gridLayout.addWidget(self.tasks_6, 6, 1, 1, 1)
        # 7
        self.tasks_7 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.tasks_7.setTitle("")
        self.tasks_7.setObjectName("tasks_7")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tasks_7)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_5 = QtWidgets.QLabel(self.tasks_7)
        self.label_5.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 400;\n"
                                   "font-size: 16px;\n"
                                   "line-height: 16px;\n"
                                   "/* identical to box height, or 100% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #A3A3A3;")
        self.label_5.setObjectName("label_5")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.verticalLayout_8.addLayout(self.formLayout_6)
        self.gridLayout.addWidget(self.tasks_7, 8, 0, 1, 1)
        # end Настройка scrollArea

        # Настройка scrollArea2
        self.scrollArea_2 = QtWidgets.QScrollArea(self.main_page)
        self.scrollArea_2.setGeometry(QtCore.QRect(708, 20, 271, 691))
        self.scrollArea_2.setMaximumSize(QtCore.QSize(16777215, 691))
        self.scrollArea_2.setStyleSheet("border: 0;\n"
                                        "background: #151515;")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 271, 691))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_2.setContentsMargins(25, 25, 25, 25)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # - Titles
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 29))
        self.label_9.setStyleSheet("font-family: \'Inter\';\n"
                                   "font-style: normal;\n"
                                   "font-weight: 700;\n"
                                   "font-size: 24px;\n"
                                   "line-height: 29px;\n"
                                   "/* identical to box height, or 121% */\n"
                                   "\n"
                                   "letter-spacing: -0.055em;\n"
                                   "\n"
                                   "color: #FFFFFF;")
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 29))
        self.label_10.setStyleSheet("font-family: \'Inter\';\n"
                                    "font-style: normal;\n"
                                    "font-weight: 700;\n"
                                    "font-size: 24px;\n"
                                    "line-height: 29px;\n"
                                    "/* identical to box height, or 121% */\n"
                                    "\n"
                                    "letter-spacing: -0.055em;\n"
                                    "\n"
                                    "color: #FFFFFF;")
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        # end

        self.groupBox_9 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_9.setTitle("")
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_2.addWidget(self.groupBox_9, 3, 0, 1, 1)

        self.groupBox_8 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_8.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_8.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.task_2_2 = QtWidgets.QFormLayout()
        self.task_2_2.setContentsMargins(-1, 10, -1, -1)
        self.task_2_2.setObjectName("task_2_2")

        self.task_btn_2_2 = QtWidgets.QToolButton(self.groupBox_8)
        self.task_btn_2_2.setMaximumSize(QtCore.QSize(18, 18))
        self.task_btn_2_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.task_btn_2_2.setStyleSheet("background: #1490AA;\n"
                                        "border-radius: 5px;")
        self.task_btn_2_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/src/img/task_done.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.task_btn_2_2.setIcon(icon1)
        self.task_btn_2_2.setObjectName("task_btn_2_2")

        self.task_description_2_2 = QtWidgets.QLabel(self.groupBox_8)
        self.task_description_2_2.setStyleSheet("font-family: \'Inter\';\n"
                                                "font-style: normal;\n"
                                                "font-weight: 400;\n"
                                                "font-size: 16px;\n"
                                                "line-height: 16px;\n"
                                                "/* identical to box height, or 100% */\n"
                                                "\n"
                                                "letter-spacing: -0.055em;\n"
                                                "\n"
                                                "color: #FFFFFF;")
        self.task_description_2_2.setTextFormat(QtCore.Qt.AutoText)
        self.task_description_2_2.setScaledContents(False)
        self.task_description_2_2.setWordWrap(True)
        self.task_description_2_2.setObjectName("task_description_2_2")

        self.task_2_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.task_btn_2_2)
        self.task_2_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.task_description_2_2)

        self.gridLayout_4.addLayout(self.task_2_2, 0, 0, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_2.addWidget(self.groupBox_8, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)

    def setupUi(self, MainWindow):
        """Базовая настройка интерфейса"""

        # Настройка отображения главного экрана
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1246, 698)
        MainWindow.setMinimumSize(QtCore.QSize(1246, 698))
        MainWindow.setMaximumSize(QtCore.QSize(1246, 698))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/src/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background: #191919;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # end Настройка отображения главного экрана

        # Настройка главного меню
        # - Header
        self.header = QtWidgets.QGroupBox(self.centralwidget)
        self.header.setEnabled(True)
        self.header.setGeometry(QtCore.QRect(0, 0, 269, 698))
        self.header.setMinimumSize(QtCore.QSize(269, 0))
        self.header.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.header.setStyleSheet("border: 0;\n"
                                  "background: #151515;")
        self.header.setObjectName("header")
        # - Logo
        self.logo = QtWidgets.QLabel(self.header)
        self.logo.setGeometry(QtCore.QRect(20, 20, 142, 52))
        self.logo.setMaximumSize(QtCore.QSize(142, 52))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/src/img/logo.svg"))
        self.logo.setObjectName("logo")
        # - Add folder btn
        self.btn_add_folder = ClickedLabel(self.header)
        self.btn_add_folder.setGeometry(QtCore.QRect(218, 30, 24, 31))
        self.btn_add_folder.setPixmap(QtGui.QPixmap(":/src/img/add_folder.svg"))
        self.btn_add_folder.setObjectName("btn_add_folder")
        self.btn_add_folder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # - Buttons
        self.buttons = QtWidgets.QGroupBox(self.header)
        self.buttons.setGeometry(QtCore.QRect(23, 93, 219, 583))
        self.buttons.setMaximumSize(QtCore.QSize(219, 583))
        self.buttons.setTitle("")
        self.buttons.setObjectName("buttons")

        self.header_btn_setup()
        # end Настройка главного меню

        # Настройка main
        self.main = QtWidgets.QStackedWidget(self.centralwidget)
        self.main.setGeometry(QtCore.QRect(269, -20, 977, 719))
        self.main.setMinimumSize(QtCore.QSize(977, 719))
        self.main.setMaximumSize(QtCore.QSize(977, 719))
        self.main.setObjectName("main")

        # main_page setup
        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("main_page")
        self.main_page_setup()

        # folder_page setup
        self.folder_page = QtWidgets.QWidget()
        self.folder_page.setObjectName("folder_page")

        self.main.addWidget(self.main_page)
        self.main.addWidget(self.folder_page)
        # end Настройка main

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tasker"))
        self.btn_menu_main.setText(_translate("MainWindow", "Все задачи"))
        # TODO(Переделать)
        self.label_5.setText(_translate("MainWindow", "Задач нет"))
        self.task_description_1_1.setText(_translate("MainWindow", "Простое задание"))
        self.label_3.setText(_translate("MainWindow", "Задач нет"))
        self.label.setText(_translate("MainWindow", "Задач нет"))
        self.label_2.setText(_translate("MainWindow", "Задач нет"))
        self.label_4.setText(_translate("MainWindow", "Задач нет"))
        self.title_6.setText(_translate("MainWindow", "Среда, 28 октября"))
        self.title_1.setText(_translate("MainWindow", "Сегодня"))
        self.title_2.setText(_translate("MainWindow", "Завтра"))
        self.title_3.setText(_translate("MainWindow", "Послезавтра"))
        self.title_4.setText(_translate("MainWindow", "Понедельник, 31 октября"))
        self.title_5.setText(_translate("MainWindow", "Вторник, 27 октября"))
        self.title_7.setText(_translate("MainWindow", "Четверг, 29 октября"))
        self.label_9.setText(_translate("MainWindow", "Просроченные"))
        self.task_description_2_2.setText(_translate("MainWindow", "Простое задание"))
        self.label_10.setText(_translate("MainWindow", "Предстоящие"))


class MainWindow(QMainWindow, Ui_MainWindow):
    """В этом классе находятся функции поведения приложения"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_add_folder.clicked.connect(self.add_folder)

    # ACTIONS
    def add_folder(self):
        print('yes')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

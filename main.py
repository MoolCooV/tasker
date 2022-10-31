# -*- coding: utf-8 -*-
import sqlite3
import sys
import src

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Actions_MainWindow:
    """Класс с методами поведения приложения"""

    def __init__(self):
        self.db = sqlite3.connect('data/tasker_data.db')
        self.cur = self.db.cursor()

        self._translate = QtCore.QCoreApplication.translate  # Не трогать

    def add_folder(self):
        pass

    def folder_click(self, sender_btn, active_button):
        if sender_btn == active_button:
            return 429
        else:
            if sender_btn:
                sender_btn.setStyleSheet("background: #1490AA;\n"
                                         "border-radius: 11px;\n"
                                         "font-family: \'Inter\';\n"
                                         "font-style: normal;\n"
                                         "font-weight: 400;\n"
                                         "font-size: 16px;\n"
                                         "line-height: 19px;\n"
                                         "text-align: left;\n"
                                         "color: #FFFFFF;\n"
                                         "padding: 8px 0 8px 15px;")
                sender_btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            if active_button:
                active_button.setStyleSheet("background: #282828;\n"
                                            "border-radius: 11px;\n"
                                            "font-family: \'Inter\';\n"
                                            "font-style: normal;\n"
                                            "font-weight: 400;\n"
                                            "font-size: 16px;\n"
                                            "line-height: 19px;\n"
                                            "text-align: left;\n"
                                            "color: #FFFFFF;\n"
                                            "padding: 8px 0 8px 15px;")
                active_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            return 200


class Ui_MainWindow(Actions_MainWindow, object):
    """Этот класс используется для настройки интерфейса"""

    class ClickedLabel(QLabel):
        clicked = pyqtSignal()

        def mouseReleaseEvent(self, e):
            super().mouseReleaseEvent(e)
            self.clicked.emit()

    def header_btn_setup(self):
        """Настройка кнопок папок"""
        BTN_HEADER_BASE = 47
        BTN_HEADER_HEIGHT = 37
        BTN_HEADER_SPACING = 10

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
        self.btn_menu_main.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_menu_main.setObjectName("btn_menu_main")
        self.btn_menu_main.folder_id = -1
        self.active_button = self.btn_menu_main
        self.btn_menu_main.clicked.connect(self.main_page_setup)

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
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            button.setObjectName(f"btn-menu_{index}")
            button.setText(self._translate("MainWindow", folder[1]))
            button.folder_id = folder[0]
            button.clicked.connect(self.folder_page_setup)

    def main_page_setup(self):
        self.folder_click(self.btn_menu_main, self.active_button)
        self.active_button = self.btn_menu_main
        self.btn_menu_main.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        self.main.setCurrentIndex(0)

        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("main_page")

        """Настройка главной вкладки"""

        self.main_title = QtWidgets.QLabel(self.main_page)
        self.main_title.setGeometry(QtCore.QRect(25, 45, 927, 29))
        self.main_title.setStyleSheet("font-family: \'Inter\';\n"
                                      "font-style: normal;\n"
                                      "font-weight: 700;\n"
                                      "font-size: 27px;\n"
                                      "line-height: 29px;\n"
                                      "/* identical to box height, or 121% */\n"
                                      "\n"
                                      "letter-spacing: -0.055em;\n"
                                      "\n"
                                      "color: #FFFFFF;")
        self.main_title.setObjectName("main_title")
        self.main_title.setText('Все задачи')

        # - Настройка main_mainArea
        self.main_mainArea = QtWidgets.QScrollArea(self.main_page)
        self.main_mainArea.setGeometry(QtCore.QRect(0, 90, 708, 628))
        self.main_mainArea.setMinimumSize(QtCore.QSize(708, 628))
        self.main_mainArea.setMaximumSize(QtCore.QSize(708, 628))
        self.main_mainArea.setStyleSheet("border: 0;")
        self.main_mainArea.setWidgetResizable(True)
        self.main_mainArea.setObjectName("main_mainArea")
        self.main_mainArea_contents = QtWidgets.QWidget()
        self.main_mainArea_contents.setGeometry(QtCore.QRect(0, 0, 708, 628))
        self.main_mainArea_contents.setObjectName("main_mainArea_contents")

        # - Настройка gridLayout
        self.main_mainArea_grid = QtWidgets.QGridLayout(self.main_mainArea_contents)
        self.main_mainArea_grid.setContentsMargins(25, 0, 25, 25)
        self.main_mainArea_grid.setObjectName("main_mainArea_grid")

        # - Titles
        # 1
        self.main_mainArea_title_1 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_1.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_1.setStyleSheet("font-family: \'Inter\';\n"
                                                 "font-style: normal;\n"
                                                 "font-weight: 700;\n"
                                                 "font-size: 24px;\n"
                                                 "line-height: 29px;\n"
                                                 "/* identical to box height, or 121% */\n"
                                                 "\n"
                                                 "letter-spacing: -0.055em;\n"
                                                 "\n"
                                                 "color: #FFFFFF;")
        self.main_mainArea_title_1.setObjectName("main_mainArea_title_2")
        self.main_mainArea_grid.addWidget(self.main_mainArea_title_1, 0, 0, 1, 1)
        # 2
        self.main_mainArea_title_2 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_2.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_2.setStyleSheet("font-family: \'Inter\';\n"
                                                 "font-style: normal;\n"
                                                 "font-weight: 700;\n"
                                                 "font-size: 24px;\n"
                                                 "line-height: 29px;\n"
                                                 "/* identical to box height, or 121% */\n"
                                                 "\n"
                                                 "letter-spacing: -0.055em;\n"
                                                 "\n"
                                                 "color: #FFFFFF;")
        self.main_mainArea_title_2.setObjectName("main_mainArea_title_2")
        self.main_mainArea_grid.addWidget(self.main_mainArea_title_2, 0, 1, 1, 1)
        # 3
        self.main_mainArea_title_3 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_3.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_3.setStyleSheet("font-family: \'Inter\';\n"
                                                 "font-style: normal;\n"
                                                 "font-weight: 700;\n"
                                                 "font-size: 24px;\n"
                                                 "line-height: 29px;\n"
                                                 "/* identical to box height, or 121% */\n"
                                                 "\n"
                                                 "letter-spacing: -0.055em;\n"
                                                 "\n"
                                                 "color: #FFFFFF;")
        self.main_mainArea_title_3.setObjectName("main_mainArea_title_3")
        self.main_mainArea_grid.addWidget(self.main_mainArea_title_3, 3, 0, 1, 1)
        # 4
        self.main_mainArea_title_4 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_4.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_4.setStyleSheet("font-family: \'Inter\';\n"
                                                 "font-style: normal;\n"
                                                 "font-weight: 700;\n"
                                                 "font-size: 24px;\n"
                                                 "line-height: 29px;\n"
                                                 "/* identical to box height, or 121% */\n"
                                                 "\n"
                                                 "letter-spacing: -0.055em;\n"
                                                 "\n"
                                                 "color: #FFFFFF;")
        self.main_mainArea_title_4.setObjectName("main_mainArea_title_4")
        self.main_mainArea_grid.addWidget(self.main_mainArea_title_4, 3, 1, 1, 1)
        # 5
        self.main_mainArea_title_5 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_5.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_5.setStyleSheet("font-family: \'Inter\';\n"
                                                 "font-style: normal;\n"
                                                 "font-weight: 700;\n"
                                                 "font-size: 24px;\n"
                                                 "line-height: 29px;\n"
                                                 "/* identical to box height, or 121% */\n"
                                                 "\n"
                                                 "letter-spacing: -0.055em;\n"
                                                 "\n"
                                                 "color: #FFFFFF;")
        self.main_mainArea_title_5.setObjectName("title_5")
        self.main_mainArea_grid.addWidget(self.main_mainArea_title_5, 5, 0, 1, 1)
        # 6
        self.main_mainArea_title_6 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_6.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_6.setStyleSheet("font-family: \'Inter\';\n"
                                                 "font-style: normal;\n"
                                                 "font-weight: 700;\n"
                                                 "font-size: 24px;\n"
                                                 "line-height: 29px;\n"
                                                 "/* identical to box height, or 121% */\n"
                                                 "\n"
                                                 "letter-spacing: -0.055em;\n"
                                                 "\n"
                                                 "color: #FFFFFF;")
        self.main_mainArea_title_6.setObjectName("main_mainArea_title_6")
        self.main_mainArea_grid.addWidget(self.main_mainArea_title_6, 5, 1, 1, 1)
        # 7
        self.main_mainArea_title_7 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_7.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_7.setStyleSheet("font-family: \'Inter\';\n"
                                                 "font-style: normal;\n"
                                                 "font-weight: 700;\n"
                                                 "font-size: 24px;\n"
                                                 "line-height: 29px;\n"
                                                 "/* identical to box height, or 121% */\n"
                                                 "\n"
                                                 "letter-spacing: -0.055em;\n"
                                                 "\n"
                                                 "color: #FFFFFF;")
        self.main_mainArea_title_7.setObjectName("main_mainArea_title_7")
        self.main_mainArea_grid.addWidget(self.main_mainArea_title_7, 7, 0, 1, 1)

        # - tasks
        # 1
        self.main_mainArea_tasks_1 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_1.setObjectName("main_mainArea_tasks_1")
        self.main_mainArea_tasks_1_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_1)
        self.main_mainArea_tasks_1_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_1_layout.setObjectName("main_mainArea_tasks_1_layout")

        # - Task
        self.task_1_1 = QtWidgets.QFormLayout()
        self.task_1_1.setContentsMargins(-1, 10, -1, -1)
        self.task_1_1.setObjectName("task_1_1")
        self.task_btn_1_1 = QtWidgets.QToolButton(self.main_mainArea_tasks_1)
        self.task_btn_1_1.setMaximumSize(QtCore.QSize(18, 18))
        self.task_btn_1_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.task_btn_1_1.setStyleSheet("border: 1px solid #FFFFFF;\n"
                                        "border-radius: 5px;")
        self.task_btn_1_1.setObjectName("task_btn_1_1")
        self.task_description_1_1 = QtWidgets.QLabel(self.main_mainArea_tasks_1)
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
        self.main_mainArea_tasks_1_layout.addLayout(self.task_1_1)
        # - end Task

        self.main_mainArea_grid.addWidget(self.main_mainArea_tasks_1, 1, 0, 1, 1)
        # 2
        self.main_mainArea_tasks_2 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_2.setTitle("")
        self.main_mainArea_tasks_2.setObjectName("main_mainArea_tasks_2")
        self.main_mainArea_tasks_2_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_2)
        self.main_mainArea_tasks_2_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_2_layout.setObjectName("main_mainArea_tasks_2_layout")

        # - Task
        self.task_2_1 = QtWidgets.QFormLayout()
        self.task_2_1.setContentsMargins(-1, 10, -1, -1)
        self.task_2_1.setObjectName("task_2_1")
        self.main_mainArea_tasks_2_layout.addLayout(self.task_2_1)
        # - end Task

        self.main_mainArea_grid.addWidget(self.main_mainArea_tasks_2, 1, 1, 1, 1)
        # 3
        self.main_mainArea_tasks_3 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_3.setTitle("")
        self.main_mainArea_tasks_3.setObjectName("main_mainArea_tasks_3")
        self.main_mainArea_tasks_3_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_3)
        self.main_mainArea_tasks_3_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_3_layout.setObjectName("main_mainArea_tasks_3_layout")

        # - Task
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.main_mainArea_tasks_3)
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
        self.main_mainArea_tasks_3_layout.addLayout(self.formLayout_2)
        # - end Task

        self.main_mainArea_grid.addWidget(self.main_mainArea_tasks_3, 4, 0, 1, 1)
        # 4
        self.main_mainArea_tasks_4 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_4.setTitle("")
        self.main_mainArea_tasks_4.setObjectName("main_mainArea_tasks_4")
        self.main_mainArea_tasks_4_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_4)
        self.main_mainArea_tasks_4_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_4_layout.setObjectName("main_mainArea_tasks_4_layout")

        # - Task
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_2 = QtWidgets.QLabel(self.main_mainArea_tasks_4)
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
        self.main_mainArea_tasks_4_layout.addLayout(self.formLayout_3)
        # - end Task

        self.main_mainArea_grid.addWidget(self.main_mainArea_tasks_4, 4, 1, 1, 1)
        # 5
        self.main_mainArea_tasks_5 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_5.setTitle("")
        self.main_mainArea_tasks_5.setObjectName("main_mainArea_tasks_5")
        self.main_mainArea_tasks_5_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_5)
        self.main_mainArea_tasks_5_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_5_layout.setObjectName("main_mainArea_tasks_5_layout")

        # - Task
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_3 = QtWidgets.QLabel(self.main_mainArea_tasks_5)
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
        self.main_mainArea_tasks_5_layout.addLayout(self.formLayout_4)
        # - end Task

        self.main_mainArea_grid.addWidget(self.main_mainArea_tasks_5, 6, 0, 1, 1)
        # 6
        self.main_mainArea_tasks_6 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_6.setTitle("")
        self.main_mainArea_tasks_6.setObjectName("main_mainArea_tasks_6")
        self.main_mainArea_tasks_6_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_6)
        self.main_mainArea_tasks_6_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_6_layout.setObjectName("main_mainArea_tasks_6_layout")

        # - Task
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_4 = QtWidgets.QLabel(self.main_mainArea_tasks_6)
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
        self.main_mainArea_tasks_6_layout.addLayout(self.formLayout_5)
        # - end Task

        self.main_mainArea_grid.addWidget(self.main_mainArea_tasks_6, 6, 1, 1, 1)
        # 7
        self.main_mainArea_tasks_7 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_7.setTitle("")
        self.main_mainArea_tasks_7.setObjectName("main_mainArea_tasks_7")
        self.main_mainArea_tasks_8_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_7)
        self.main_mainArea_tasks_8_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_8_layout.setObjectName("main_mainArea_tasks_8_layout")

        # - Task
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setContentsMargins(-1, 10, -1, -1)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_5 = QtWidgets.QLabel(self.main_mainArea_tasks_7)
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
        self.main_mainArea_tasks_8_layout.addLayout(self.formLayout_6)
        # - end Task

        self.main_mainArea_grid.addWidget(self.main_mainArea_tasks_7, 8, 0, 1, 1)
        # end Настройка main_mainArea

        # Настройка main_secondArea
        self.main_secondArea = QtWidgets.QScrollArea(self.main_page)
        self.main_secondArea.setGeometry(QtCore.QRect(708, 20, 271, 691))
        self.main_secondArea.setMaximumSize(QtCore.QSize(16777215, 691))
        self.main_secondArea.setStyleSheet("border: 0;\n"
                                           "background: #151515;")
        self.main_secondArea.setWidgetResizable(True)
        self.main_secondArea.setObjectName("main_secondArea")
        self.main_secondArea_contents = QtWidgets.QWidget()
        self.main_secondArea_contents.setGeometry(QtCore.QRect(0, 0, 271, 691))
        self.main_secondArea_contents.setObjectName("main_secondArea_contents")

        self.main_secondArea_grid = QtWidgets.QGridLayout(self.main_secondArea_contents)
        self.main_secondArea_grid.setContentsMargins(25, 25, 25, 25)
        self.main_secondArea_grid.setObjectName("main_secondArea_grid")

        # - Titles
        # 1
        self.main_secondArea_title_1 = QtWidgets.QLabel(self.main_secondArea_contents)
        self.main_secondArea_title_1.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_secondArea_title_1.setStyleSheet("font-family: \'Inter\';\n"
                                                   "font-style: normal;\n"
                                                   "font-weight: 700;\n"
                                                   "font-size: 24px;\n"
                                                   "line-height: 29px;\n"
                                                   "/* identical to box height, or 121% */\n"
                                                   "\n"
                                                   "letter-spacing: -0.055em;\n"
                                                   "\n"
                                                   "color: #FFFFFF;")
        self.main_secondArea_title_1.setObjectName("main_secondArea_title_1")
        # 2
        self.main_secondArea_title_2 = QtWidgets.QLabel(self.main_secondArea_contents)
        self.main_secondArea_title_2.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_secondArea_title_2.setStyleSheet("font-family: \'Inter\';\n"
                                                   "font-style: normal;\n"
                                                   "font-weight: 700;\n"
                                                   "font-size: 24px;\n"
                                                   "line-height: 29px;\n"
                                                   "/* identical to box height, or 121% */\n"
                                                   "\n"
                                                   "letter-spacing: -0.055em;\n"
                                                   "\n"
                                                   "color: #FFFFFF;")
        self.main_secondArea_title_2.setObjectName("main_secondArea_title_2")

        self.main_secondArea_grid.addWidget(self.main_secondArea_title_1, 0, 0, 1, 1)
        self.main_secondArea_grid.addWidget(self.main_secondArea_title_2, 2, 0, 1, 1)
        # - end Titles

        # - groups
        self.main_mainArea_tasks_1 = QtWidgets.QGroupBox(self.main_secondArea_contents)
        self.main_mainArea_tasks_1.setTitle("")
        self.main_mainArea_tasks_1.setObjectName("main_secondArea_group_2")
        self.main_secondArea_grid.addWidget(self.main_mainArea_tasks_1, 1, 0, 1, 1)

        self.main_secondArea_group_2 = QtWidgets.QGroupBox(self.main_secondArea_contents)
        self.main_secondArea_group_2.setTitle("")
        self.main_secondArea_group_2.setObjectName("main_mainArea_tasks_1")
        self.main_secondArea_grid.addWidget(self.main_secondArea_group_2, 3, 0, 1, 1)
        # - end groups

        self.main_mainArea_tasks_1_layout = QtWidgets.QGridLayout(self.main_mainArea_tasks_1)
        self.main_mainArea_tasks_1_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_mainArea_tasks_1_layout.setContentsMargins(0, 0, 0, 0)
        self.main_mainArea_tasks_1_layout.setObjectName("main_mainArea_tasks_1_layout")

        # Task
        self.task_2_2 = QtWidgets.QFormLayout()
        self.task_2_2.setContentsMargins(-1, 10, -1, -1)
        self.task_2_2.setObjectName("task_2_2")
        self.task_btn_2_2 = QtWidgets.QToolButton(self.main_mainArea_tasks_1)
        self.task_btn_2_2.setMaximumSize(QtCore.QSize(18, 18))
        self.task_btn_2_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.task_btn_2_2.setStyleSheet("background: #1490AA;\n"
                                        "border-radius: 5px;")
        self.task_btn_2_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/src/img/task_done.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.task_btn_2_2.setIcon(icon1)
        self.task_btn_2_2.setObjectName("task_btn_2_2")
        self.task_description_2_2 = QtWidgets.QLabel(self.main_mainArea_tasks_1)
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
        self.main_mainArea_tasks_1_layout.addLayout(self.task_2_2, 0, 0, 1, 1)
        self.main_mainArea_tasks_1_layout.setColumnStretch(0, 1)
        # end task
        # end Настройка main_secondArea

        self.main_mainArea.setWidget(self.main_mainArea_contents)
        self.main_secondArea.setWidget(self.main_secondArea_contents)

        self.main.addWidget(self.main_page)

    def folder_page_setup(self):
        self.folder_page = QtWidgets.QWidget()

        if self.sender():
            answer = self.folder_click(self.sender(), self.active_button)
            self.active_button = self.sender()

            folder = self.cur.execute(f'''SELECT folder_title FROM folders WHERE folder_id = ?''',
                                      [self.active_button.folder_id]).fetchone()

            tasks = self.cur.execute('''SELECT * FROM tasks WHERE folder_id = ?''',
                                     [self.active_button.folder_id]).fetchall()

            print(folder[0] if folder else '')

            self.main.setCurrentIndex(1)

            self.folder_title.setText(folder[0])
        else:
            self.folder_title = QtWidgets.QLabel(self.folder_page)
            self.folder_title.setGeometry(QtCore.QRect(25, 45, 927, 29))
            self.folder_title.setStyleSheet("font-family: \'Inter\';\n"
                                            "font-style: normal;\n"
                                            "font-weight: 700;\n"
                                            "font-size: 27px;\n"
                                            "line-height: 29px;\n"
                                            "/* identical to box height, or 121% */\n"
                                            "\n"
                                            "letter-spacing: -0.055em;\n"
                                            "\n"
                                            "color: #FFFFFF;")
            self.folder_title.setObjectName("folder_title")

            self.folder_area = QtWidgets.QScrollArea(self.folder_page)
            self.folder_area.setGeometry(QtCore.QRect(0, 90, 977, 628))
            self.folder_area.setMinimumSize(QtCore.QSize(977, 628))
            self.folder_area.setMaximumSize(QtCore.QSize(977, 628))
            self.folder_area.setStyleSheet("border: 0;")
            self.folder_area.setWidgetResizable(True)
            self.folder_area.setObjectName("folder_area")

            self.folder_area_contents = QtWidgets.QWidget()
            self.folder_area_contents.setGeometry(QtCore.QRect(0, 0, 977, 628))
            self.folder_area_contents.setObjectName("folder_area_contents")

            self.folder_area_layout = QtWidgets.QVBoxLayout(self.folder_area_contents)
            self.folder_area_layout.setContentsMargins(25, 0, 25, 25)
            self.folder_area_layout.setObjectName("folder_area_layout")

            # Task
            self.task_1_2 = QtWidgets.QFormLayout()
            self.task_1_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
            self.task_1_2.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
            self.task_1_2.setContentsMargins(-1, 10, -1, -1)
            self.task_1_2.setObjectName("task_1_2")
            self.task_btn_1_2 = QtWidgets.QToolButton(self.folder_area_contents)
            self.task_btn_1_2.setMaximumSize(QtCore.QSize(18, 18))
            self.task_btn_1_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.task_btn_1_2.setStyleSheet("border: 1px solid #FFFFFF;\n"
                                            "border-radius: 5px;")
            self.task_btn_1_2.setText("")
            self.task_btn_1_2.setObjectName("task_btn_1_2")
            self.task_1_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.task_btn_1_2)
            self.task_description_1_2 = QtWidgets.QLabel(self.folder_area_contents)
            self.task_description_1_2.setStyleSheet("font-family: \'Inter\';\n"
                                                    "font-style: normal;\n"
                                                    "font-weight: 400;\n"
                                                    "font-size: 16px;\n"
                                                    "line-height: 16px;\n"
                                                    "/* identical to box height, or 100% */\n"
                                                    "\n"
                                                    "letter-spacing: -0.055em;\n"
                                                    "\n"
                                                    "color: #FFFFFF;")
            self.task_description_1_2.setWordWrap(False)
            self.task_description_1_2.setObjectName("task_description_1_2")
            self.task_1_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.task_description_1_2)
            self.folder_area_layout.addLayout(self.task_1_2)
            # end Task

            self.folder_area.setWidget(self.folder_area_contents)
            self.folder_page.setObjectName("folder_page")

            self.main.addWidget(self.folder_page)

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
        self.btn_add_folder = self.ClickedLabel(self.header)
        self.btn_add_folder.setGeometry(QtCore.QRect(218, 30, 24, 31))
        self.btn_add_folder.setPixmap(QtGui.QPixmap(":/src/img/add_folder.svg"))
        self.btn_add_folder.setObjectName("btn_add_folder")
        self.btn_add_folder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_folder.clicked.connect(self.add_folder)
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

        self.main_page_setup()
        self.folder_page_setup()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(self._translate("MainWindow", "Tasker"))
        self.btn_menu_main.setText(self._translate("MainWindow", "Все задачи"))
        # Titles
        self.main_mainArea_title_1.setText(self._translate("MainWindow", "Сегодня"))
        self.main_mainArea_title_2.setText(self._translate("MainWindow", "Завтра"))
        self.main_mainArea_title_3.setText(self._translate("MainWindow", "Послезавтра"))
        self.main_mainArea_title_4.setText(self._translate("MainWindow", "Понедельник, 31 октября"))
        self.main_mainArea_title_5.setText(self._translate("MainWindow", "Вторник, 27 октября"))
        self.main_mainArea_title_6.setText(self._translate("MainWindow", "Среда, 28 октября"))
        self.main_mainArea_title_7.setText(self._translate("MainWindow", "Четверг, 29 октября"))
        self.main_secondArea_title_1.setText(self._translate("MainWindow", "Просроченные"))
        self.main_secondArea_title_2.setText(self._translate("MainWindow", "Предстоящие"))
        # end Titles
        # TODO(Переделать)
        self.label_5.setText(self._translate("MainWindow", "Задач нет"))
        self.task_description_1_1.setText(self._translate("MainWindow", "Простое задание"))
        self.label_3.setText(self._translate("MainWindow", "Задач нет"))
        self.label.setText(self._translate("MainWindow", "Задач нет"))
        self.label_2.setText(self._translate("MainWindow", "Задач нет"))
        self.label_4.setText(self._translate("MainWindow", "Задач нет"))
        self.task_description_2_2.setText(self._translate("MainWindow", "Простое задание"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
import sqlite3
import sys
import datetime
import src

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Actions:
    """Класс с методами поведения приложения"""

    def __init__(self):
        self.db = sqlite3.connect('data/tasker_data.db')
        self.cur = self.db.cursor()

        self._translate = QtCore.QCoreApplication.translate
        self.tasks = []

    def add_folder(self, folder_name="Привет"):
        self.cur.execute(f'''INSERT INTO folders (folder_title) VALUES (?)''', (folder_name,))
        self.db.commit()

    def add_task(self):
        pass

    def reload_tasks(self):
        for task in self.tasks:
            task.deleteLater()
        self.tasks.clear()

    def folder_click(self, sender_btn, active_button):
        if sender_btn == active_button:
            pass
        else:
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


class Ui_MainWindow(Actions, object):
    """Этот класс используется для настройки интерфейса"""

    class ClickedLabel(QLabel):
        clicked = pyqtSignal()

        def mouseReleaseEvent(self, e):
            super().mouseReleaseEvent(e)
            self.clicked.emit()

    # Setups
    def header_btn_setup(self):
        """Настройка кнопок папок"""
        BTN_HEADER_BASE = 47
        BTN_HEADER_HEIGHT = 37
        BTN_HEADER_SPACING = 10

        folders = self.cur.execute('''SELECT * FROM folders''').fetchall()

        self.btn_menu_main = QtWidgets.QPushButton(self.buttons)
        self.btn_menu_main.setGeometry(QtCore.QRect(0, 0, 219, 37))
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
        self.btn_menu_main.clicked.connect(self.main_page_tasks)

        for index, folder in enumerate(folders):
            button = QtWidgets.QPushButton(self.buttons)
            button.setGeometry(QtCore.QRect(0, BTN_HEADER_BASE + ((BTN_HEADER_HEIGHT + BTN_HEADER_SPACING) * index),
                                            219, 37))
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
            button.clicked.connect(self.folder_page_tasks)

    def main_page_setup(self):
        """Настройка главной вкладки"""



        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("main_page")

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

        # - Настройка main_mainArea
        self.main_mainArea = QtWidgets.QScrollArea(self.main_page)
        self.main_mainArea.setGeometry(QtCore.QRect(0, 90, 708, 628))
        self.main_mainArea.setStyleSheet("border: 0;")
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
        self.main_mainArea_tasks_1.setObjectName("main_secondArea_group_2")
        self.main_secondArea_grid.addWidget(self.main_mainArea_tasks_1, 1, 0, 1, 1)

        self.main_secondArea_group_2 = QtWidgets.QGroupBox(self.main_secondArea_contents)
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
        self.folder_page.setObjectName("folder_page")

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
        self.folder_area.setMaximumSize(QtCore.QSize(16777215, 977))
        self.folder_area.setWidgetResizable(True)
        self.folder_area.setStyleSheet("border: 0;")
        self.folder_area.setObjectName("folder_area")

        self.folder_area_contents = QtWidgets.QWidget()
        self.folder_area_contents.setGeometry(QtCore.QRect(0, 0, 977, 628))
        self.folder_area_contents.setObjectName("folder_area_contents")

        self.folder_area_layout = QtWidgets.QVBoxLayout(self.folder_area_contents)
        self.folder_area_layout.setContentsMargins(25, 0, 25, 25)
        self.folder_area_layout.setSpacing(12)
        self.folder_area_layout.setObjectName("folder_area_layout")

        self.folder_area.setWidget(self.folder_area_contents)

        self.main.addWidget(self.folder_page)

    # Tasks loading
    def main_page_tasks(self):
        self.folder_click(self.btn_menu_main, self.active_button)
        self.active_button.setEnabled(True)
        self.active_button = self.btn_menu_main
        self.active_button.setEnabled(False)
        self.btn_menu_main.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        tasks = self.cur.execute('''SELECT * FROM tasks''')

        self.main.setCurrentIndex(0)

    def folder_page_tasks(self):
        self.reload_tasks()

        self.folder_click(self.sender(), self.active_button)
        self.sender().setEnabled(False)
        self.active_button.setEnabled(True)
        self.active_button = self.sender()

        folder = self.cur.execute(f'''SELECT folder_title FROM folders WHERE folder_id = ?''',
                                  [self.active_button.folder_id]).fetchone()
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE folder_id = ?''',
                                 [self.active_button.folder_id]).fetchall()

        self.folder_title.setText(folder[0])

        if tasks:
            for index, task in enumerate(tasks):
                self.task = QtWidgets.QGroupBox(self.folder_area_contents)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHeightForWidth(self.task.sizePolicy().hasHeightForWidth())
                self.task.setSizePolicy(sizePolicy)
                self.task.setObjectName(f"task_{index}")

                self.task_layout = QtWidgets.QFormLayout(self.task)
                self.task_layout.setContentsMargins(0, 0, 0, 0)
                self.task_layout.setObjectName(f"task_layout_{index}")

                self.task_btn = QtWidgets.QToolButton(self.task)
                self.task_btn.setMaximumSize(QtCore.QSize(18, 18))
                self.task_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.task_btn.setStyleSheet("border: 1.25px solid #FFFFFF;\n"
                                            "border-radius: 5px;")
                self.task_btn.setObjectName(f"task_btn_{index}")

                self.task_description = QtWidgets.QLabel(self.task)
                self.task_description.setStyleSheet("font-family: \'Inter\';\n"
                                                    "font-style: normal;\n"
                                                    "font-weight: 400;\n"
                                                    "font-size: 16px;\n"
                                                    "line-height: 16px;\n"
                                                    "/* identical to box height, or 100% */\n"
                                                    "\n"
                                                    "letter-spacing: -0.055em;\n"
                                                    "\n"
                                                    "color: #FFFFFF;")
                self.task_description.setWordWrap(False)
                self.task_description.setObjectName(f"task_description_{index}")
                self.task_description.setText(self._translate("MainWindow", task[3]))

                self.task_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.task_btn)
                self.task_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.task_description)

                self.folder_area_layout.addWidget(self.task)

                self.tasks.append(self.task)

            self.folder_space = QtWidgets.QLabel()
            self.folder_space.setObjectName("folder_space")
            self.tasks.append(self.folder_space)

            self.folder_area_layout.addWidget(self.folder_space)
        else:
            self.folder_no_tasks = QtWidgets.QGroupBox(self.folder_area_contents)
            self.folder_no_tasks.setObjectName("folder_no_tasks")

            self.folder_no_tasks_layout = QtWidgets.QFormLayout(self.folder_no_tasks)
            self.folder_no_tasks_layout.setContentsMargins(0, 0, 0, 0)
            self.folder_no_tasks_layout.setObjectName("folder_no_tasks_layout")

            self.folder_no_tasks_description = QtWidgets.QLabel(self.folder_area_contents)
            self.folder_no_tasks_description.setStyleSheet("font-family: \'Inter\';\n"
                                                           "font-style: normal;\n"
                                                           "font-weight: 400;\n"
                                                           "font-size: 16px;\n"
                                                           "line-height: 16px;\n"
                                                           "/* identical to box height, or 100% */\n"
                                                           "\n"
                                                           "letter-spacing: -0.055em;\n"
                                                           "\n"
                                                           "color: #A3A3A3;")
            self.folder_no_tasks_description.setObjectName("folder_no_tasks_description")
            self.folder_no_tasks_description.setText(self._translate("MainWindow", "Задач нет"))

            self.folder_no_tasks_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                                  self.folder_no_tasks_description)

            self.folder_no_tasks.setLayout(self.folder_no_tasks_layout)
            self.folder_area_layout.addWidget(self.folder_no_tasks)

            self.tasks.append(self.folder_no_tasks)

        self.main.setCurrentIndex(1)

    # Main setup
    def setupUi(self, MainWindow):
        """Базовая настройка интерфейса"""

        # Настройка отображения главного экрана
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(QtCore.QSize(1246, 698))
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
        self.header.setStyleSheet("border: 0;\n"
                                  "background: #151515;")
        self.header.setObjectName("header")
        # - Logo
        self.logo = QtWidgets.QLabel(self.header)
        self.logo.setGeometry(QtCore.QRect(20, 20, 142, 52))
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
        self.buttons.setObjectName("buttons")

        self.header_btn_setup()
        # end Настройка главного меню

        # Настройка main
        self.main = QtWidgets.QStackedWidget(self.centralwidget)
        self.main.setGeometry(QtCore.QRect(269, -20, 977, 719))
        self.main.setObjectName("main")

        self.main_page_setup()
        self.folder_page_setup()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(self._translate("MainWindow", "Tasker"))
        self.main_title.setText(self._translate("MainWindow", "Все задачи"))
        self.btn_menu_main.setText(self._translate("MainWindow", "Все задачи"))
        self.main_mainArea_title_1.setText(self._translate("MainWindow", "Сегодня"))
        self.main_mainArea_title_2.setText(self._translate("MainWindow", "Завтра"))
        self.main_mainArea_title_3.setText(self._translate("MainWindow", "Послезавтра"))
        self.main_mainArea_title_4.setText(self._translate("MainWindow", "Понедельник, 31 октября"))
        self.main_mainArea_title_5.setText(self._translate("MainWindow", "Вторник, 27 октября"))
        self.main_mainArea_title_6.setText(self._translate("MainWindow", "Среда, 28 октября"))
        self.main_mainArea_title_7.setText(self._translate("MainWindow", "Четверг, 29 октября"))
        self.main_secondArea_title_1.setText(self._translate("MainWindow", "Просроченные"))
        self.main_secondArea_title_2.setText(self._translate("MainWindow", "Предстоящие"))
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

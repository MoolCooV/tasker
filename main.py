#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sys
import locale
import datetime as dt
import src

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

STYLES = {
    'title': ("font-family: \'Inter\';\n"
              "font-style: normal;\n"
              "font-weight: 700;\n"
              "font-size: 27px;\n"
              "line-height: 29px;\n"
              "letter-spacing: -0.055em;\n"
              "color: #FFFFFF;"),
    'subtitle': ("font-family: \'Inter\';\n"
                 "font-style: normal;\n"
                 "font-weight: 700;\n"
                 "font-size: 24px;\n"
                 "line-height: 29px;\n"
                 "letter-spacing: -0.055em;\n"
                 "color: #FFFFFF;"),
    'btn_active': ("background: #1490AA;\n"
                   "border-radius: 11px;\n"
                   "font-family: \'Inter\';\n"
                   "font-style: normal;\n"
                   "font-weight: 400;\n"
                   "font-size: 16px;\n"
                   "line-height: 19px;\n"
                   "text-align: left;\n"
                   "color: #FFFFFF;\n"
                   "padding: 8px 0 8px 15px;"),
    'btn_inactive': ("background: #282828;\n"
                     "border-radius: 11px;\n"
                     "font-family: \'Inter\';\n"
                     "font-style: normal;\n"
                     "font-weight: 400;\n"
                     "font-size: 16px;\n"
                     "line-height: 19px;\n"
                     "text-align: left;\n"
                     "color: #FFFFFF;\n"
                     "padding: 8px 0 8px 15px;"),
    'btn_action': ("background: #282828;\n"
                   "border-radius: 11px;\n"
                   "font-family: \'Inter\';\n"
                   "font-style: normal;\n"
                   "font-weight: 400;\n"
                   "font-size: 16px;\n"
                   "line-height: 19px;\n"
                   "text-align: center;\n"
                   "color: #FFFFFF;\n"
                   "padding: 8px 0 8px 0;"),
    'btn_action_active': ("background: #1490AA;\n"
                          "border-radius: 11px;\n"
                          "font-family: \'Inter\';\n"
                          "font-style: normal;\n"
                          "font-weight: 400;\n"
                          "font-size: 16px;\n"
                          "line-height: 19px;\n"
                          "text-align: center;\n"
                          "color: #FFFFFF;\n"
                          "padding: 8px 0 8px 0;"),
    'task_btn_active': ("background: #1490AA;\n"
                        "border-radius: 5px;"),
    'task_btn_inactive': ("border: 1.25px solid #FFFFFF;\n"
                          "border-radius: 5px;\n"),
    'task_description': ("font-family: \'Inter\';\n"
                         "font-style: normal;\n"
                         "font-weight: 400;\n"
                         "font-size: 16px;\n"
                         "line-height: 16px;\n"
                         "letter-spacing: -0.055em;\n"
                         "color: #FFFFFF;"),
    'no_tasks': ("font-family: \'Inter\';\n"
                 "font-style: normal;\n"
                 "font-weight: 400;\n"
                 "font-size: 16px;\n"
                 "line-height: 16px;\n"
                 "letter-spacing: -0.055em;\n"
                 "color: #A3A3A3;"),
    'dialog_label': ("font-family: \'Inter\';\n"
                     "font-style: normal;\n"
                     "font-weight: 400;\n"
                     "font-size: 16px;\n"
                     "line-height: 19px;\n"
                     "color: #FFFFFF;"),
    'dialog_error': ('''
font-family: 'Inter';
font-style: normal;
font-weight: 300;
font-size: 13px;
line-height: 16px;
text-align: center;
color: #FF4E4E;
'''),
    'dialog_input': ("background: #282828;\n"
                     "border-radius: 11px;\n"
                     "font-family: \'Inter\';\n"
                     "font-style: normal;\n"
                     "font-weight: 300;\n"
                     "font-size: 15px;\n"
                     "line-height: 19px;\n"
                     "padding: 4px 10px;\n"
                     "color: #FFFFFF;"),
    'dialog_input_error': ("background: #282828;\n"
                           "border-radius: 11px;\n"
                           "border: 1px solid #FF4E4E;\n"
                           "font-family: \'Inter\';\n"
                           "font-style: normal;\n"
                           "font-weight: 300;\n"
                           "font-size: 15px;\n"
                           "line-height: 19px;\n"
                           "padding: 4px 10px;\n"
                           "color: #FFFFFF;"),
    'dialog_date': ("""QDateEdit { background: #282828; border-radius: 11px; padding-left: 5px; font-family: 'Inter'; 
    font-style: normal; font-weight: 300; font-size: 15px; line-height: 19px; text-align: center; color: #FFFFFF; } 
    QDateEdit:disabled { background: #282828; border-radius: 11px; font-family: 'Inter'; font-style: normal; 
    font-weight: 300; font-size: 15px; line-height: 19px; text-align: center; color: #A3A3A3; } QDateEdit::up-button 
    { width: 16px; height: 13px; border-radius: 0px 11px 0px 0px; } QDateEdit::up-button:pressed { background: 
    #191919; } QDateEdit::up-arrow { image: url(./src/img/dateEdit/arrow1.png); } QDateEdit::down-button { width: 
    16px; height: 13px; border-radius: 0px 0px 0px 11px; } QDateEdit::down-button:pressed { background: #191919; } 
    QDateEdit::down-arrow { image: url(./src/img/dateEdit/arrow2.png) }"""),
    'dialog_btnConfirm': ("font-family: 'Inter';\n"
                          "font-style: normal;\n"
                          "font-weight: 400;\n"
                          "font-size: 16px;\n"
                          "line-height: 19px;\n"
                          "text-align: center;\n"
                          "color: #FFFFFF;\n"
                          "background: #1490AA;\n"
                          "border-radius: 11px;"),
    'dialog_btnCancel': ("font-family: 'Inter';\n"
                         "font-style: normal;\n"
                         "font-weight: 400;\n"
                         "font-size: 16px;\n"
                         "line-height: 19px;\n"
                         "text-align: center;\n"
                         "color: #FFFFFF;\n"
                         "background: #282828;\n"
                         "border-radius: 11px;\n"),
    'dialog_folderList': ("background: #191919;\n"
                          "border-radius: 11px;\n"
                          "border: 0;\n"
                          "padding: 5px 3px 5px 3px;\n"
                          "font-family: \'Inter\';\n"
                          "font-style: normal;\n"
                          "font-weight: 400;\n"
                          "font-size: 16px;\n"
                          "line-height: 19px;\n"
                          "color: #FFFFFF;")
}
MONTHS = {
    'Январь': 'Января',
    'Февраль': 'Февраля',
    'Март': 'Марта',
    'Апрель': 'Апреля',
    'Май': 'Мая',
    'Июнь': 'Июня',
    'Июль': 'Июля',
    'Август': 'Августа',
    'Сентябрь': 'Сентября',
    'Октябрь': 'Октября',
    'Ноябрь': 'Ноября',
    'Декабрь': 'Декабря'
}


class DialogMenu:
    def __init__(self):
        self._translate = QtCore.QCoreApplication.translate

        self.db = sqlite3.connect('data/tasker_data.db')
        self.cur = self.db.cursor()

        self.folder_folderSelect = []

    # - Dialog window methods
    def dialog_error(self, err):
        if err == 'folder_name':
            self.dialog_folder_input.setText('')
            self.dialog_folder_input.setStyleSheet(STYLES['dialog_input_error'])
            self.dialog_error_label.setGeometry(QtCore.QRect(29, 108, 400, 17))
            self.dialog_error_label.setText(self._translate("Dialog", "Название папки должно быть длиной от 1 до 20 "
                                                                      "символов"))
        elif err == 'folders_count':
            self.dialog_error_label.setGeometry(QtCore.QRect(88, 108, 265, 17))
            self.dialog_error_label.setText(self._translate("Dialog", "Вы не можете создать больше 12 папок"))
        elif err == 'task_name':
            self.dialog_task_title_input.setText('')
            self.dialog_task_title_input.setStyleSheet(STYLES['dialog_input_error'])
            self.dialog_error_label.setGeometry(QtCore.QRect(56, 204, 340, 17))
            self.dialog_error_label.setText(self._translate("Dialog", "Название задачи должно быть от 1 до 30 "
                                                                      "символов"))
        self.dialog_error_label.show()

    def hide_dialog(self):
        self.dialog_container.hide()
        self.dialog_folder_container.hide()
        self.dialog_task_container.hide()
        self.dialog_btnDelete.hide()

    def dialog_noDate_action(self):
        if self.sender().status:
            self.sender().setStyleSheet(STYLES['task_btn_inactive'])
            self.sender().setIcon(QtGui.QIcon(''))
            self.sender().status = False

            self.dialog_task_date_edit.setDisabled(False)
        else:
            self.sender().setStyleSheet(STYLES['task_btn_active'])
            noDate_btn_icon = QtGui.QIcon()
            noDate_btn_icon.addPixmap(QtGui.QPixmap("./src/img/task_done.png"), QtGui.QIcon.Normal,
                                      QtGui.QIcon.Off)
            self.sender().setIcon(noDate_btn_icon)
            self.sender().status = True

            self.dialog_task_date_edit.setDisabled(True)

    def dialog_buttons_actions(self):
        if self.sender().action == 'add_folder':
            folders = len(self.cur.execute('''SELECT * FROM folders''').fetchall())
            if folders < 12:
                if 1 <= len(self.dialog_folder_input.text()) <= 20:
                    self.add_folder()
                    self.dialog_action_cancel()
                else:
                    self.dialog_error('folder_name')
            else:
                self.dialog_error('folders_count')
        elif self.sender().action == 'add_task':
            if 1 <= len(self.dialog_task_title_input.text()) <= 30:
                if self.dialog_task_date_noDate_btn.status:
                    date = None
                else:
                    date = self.dialog_task_date_edit.date().toPyDate()

                self.add_task(self.dialog_task_title_input.text(), date, self.dialog_folderSelect_folder)
                self.dialog_action_cancel()

                self.main_page_load(True)
            else:
                self.dialog_error('task_name')
        elif self.sender().action == 'connect_folder':
            self.dialog_folderSelect_folder = self.FolderSelect_folderList.currentItem().id

            if len(self.FolderSelect_folderList.currentItem().text()) > 14:
                self.dialog_task_folder_btn.setText(f'{self.FolderSelect_folderList.currentItem().text()[:14]}...')
            else:
                self.dialog_task_folder_btn.setText(self.FolderSelect_folderList.currentItem().text())

            self.dialog_task_folder_btn.setStyleSheet(STYLES['btn_action_active'])
            self.dialog_task_folder_cancel_btn.show()

            self.FolderSelect_Dialog.hide()
        elif self.sender().action == 'unpair_folder':
            self.dialog_folderSelect_folder = None
            self.dialog_task_folder_btn.setText(self._translate("MainWindow", "Создать задачу"))
            self.dialog_task_folder_btn.setStyleSheet(STYLES['btn_action'])
            self.dialog_task_folder_cancel_btn.hide()
        elif self.sender().action == 'edit_folder':
            if 1 <= len(self.dialog_folder_input.text()) <= 20:
                self.cur.execute('''UPDATE folders SET folder_title = ? WHERE folder_id = ?''',
                                 (self.dialog_folder_input.text(), self.sender().id))
                self._folders_btn_setup()
                self.main_page_load(True)
                self.dialog_action_cancel()
            else:
                self.dialog_error('folder_name')
        elif self.sender().action == 'delete_folder':
            self.cur.execute('''UPDATE tasks SET folder_id = ? WHERE folder_id = ?''', (None, self.sender().id))
            self.cur.execute('''DELETE FROM folders WHERE folder_id = ?''', (self.sender().id,))
            self._folders_btn_setup()
            self.main_page_load(True)
            self.dialog_action_cancel()

        self.db.commit()

    def dialog_action_cancel(self):
        self.dialog_folder_input.setText(self._translate("MainWindow", ""))
        self.hide_dialog()

    def dialog_folderSelect_load(self):
        self.FolderSelect_folderList.deleteLater()

        self.FolderSelect_folderList = QtWidgets.QListWidget(self.FolderSelect_Dialog)
        self.FolderSelect_folderList.setStyleSheet(STYLES['dialog_folderList'])
        self.FolderSelect_folderList.action = "connect_folder"
        self.FolderSelect_folderList.itemDoubleClicked.connect(self.dialog_buttons_actions)

        folders = self.cur.execute('''SELECT * FROM folders''').fetchall()

        for index, folder in enumerate(folders):
            item = QtWidgets.QListWidgetItem(self.FolderSelect_folderList)
            self.FolderSelect_folderList.addItem(item)
            item.setText(self._translate("Dialog", folder[1]))
            item.id = folder[0]
            self.folder_folderSelect.append(item)

        self.FolderSelect_layout.addWidget(self.FolderSelect_folderList, 1, 0, 1, 1)
        self.FolderSelect_Dialog.show()

    def dialog_menu_load(self):
        if self.sender().action == 'add_folder':
            self.dialog.setFixedSize(QtCore.QSize(440, 190))
            self.dialog_title.setText(self._translate("MainWindow", "Создать папку"))
            self.buttons_container.setGeometry(QtCore.QRect(105, 134, self.dialog_btnConfirm.width() * 2 + 10, 36))
            self.dialog_folder_input.setStyleSheet(STYLES['dialog_input'])
            self.dialog_folder_container.show()

            self.dialog_btnConfirm.setText(self._translate("MainWindow", "Создать"))
        elif self.sender().action == 'add_task':
            self.dialog.setFixedSize(QtCore.QSize(440, 287))
            self.dialog_title.setText(self._translate("MainWindow", "Создать задачу"))
            self.buttons_container.setGeometry(QtCore.QRect(107, 230, self.dialog_btnConfirm.width() * 2 + 10, 36))

            self.dialog_task_title_input.setText("")
            self.dialog_task_title_input.setStyleSheet(STYLES['dialog_input'])
            self.dialog_task_date_edit.setDate(self.date)
            self.dialog_task_date_edit.setDisabled(False)
            self.dialog_task_date_noDate_btn.setStyleSheet(STYLES['task_btn_inactive'])
            self.dialog_task_date_noDate_btn.status = False
            self.dialog_task_date_noDate_btn.setIcon(QtGui.QIcon(""))

            self.dialog_btnConfirm.setText(self._translate("MainWindow", "Создать"))

            if self.sender().folder:
                self.dialog_task_folder_btn.setStyleSheet(STYLES['btn_action_active'])
                if len(self.sender().folder[1]) > 14:
                    self.dialog_task_folder_btn.setText(f'{self.sender().folder[1][:14]}...')
                else:
                    self.dialog_task_folder_btn.setText(self.sender().folder[1])

                self.dialog_folderSelect_folder = self.sender().folder[0]
                self.dialog_task_folder_cancel_btn.show()
            else:
                self.dialog_task_folder_btn.setStyleSheet(STYLES['btn_action'])
                self.dialog_task_folder_btn.setText(self._translate("MainWindow", "Добавить в папку"))

                self.dialog_folderSelect_folder = None
                self.dialog_task_folder_cancel_btn.hide()

            self.dialog_task_container.show()
        elif self.sender().action == 'edit_folder':
            folder = self.cur.execute('''SELECT * FROM folders WHERE folder_id = ?''', (self.sender().id,)).fetchone()

            self.dialog.setFixedSize(QtCore.QSize(440, 190))
            self.dialog_title.setText(self._translate("MainWindow", f"Редактировать папку"))
            self.buttons_container.setGeometry(QtCore.QRect(82, 134, self.dialog_btnConfirm.width() * 2 + 10, 36))
            self.dialog_folder_input.setStyleSheet(STYLES['dialog_input'])
            self.dialog_folder_input.setText(self._translate("MainWindow", folder[1]))

            self.dialog_btnDelete.setGeometry(QtCore.QRect(322, 134, 36, 36))
            self.dialog_btnDelete.action = "delete_folder"
            self.dialog_btnDelete.id = self.sender().id
            self.dialog_btnDelete.show()

            self.dialog_btnConfirm.id = self.sender().id
            self.dialog_btnConfirm.setText(self._translate("MainWindow", "Сохранить"))
            self.dialog_folder_container.show()

        self.dialog_error_label.hide()
        self.dialog_btnConfirm.action = self.sender().action
        self.dialog_container.show()

    def _dialog_folderSelect_setup(self):
        self.FolderSelect_Dialog = QtWidgets.QDialog(self.dialog)
        self.FolderSelect_Dialog.setFixedSize(QtCore.QSize(440, 286))
        self.FolderSelect_Dialog.setStyleSheet("background: #151515;")
        self.FolderSelect_Dialog.setSizeGripEnabled(False)
        self.FolderSelect_Dialog.setModal(True)

        self.FolderSelect_layout = QtWidgets.QGridLayout(self.FolderSelect_Dialog)
        self.FolderSelect_layout.setContentsMargins(25, 25, 25, 25)
        self.FolderSelect_layout.setHorizontalSpacing(6)
        self.FolderSelect_layout.setVerticalSpacing(15)

        self.FolderSelect_title = QtWidgets.QLabel(self.FolderSelect_Dialog)
        self.FolderSelect_title.setStyleSheet(STYLES['subtitle'])

        self.FolderSelect_folderList = QtWidgets.QListWidget(self.FolderSelect_Dialog)
        self.FolderSelect_folderList.setStyleSheet(STYLES['dialog_folderList'])

        self.FolderSelect_layout.addWidget(self.FolderSelect_title, 0, 0, 1, 1)

    def _dialog_menu_setup(self):
        self.dialog_container = QtWidgets.QGroupBox(self.centralwidget)
        self.dialog_container.resize(QtCore.QSize(1246, 698))
        self.dialog_container.setStyleSheet("background: rgba(0, 0, 0, 0.5);\nborder: 0;")

        self.dialog_container_layout = QtWidgets.QGridLayout(self.dialog_container)
        self.dialog_container_layout.setContentsMargins(0, 5, 0, 0)

        self.dialog = QtWidgets.QGroupBox(self.dialog_container)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.dialog.sizePolicy().hasHeightForWidth())
        self.dialog.setSizePolicy(sizePolicy)
        self.dialog.setStyleSheet("background: #151515;border-radius: 15px;")

        self.dialog_title = QtWidgets.QLabel(self.dialog)
        self.dialog_title.setGeometry(QtCore.QRect(25, 25, 391, 29))
        self.dialog_title.setStyleSheet(STYLES['subtitle'])

        self.dialog_error_label = QtWidgets.QLabel(self.dialog)
        self.dialog_error_label.setStyleSheet(STYLES['dialog_error'])

        self.buttons_container = QtWidgets.QGroupBox(self.dialog)
        self.buttons_container.setStyleSheet("border: 0;")

        self.buttons_container_layout = QtWidgets.QGridLayout(self.buttons_container)
        self.buttons_container_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_container_layout.setHorizontalSpacing(10)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.dialog_btnConfirm = QtWidgets.QPushButton(self.buttons_container)
        sizePolicy.setHeightForWidth(self.dialog_btnConfirm.sizePolicy().hasHeightForWidth())
        self.dialog_btnConfirm.setSizePolicy(sizePolicy)
        self.dialog_btnConfirm.setFixedSize(QtCore.QSize(110, 36))
        self.dialog_btnConfirm.setStyleSheet(STYLES['dialog_btnConfirm'])
        self.dialog_btnConfirm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dialog_btnConfirm.clicked.connect(self.dialog_buttons_actions)

        self.dialog_btnCancel = QtWidgets.QPushButton(self.buttons_container)
        sizePolicy.setHeightForWidth(self.dialog_btnCancel.sizePolicy().hasHeightForWidth())
        self.dialog_btnCancel.setSizePolicy(sizePolicy)
        self.dialog_btnCancel.setFixedSize(QtCore.QSize(110, 36))
        self.dialog_btnCancel.setStyleSheet(STYLES['dialog_btnCancel'])
        self.dialog_btnCancel.clicked.connect(self.dialog_action_cancel)
        self.dialog_btnCancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.buttons_container_layout.addWidget(self.dialog_btnConfirm, 0, 0, 1, 1)
        self.buttons_container_layout.addWidget(self.dialog_btnCancel, 0, 1, 1, 1)

        self.dialog_btnDelete = QtWidgets.QPushButton(self.dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./src/img/delete_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dialog_btnDelete.setIcon(icon)
        self.dialog_btnDelete.setStyleSheet(STYLES['btn_action'])
        self.dialog_btnDelete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dialog_btnDelete.clicked.connect(self.dialog_buttons_actions)
        self.dialog_btnDelete.hide()

        # Add folder
        self.dialog_folder_container = QtWidgets.QGroupBox(self.dialog)
        self.dialog_folder_container.setGeometry(QtCore.QRect(0, 70, 440, 29))
        self.dialog_folder_container.setStyleSheet("border: 0;")

        self.dialog_folder_label = QtWidgets.QLabel(self.dialog_folder_container)
        self.dialog_folder_label.setGeometry(QtCore.QRect(25, 4, 81, 20))
        self.dialog_folder_label.setStyleSheet(STYLES['dialog_label'])

        self.dialog_folder_input = QtWidgets.QLineEdit(self.dialog_folder_container)
        self.dialog_folder_input.setGeometry(QtCore.QRect(120, 0, 295, 29))
        self.dialog_folder_input.setStyleSheet(STYLES['dialog_input'])

        # Add tas
        self.dialog_task_container = QtWidgets.QGroupBox(self.dialog)
        self.dialog_task_container.setGeometry(QtCore.QRect(0, 70, 440, 125))
        self.dialog_task_container.setStyleSheet("border: 0;")

        self.dialog_task_title_label = QtWidgets.QLabel(self.dialog_task_container)
        self.dialog_task_title_label.setGeometry(QtCore.QRect(25, 4, 81, 20))
        self.dialog_task_title_label.setStyleSheet(STYLES['dialog_label'])

        self.dialog_task_title_input = QtWidgets.QLineEdit(self.dialog_task_container)
        self.dialog_task_title_input.setGeometry(QtCore.QRect(120, 0, 295, 29))
        self.dialog_task_title_input.setStyleSheet(STYLES['dialog_input'])

        self.dialog_task_date_label = QtWidgets.QLabel(self.dialog_task_container)
        self.dialog_task_date_label.setGeometry(QtCore.QRect(25, 48, 42, 20))
        self.dialog_task_date_label.setStyleSheet(STYLES['dialog_label'])

        self.dialog_task_date_edit = QtWidgets.QDateEdit(self.dialog_task_container)
        self.dialog_task_date_edit.setGeometry(QtCore.QRect(120, 44, 85, 29))
        self.dialog_task_date_edit.setStyleSheet(STYLES['dialog_date'])
        self.dialog_task_date_edit.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.dialog_task_date_edit.setTimeSpec(QtCore.Qt.LocalTime)
        self.dialog_task_date_edit.setDisplayFormat('dd.MM.yy')
        self.dialog_task_date_edit.setAlignment(QtCore.Qt.AlignCenter)

        self.dialog_task_date_noDate_btn = QtWidgets.QToolButton(self.dialog_task_container)
        self.dialog_task_date_noDate_btn.setGeometry(QtCore.QRect(230, 48, 95, 20))
        self.dialog_task_date_noDate_btn.setMaximumSize(QtCore.QSize(18, 18))
        self.dialog_task_date_noDate_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dialog_task_date_noDate_btn.clicked.connect(self.dialog_noDate_action)

        self.dialog_task_date_noDate_label = QtWidgets.QLabel(self.dialog_task_container)
        self.dialog_task_date_noDate_label.setGeometry(QtCore.QRect(255, 47, 95, 20))
        self.dialog_task_date_noDate_label.setStyleSheet(STYLES['task_description'])

        self.dialog_task_folder_label = QtWidgets.QLabel(self.dialog_task_container)
        self.dialog_task_folder_label.setGeometry(QtCore.QRect(25, 96, 52, 20))
        self.dialog_task_folder_label.setStyleSheet(STYLES['dialog_label'])

        self.dialog_task_folder_btn = QtWidgets.QPushButton(self.dialog_task_container)
        self.dialog_task_folder_btn.setGeometry(QtCore.QRect(120, 88, 169, 37))
        self.dialog_task_folder_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dialog_task_folder_btn.clicked.connect(self.dialog_folderSelect_load)

        self.dialog_task_folder_cancel_btn = QtWidgets.QPushButton(self.dialog_task_container)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./src/img/cancel_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dialog_task_folder_cancel_btn.setIcon(icon)
        self.dialog_task_folder_cancel_btn.setGeometry(QtCore.QRect(299, 88, 37, 37))
        self.dialog_task_folder_cancel_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dialog_task_folder_cancel_btn.action = 'unpair_folder'
        self.dialog_task_folder_cancel_btn.clicked.connect(self.dialog_buttons_actions)
        self.dialog_task_folder_cancel_btn.setStyleSheet(STYLES['btn_action'])

        self.dialog_container_layout.addWidget(self.dialog, 0, 0, 1, 1)

        self._dialog_folderSelect_setup()
        self.hide_dialog()


class MainWindow_Init(DialogMenu, object):
    def __init__(self):
        super().__init__()

        self.tasks_to_unload = []
        self.folders_to_unload = []

        locale.setlocale(locale.LC_ALL, "ru")
        self.date = dt.date.today()

        self.BTN_HEADER_BASE = 46
        self.BTN_HEADER_HEIGHT = 36
        self.BTN_HEADER_SPACING = 10

    class ClickedLabel(QtWidgets.QLabel):
        clicked = pyqtSignal()

        def mouseReleaseEvent(self, e):
            super().mouseReleaseEvent(e)
            self.clicked.emit()

    # Methods
    # - Folders methods
    @staticmethod
    def folder_click(sender_btn, active_button):
        if sender_btn == active_button:
            pass
        else:
            sender_btn.setStyleSheet(STYLES['btn_active'])
            sender_btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            active_button.setStyleSheet(STYLES['btn_inactive'])
            active_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def add_folder(self):
        self.cur.execute(f'''INSERT INTO folders (folder_title) VALUES (?)''',
                         (self.dialog_folder_input.text(),))
        self.db.commit()
        self._folders_btn_setup()
        self.main_page_load(True)

    def load_folders(self, folders):
        for index, folder in enumerate(folders):
            button = QtWidgets.QPushButton(self.buttons)
            button.setGeometry(QtCore.QRect(25, self.BTN_HEADER_BASE +
                                            ((self.BTN_HEADER_HEIGHT + self.BTN_HEADER_SPACING) * index),
                                            219, 36))
            button.setStyleSheet(STYLES['btn_inactive'])
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            button.setText(self._translate("MainWindow", folder[1]))
            button.folder_id = folder[0]
            button.clicked.connect(self.folder_page_load)

            button.show()
            button.raise_()

            self.folders_to_unload.append(button)

    def unload_folders(self):
        for folder in self.folders_to_unload:
            folder.deleteLater()
        self.folders_to_unload.clear()

    # - Task methods
    def task_action(self):
        self.cur.execute('''UPDATE tasks SET task_status = ? WHERE task_id = ?''',
                         (not self.sender().status, self.sender().id))
        self.db.commit()

        if self.sender().page == 'main':
            self.main_page_load(True)
        elif self.sender().page == 'folder':
            self.folder_page_load(True)

    def add_task(self, title, date, folder):
        self.cur.execute(f'''INSERT INTO tasks (task_description, task_date, folder_id) VALUES (?, ?, ?)''',
                         (title, date, folder))
        self.db.commit()

        self.folder_click(self.btn_menu_main, self.active_button)
        self.active_button.setEnabled(True)
        self.active_button = self.btn_menu_main
        self.active_button.setEnabled(False)
        self.btn_menu_main.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def delete_task(self):
        self.cur.execute('''DELETE FROM tasks WHERE task_id = ?''', (self.sender().id,))
        self.db.commit()

        if self.sender().page == 'main':
            self.main_page_load(True)
        elif self.sender().page == 'folder':
            self.folder_page_load(True)

    def load_tasks(self, tasks, isMainPage, container, layout, withDate=False):
        folder_space = QtWidgets.QLabel()
        folder_space.setMinimumSize(QtCore.QSize(0, 0))
        if tasks:
            for index, task_info in enumerate(tasks):
                task = QtWidgets.QGroupBox(container)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHeightForWidth(task.sizePolicy().hasHeightForWidth())
                task.setSizePolicy(sizePolicy)

                task_layout = QtWidgets.QFormLayout(task)
                task_layout.setContentsMargins(0, 0, 0, 0)

                task_btn = QtWidgets.QToolButton(task)
                task_btn.setMaximumSize(QtCore.QSize(18, 18))
                task_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                task_btn.id = task_info[0]
                task_btn.clicked.connect(self.task_action)

                task_description = self.ClickedLabel(task)
                task_description.setStyleSheet(STYLES['task_description'])
                task_description.setWordWrap(True)
                task_description.id = task_info[0]

                if not task_info[4]:
                    task_btn.setStyleSheet(STYLES['task_btn_inactive'])
                    task_btn.status = False
                else:
                    task_btn.setStyleSheet(STYLES['task_btn_active'])
                    task_btn_icon = QtGui.QIcon()
                    task_btn_icon.addPixmap(QtGui.QPixmap("./src/img/task_done.png"), QtGui.QIcon.Normal,
                                            QtGui.QIcon.Off)
                    task_btn.setIcon(task_btn_icon)
                    task_btn.status = True

                    font = task_description.font()
                    font.setStrikeOut(True)
                    task_description.setFont(font)
                    task_description.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    task_description.clicked.connect(self.delete_task)

                if task_info[2] and withDate:
                    date = task_info[2].split('-')
                    task_description.setText(self._translate("MainWindow", f'{task_info[3]}  '
                                                                           f'{date[2]}.{date[1]}'))
                else:
                    task_description.setText(self._translate("MainWindow", f'{task_info[3]}'))

                if isMainPage:
                    task_btn.page = task_description.page = 'main'
                else:
                    task_btn.page = task_description.page = 'folder'

                task_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, task_btn)
                task_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, task_description)

                layout.addWidget(task)

                self.tasks_to_unload.append(task)

            self.tasks_to_unload.append(folder_space)
            layout.addWidget(folder_space)
        else:
            no_tasks = QtWidgets.QGroupBox(container)
            no_tasks_layout = QtWidgets.QFormLayout(no_tasks)
            no_tasks_layout.setContentsMargins(0, 0, 0, 0)

            no_tasks_description = QtWidgets.QLabel(no_tasks)
            no_tasks_description.setStyleSheet(STYLES['no_tasks'])
            no_tasks_description.setText(self._translate("MainWindow", "Задач нет"))

            no_tasks_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                      no_tasks_description)

            no_tasks.setLayout(no_tasks_layout)
            layout.addWidget(no_tasks)

            self.tasks_to_unload.append(no_tasks)

    def unload_tasks(self):
        for task in self.tasks_to_unload:
            task.deleteLater()
        self.tasks_to_unload.clear()

    # Ui
    # - Pages load
    def main_page_load(self, reload=False):
        if not reload:
            self.folder_click(self.btn_menu_main, self.active_button)
            self.active_button.setEnabled(True)
            self.active_button = self.btn_menu_main
            self.active_button.setEnabled(False)
            self.btn_menu_main.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # Titles
        date = self.date + dt.timedelta(days=3)
        self.main_mainArea_title_4.setText(self._translate("MainWindow", f"{date.strftime('%A').capitalize()}, "
                                                                         f"{int(date.strftime('%d'))} "
                                                                         f"{MONTHS[date.strftime('%B')]}"))

        date = self.date + dt.timedelta(days=4)
        self.main_mainArea_title_5.setText(self._translate("MainWindow", f"{date.strftime('%A').capitalize()}, "
                                                                         f"{int(date.strftime('%d'))} "
                                                                         f"{MONTHS[date.strftime('%B')]}"))

        date = self.date + dt.timedelta(days=5)
        self.main_mainArea_title_6.setText(self._translate("MainWindow", f"{date.strftime('%A').capitalize()}, "
                                                                         f"{int(date.strftime('%d'))} "
                                                                         f"{MONTHS[date.strftime('%B')]}"))

        date = self.date + dt.timedelta(days=6)
        self.main_mainArea_title_7.setText(self._translate("MainWindow", f"{date.strftime('%A').capitalize()}, "
                                                                         f"{int(date.strftime('%d'))} "
                                                                         f"{MONTHS[date.strftime('%B')]}"))

        # Tasks
        self.unload_tasks()
        # MainArea
        # 1
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date = ?''', (self.date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_1, self.main_mainArea_tasks_1_layout)
        # 2
        date = (self.date + dt.timedelta(days=1))
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date = ?''', (date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_2, self.main_mainArea_tasks_2_layout)
        # 3
        date = (self.date + dt.timedelta(days=2))
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date = ?''', (date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_3, self.main_mainArea_tasks_3_layout)
        # 4
        date = (self.date + dt.timedelta(days=3))
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date = ?''', (date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_4, self.main_mainArea_tasks_4_layout)
        # 5
        date = (self.date + dt.timedelta(days=4))
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date = ?''', (date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_5, self.main_mainArea_tasks_5_layout)
        # 6
        date = (self.date + dt.timedelta(days=5))
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date = ?''', (date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_6, self.main_mainArea_tasks_6_layout)
        # 7
        date = (self.date + dt.timedelta(days=6))
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date = ?''', (date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_7, self.main_mainArea_tasks_7_layout)
        # 8
        date = self.date + dt.timedelta(days=6)
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date > ?''', (date,)).fetchall()
        self.load_tasks(tasks, True, self.main_mainArea_tasks_8, self.main_mainArea_tasks_8_layout, True)

        # SecondArea
        # 1
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date < ?''', (self.date,)).fetchall()
        self.load_tasks(tasks, True, self.main_secondArea_tasks_1, self.main_secondArea_tasks_1_layout, True)
        # 2
        tasks = self.cur.execute('''SELECT * FROM tasks WHERE task_date IS NULL''').fetchall()
        self.load_tasks(tasks, True, self.main_secondArea_tasks_2, self.main_secondArea_tasks_2_layout)

        self.main.setCurrentIndex(0)

    def folder_page_load(self, reload=False):
        if not reload:
            self.folder_click(self.sender(), self.active_button)
            self.active_button.setEnabled(True)
            self.sender().setEnabled(False)
            self.active_button = self.sender()

        folder = self.cur.execute(f'''SELECT * FROM folders WHERE folder_id = ?''',
                                  [self.active_button.folder_id]).fetchone()

        tasks = self.cur.execute('''SELECT * FROM tasks WHERE folder_id = ?''',
                                 [self.active_button.folder_id]).fetchall()

        if folder:
            self.folder_title.setText(folder[1])
            self.folder_title.id = folder[0]

            self.folder_btn_add_task.folder = folder

        self.unload_tasks()
        self.load_tasks(tasks, False, self.folder_area_contents, self.folder_area_layout, True)

        self.main.setCurrentIndex(1)

    # - Setups
    def _folders_btn_setup(self):
        self.unload_folders()

        self.btn_menu_main = QtWidgets.QPushButton(self.buttons)
        self.btn_menu_main.setGeometry(QtCore.QRect(25, 0, 219, 36))
        self.btn_menu_main.setStyleSheet(STYLES['btn_active'])
        self.btn_menu_main.setText(self._translate("MainWindow", "Все задачи"))
        self.btn_menu_main.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_menu_main.folder_id = -1
        self.active_button = self.btn_menu_main
        self.btn_menu_main.clicked.connect(self.main_page_load)
        self.btn_menu_main.show()
        self.folders_to_unload.append(self.btn_menu_main)

        folders = self.cur.execute('''SELECT * FROM folders''').fetchall()
        self.load_folders(folders)

    def _main_page_setup(self):
        """Настройка главной вкладки"""

        self.main_page = QtWidgets.QWidget()

        self.main_title = QtWidgets.QLabel(self.main_page)
        self.main_title.setGeometry(QtCore.QRect(25, 45, 927, 29))
        self.main_title.setStyleSheet(STYLES['title'])

        self.main_btn_add_task = QtWidgets.QPushButton(self.main_page)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./src/img/add_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_btn_add_task.setIcon(icon)
        self.main_btn_add_task.setStyleSheet(STYLES['btn_action'])
        self.main_btn_add_task.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.main_btn_add_task.action = "add_task"
        self.main_btn_add_task.clicked.connect(self.dialog_menu_load)
        self.main_btn_add_task.folder = None

        # - Настройка main_mainArea
        self.main_mainArea = QtWidgets.QScrollArea(self.main_page)
        self.main_mainArea.setWidgetResizable(True)
        self.main_mainArea.setStyleSheet("border: 0;")
        self.main_mainArea_contents = QtWidgets.QWidget()

        # - Настройка gridLayout
        self.main_mainArea_layout = QtWidgets.QGridLayout(self.main_mainArea_contents)
        self.main_mainArea_layout.setContentsMargins(25, 0, 25, 25)
        self.main_mainArea_layout.setVerticalSpacing(5)

        # - Titles
        # 1
        self.main_mainArea_title_1 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_1.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_1.setStyleSheet(STYLES['subtitle'])
        # 2
        self.main_mainArea_title_2 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_2.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_2.setStyleSheet(STYLES['subtitle'])
        # 3
        self.main_mainArea_title_3 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_3.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_3.setStyleSheet(STYLES['subtitle'])
        # 4
        self.main_mainArea_title_4 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_4.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_4.setStyleSheet(STYLES['subtitle'])
        # 5
        self.main_mainArea_title_5 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_5.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_5.setStyleSheet(STYLES['subtitle'])
        # 6
        self.main_mainArea_title_6 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_6.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_6.setStyleSheet(STYLES['subtitle'])
        # 7
        self.main_mainArea_title_7 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_7.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_7.setStyleSheet(STYLES['subtitle'])
        # 8
        self.main_mainArea_title_8 = QtWidgets.QLabel(self.main_mainArea_contents)
        self.main_mainArea_title_8.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_mainArea_title_8.setStyleSheet(STYLES['subtitle'])

        # - tasks
        # 1
        self.main_mainArea_tasks_1 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_1_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_1)
        self.main_mainArea_tasks_1_layout.setContentsMargins(0, 5, 0, 0)

        # 2
        self.main_mainArea_tasks_2 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_2_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_2)
        self.main_mainArea_tasks_2_layout.setContentsMargins(0, 5, 0, 0)

        # 3
        self.main_mainArea_tasks_3 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_3_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_3)
        self.main_mainArea_tasks_3_layout.setContentsMargins(0, 5, 0, 0)

        # 4
        self.main_mainArea_tasks_4 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_4_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_4)
        self.main_mainArea_tasks_4_layout.setContentsMargins(0, 5, 0, 0)

        # 5
        self.main_mainArea_tasks_5 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_5_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_5)
        self.main_mainArea_tasks_5_layout.setContentsMargins(0, 5, 0, 0)

        # 6
        self.main_mainArea_tasks_6 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_6_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_6)
        self.main_mainArea_tasks_6_layout.setContentsMargins(0, 5, 0, 0)

        # 7
        self.main_mainArea_tasks_7 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_7_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_7)
        self.main_mainArea_tasks_7_layout.setContentsMargins(0, 5, 0, 0)

        # 8
        self.main_mainArea_tasks_8 = QtWidgets.QGroupBox(self.main_mainArea_contents)
        self.main_mainArea_tasks_8_layout = QtWidgets.QVBoxLayout(self.main_mainArea_tasks_8)
        self.main_mainArea_tasks_8_layout.setContentsMargins(0, 5, 0, 0)

        self.main_mainArea_layout.addWidget(self.main_mainArea_title_1, 0, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_title_2, 0, 1, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_title_3, 3, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_title_4, 3, 1, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_title_5, 5, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_title_6, 5, 1, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_title_7, 7, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_title_8, 7, 1, 1, 1)

        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_1, 1, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_2, 1, 1, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_3, 4, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_4, 4, 1, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_5, 6, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_6, 6, 1, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_7, 8, 0, 1, 1)
        self.main_mainArea_layout.addWidget(self.main_mainArea_tasks_8, 8, 1, 1, 1)
        # end Настройка main_mainArea

        # Настройка main_secondArea
        self.main_secondArea = QtWidgets.QScrollArea(self.main_page)
        self.main_secondArea.setGeometry(QtCore.QRect(708, 20, 271, 691))
        self.main_secondArea.setWidgetResizable(True)
        self.main_secondArea.setStyleSheet("border: 0;\nbackground: #151515;")
        self.main_secondArea_contents = QtWidgets.QWidget()
        self.main_secondArea_contents.setGeometry(QtCore.QRect(0, 0, 271, 691))

        self.main_secondArea_layout = QtWidgets.QGridLayout(self.main_secondArea_contents)
        self.main_secondArea_layout.setContentsMargins(25, 25, 25, 25)
        self.main_secondArea_layout.setVerticalSpacing(5)

        # - Titles
        # 1
        self.main_secondArea_title_1 = QtWidgets.QLabel(self.main_secondArea_contents)
        self.main_secondArea_title_1.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_secondArea_title_1.setStyleSheet(STYLES['subtitle'])
        # 2
        self.main_secondArea_title_2 = QtWidgets.QLabel(self.main_secondArea_contents)
        self.main_secondArea_title_2.setMaximumSize(QtCore.QSize(16777215, 29))
        self.main_secondArea_title_2.setStyleSheet(STYLES['subtitle'])

        self.main_secondArea_layout.addWidget(self.main_secondArea_title_1, 0, 0, 1, 1)
        self.main_secondArea_layout.addWidget(self.main_secondArea_title_2, 2, 0, 1, 1)
        # - end Titles

        # - groups
        self.main_secondArea_tasks_1 = QtWidgets.QGroupBox(self.main_secondArea_contents)
        self.main_secondArea_tasks_1_layout = QtWidgets.QVBoxLayout(self.main_secondArea_tasks_1)
        self.main_secondArea_tasks_1_layout.setContentsMargins(0, 5, 0, 0)

        self.main_secondArea_tasks_2 = QtWidgets.QGroupBox(self.main_secondArea_contents)
        self.main_secondArea_tasks_2_layout = QtWidgets.QVBoxLayout(self.main_secondArea_tasks_2)
        self.main_secondArea_tasks_2_layout.setContentsMargins(0, 5, 0, 0)

        self.main_secondArea_layout.addWidget(self.main_secondArea_tasks_1, 1, 0, 1, 1)
        self.main_secondArea_layout.addWidget(self.main_secondArea_tasks_2, 3, 0, 1, 1)

        self.main_page_load()

        self.main_mainArea.setWidget(self.main_mainArea_contents)
        self.main_secondArea.setWidget(self.main_secondArea_contents)

        self.main.addWidget(self.main_page)

    def _folder_page_setup(self):
        self.folder_page = QtWidgets.QWidget()

        self.folder_title = self.ClickedLabel(self.folder_page)
        self.folder_title.setGeometry(QtCore.QRect(25, 45, 927, 29))
        self.folder_title.setStyleSheet(STYLES['title'])
        self.folder_title.action = 'edit_folder'
        self.folder_title.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.folder_title.clicked.connect(self.dialog_menu_load)

        self.folder_btn_add_task = QtWidgets.QPushButton(self.folder_page)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./src/img/add_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folder_btn_add_task.setIcon(icon)
        self.folder_btn_add_task.setStyleSheet(STYLES['btn_action'])
        self.folder_btn_add_task.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.folder_btn_add_task.action = "add_task"
        self.folder_btn_add_task.clicked.connect(self.dialog_menu_load)

        self.folder_area = QtWidgets.QScrollArea(self.folder_page)
        self.folder_area.setGeometry(QtCore.QRect(0, 90, 977, 628))
        self.folder_area.setMaximumSize(QtCore.QSize(16777215, 977))
        self.folder_area.setWidgetResizable(True)
        self.folder_area.setStyleSheet("border: 0;")

        self.folder_area_contents = QtWidgets.QWidget()
        self.folder_area_contents.setGeometry(QtCore.QRect(0, 0, 977, 628))

        self.folder_area_layout = QtWidgets.QVBoxLayout(self.folder_area_contents)
        self.folder_area_layout.setContentsMargins(25, 0, 25, 25)
        self.folder_area_layout.setSpacing(12)

        self.folder_area.setWidget(self.folder_area_contents)

        self.main.addWidget(self.folder_page)

    # - Main setup
    def setupUi(self, MainWindow):
        # Настройка отображения главного экрана
        MainWindow.resize(QtCore.QSize(1246, 698))
        MainWindow.setMinimumSize(QtCore.QSize(1246, 698))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/src/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background: #191919;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # end Настройка отображения главного экрана

        # Настройка главного меню
        # - Header
        self.header = QtWidgets.QGroupBox(self.centralwidget)
        self.header.setEnabled(True)
        self.header.setStyleSheet("border: 0;\nbackground: #151515;")
        # - Logo
        self.logo = QtWidgets.QLabel(self.header)
        self.logo.setGeometry(QtCore.QRect(25, 20, 145, 50))
        self.logo.setPixmap(QtGui.QPixmap("./src/img/logo.png"))
        # - Add folder btn
        self.header_btn__addFolder = QtWidgets.QPushButton(self.header)
        self.header_btn__addFolder.setGeometry(QtCore.QRect(208, 27, 36, 36))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./src/img/add_folder_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.header_btn__addFolder.setIcon(icon)
        self.header_btn__addFolder.setStyleSheet(STYLES['btn_action'])
        self.header_btn__addFolder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.header_btn__addFolder.action = "add_folder"
        self.header_btn__addFolder.clicked.connect(self.dialog_menu_load)
        # - Buttons
        self.buttons = QtWidgets.QGroupBox(self.header)
        self.buttons.setGeometry(QtCore.QRect(0, 88, 269, 594))

        self._folders_btn_setup()
        # end Настройка главного меню

        # Настройка main
        self.main = QtWidgets.QStackedWidget(self.centralwidget)

        self._main_page_setup()
        self._folder_page_setup()
        self._dialog_menu_setup()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(self._translate("MainWindow", "Tasker"))
        self.main_title.setText(self._translate("MainWindow", "Все задачи"))
        self.main_mainArea_title_1.setText(self._translate("MainWindow", "Сегодня"))
        self.main_mainArea_title_2.setText(self._translate("MainWindow", "Завтра"))
        self.main_mainArea_title_3.setText(self._translate("MainWindow", "Послезавтра"))
        self.main_mainArea_title_8.setText(self._translate("MainWindow", "Предстоящие"))
        self.main_secondArea_title_1.setText(self._translate("MainWindow", "Просроченные"))
        self.main_secondArea_title_2.setText(self._translate("MainWindow", "Без даты"))
        self.dialog_btnCancel.setText(self._translate("MainWindow", "Отменить"))
        self.dialog_folder_label.setText(self._translate("MainWindow", "Название:"))
        self.dialog_task_title_label.setText(self._translate("MainWindow", "Название:"))
        self.dialog_task_date_label.setText(self._translate("MainWindow", "Дата:"))
        self.dialog_task_date_noDate_label.setText(self._translate("MainWindow", "Без даты"))
        self.dialog_task_folder_label.setText(self._translate("MainWindow", "Папка:"))
        self.FolderSelect_Dialog.setWindowTitle(self._translate("Dialog", "Добавить в папку"))
        self.FolderSelect_title.setText(self._translate("Dialog", "Добавить в папку"))
        __sortingEnabled = self.FolderSelect_folderList.isSortingEnabled()
        self.FolderSelect_folderList.setSortingEnabled(False)
        self.FolderSelect_folderList.setSortingEnabled(__sortingEnabled)


class MainWindow(QtWidgets.QMainWindow, MainWindow_Init):
    resized = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.resized.connect(self.resizeUI)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def resizeUI(self):
        w = self.width()
        h = self.height()

        self.header.setGeometry(QtCore.QRect(0, 0, 269, h))
        self.main.move(QtCore.QPoint(269, -20))
        self.main.setFixedSize(QtCore.QSize(w, h + 20))
        self.main_btn_add_task.setGeometry(QtCore.QRect(w - 600, 43, 37, 37))
        self.main_mainArea.move(QtCore.QPoint(0, 90))
        self.main_mainArea.setFixedSize(QtCore.QSize(w - 540, h))
        self.main_secondArea.move(QtCore.QPoint(w - 540, 20))
        self.main_secondArea.setFixedSize(QtCore.QSize(271, h))
        self.folder_btn_add_task.setGeometry(QtCore.QRect(w - 331, 43, 37, 37))
        self.dialog_container.resize(QtCore.QSize(w, h))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

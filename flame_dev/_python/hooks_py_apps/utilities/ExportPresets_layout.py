# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_hook_layout.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PySide.QtCore import *
from PySide.QtGui import *
import sys


class Ui_ExportPresetsLayout(object):
    def setupUi(self, ExportPresetsLayout):

        self.centralWidget = QWidget(ExportPresetsLayout)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(30, 30, 30, 30)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
########################################## PRESET01 ##########################
        self.preset01Path = QLabel(self.centralWidget)
        self.preset01Path.setEnabled(True)
        self.preset01Path.setObjectName("preset01Path")
        self.gridLayout.addWidget(self.preset01Path, 0, 0, 1, 1)
        self.preset01PathField = QLineEdit(self.centralWidget)
        self.preset01PathField.setText("")
        self.preset01PathField.setObjectName("preset01PathField")
        self.gridLayout.addWidget(self.preset01PathField, 0, 1, 1, 2)
        self.browsePath = QPushButton(self.centralWidget)
        self.browsePath.setObjectName("browsePath")
        self.gridLayout.addWidget(self.browsePath, 0, 3, 1, 1)
        self.preset01Name = QLabel(self.centralWidget)
        self.preset01Name.setObjectName("preset01Name")
        self.gridLayout.addWidget(self.preset01Name, 1, 0, 1, 1)
        self.preset01NameField = QLineEdit(self.centralWidget)
        self.preset01NameField.setText("")
        self.preset01NameField.setObjectName("preset01NameField")
        self.gridLayout.addWidget(self.preset01NameField, 1, 1, 1, 2)
########################################## PRESET02 ##########################
        self.preset02Path = QLabel(self.centralWidget)
        self.preset02Path.setEnabled(True)
        self.preset02Path.setObjectName("preset02Path")
        self.gridLayout.addWidget(self.preset02Path, 2, 0, 1, 1)
        self.preset02PathField = QLineEdit(self.centralWidget)
        self.preset02PathField.setText("")
        self.preset02PathField.setObjectName("preset02PathField")
        self.gridLayout.addWidget(self.preset02PathField, 2, 1, 1, 2)
        self.browsePath02 = QPushButton(self.centralWidget)
        self.browsePath02.setObjectName("browsePath02")
        self.gridLayout.addWidget(self.browsePath02, 2, 3, 1, 1)
        self.preset02Name = QLabel(self.centralWidget)
        self.preset02Name.setObjectName("preset02Name")
        self.gridLayout.addWidget(self.preset02Name, 3, 0, 1, 1)
        self.preset02NameField = QLineEdit(self.centralWidget)
        self.preset02NameField.setText("")
        self.preset02NameField.setObjectName("preset02NameField")
        self.gridLayout.addWidget(self.preset02NameField, 3, 1, 1, 2)
########################################## PRESET03 ##########################
        self.preset03Path = QLabel(self.centralWidget)
        self.preset03Path.setEnabled(True)
        self.preset03Path.setObjectName("preset03Path")
        self.gridLayout.addWidget(self.preset03Path, 4, 0, 1, 1)
        self.preset03PathField = QLineEdit(self.centralWidget)
        self.preset03PathField.setText("")
        self.preset03PathField.setObjectName("preset03PathField")
        self.gridLayout.addWidget(self.preset03PathField, 4, 1, 1, 2)
        self.browsePath03 = QPushButton(self.centralWidget)
        self.browsePath03.setObjectName("browsePath03")
        self.gridLayout.addWidget(self.browsePath03, 4, 3, 1, 1)
        self.preset03Name = QLabel(self.centralWidget)
        self.preset03Name.setObjectName("preset03Name")
        self.gridLayout.addWidget(self.preset03Name, 5, 0, 1, 1)
        self.preset03NameField = QLineEdit(self.centralWidget)
        self.preset03NameField.setText("")
        self.preset03NameField.setObjectName("preset03NameField")
        self.gridLayout.addWidget(self.preset03NameField, 5, 1, 1, 2)
########################################## PRESET04 ##########################
        self.preset04Path = QLabel(self.centralWidget)
        self.preset04Path.setEnabled(True)
        self.preset04Path.setObjectName("preset04Path")
        self.gridLayout.addWidget(self.preset04Path, 6, 0, 1, 1)
        self.preset04PathField = QLineEdit(self.centralWidget)
        self.preset04PathField.setText("")
        self.preset04PathField.setObjectName("preset04PathField")
        self.gridLayout.addWidget(self.preset04PathField, 6, 1, 1, 2)
        self.browsePath04 = QPushButton(self.centralWidget)
        self.browsePath04.setObjectName("browsePath04")
        self.gridLayout.addWidget(self.browsePath04, 6, 3, 1, 1)
        self.preset04Name = QLabel(self.centralWidget)
        self.preset04Name.setObjectName("preset04Name")
        self.gridLayout.addWidget(self.preset04Name, 7, 0, 1, 1)
        self.preset04NameField = QLineEdit(self.centralWidget)
        self.preset04NameField.setText("")
        self.preset04NameField.setObjectName("preset04NameField")
        self.gridLayout.addWidget(self.preset04NameField, 7, 1, 1, 2)
########################################## PRESET05 ##########################
        self.preset05Path = QLabel(self.centralWidget)
        self.preset05Path.setEnabled(True)
        self.preset05Path.setObjectName("preset05Path")
        self.gridLayout.addWidget(self.preset05Path, 8, 0, 1, 1)
        self.preset05PathField = QLineEdit(self.centralWidget)
        self.preset05PathField.setText("")
        self.preset05PathField.setObjectName("preset05PathField")
        self.gridLayout.addWidget(self.preset05PathField, 8, 1, 1, 2)
        self.browsePath05 = QPushButton(self.centralWidget)
        self.browsePath05.setObjectName("browsePath05")
        self.gridLayout.addWidget(self.browsePath05, 8, 3, 1, 1)
        self.preset05Name = QLabel(self.centralWidget)
        self.preset05Name.setObjectName("preset05Name")
        self.gridLayout.addWidget(self.preset05Name, 9, 0, 1, 1)
        self.preset05NameField = QLineEdit(self.centralWidget)
        self.preset05NameField.setText("")
        self.preset05NameField.setObjectName("preset05NameField")
        self.gridLayout.addWidget(self.preset05NameField, 9, 1, 1, 2)

        # self.browseProject = QPushButton(self.centralWidget)
        # self.browseProject.setObjectName("browseProject")
        # self.gridLayout.addWidget(self.browseProject, 1, 3, 1, 1)
        self.pushButton_save = QPushButton(self.centralWidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.gridLayout.addWidget(self.pushButton_save, 12, 3, 1, 1)
        ExportPresetsLayout.setCentralWidget(self.centralWidget)
        self.preset01Path.setBuddy(self.preset01PathField)
        self.preset01Name.setBuddy(self.preset01NameField)
#
        self.preset02Path.setBuddy(self.preset02PathField)
        self.preset02Name.setBuddy(self.preset02NameField)

        self.preset03Path.setBuddy(self.preset03PathField)
        self.preset03Name.setBuddy(self.preset03NameField)

        self.preset04Path.setBuddy(self.preset04PathField)
        self.preset04Name.setBuddy(self.preset04NameField)

        self.preset05Path.setBuddy(self.preset05PathField)
        self.preset05Name.setBuddy(self.preset05NameField)
#
        self.retranslateUi(ExportPresetsLayout)
        QMetaObject.connectSlotsByName(ExportPresetsLayout)
        ExportPresetsLayout.setTabOrder(self.preset01PathField, self.browsePath)
        ExportPresetsLayout.setTabOrder(self.browsePath, self.preset01NameField)
        ExportPresetsLayout.setTabOrder(self.preset02PathField, self.browsePath02)
        ExportPresetsLayout.setTabOrder(self.browsePath02, self.preset02NameField)
        ExportPresetsLayout.setTabOrder(self.preset03PathField, self.browsePath03)
        ExportPresetsLayout.setTabOrder(self.browsePath03, self.preset03NameField)
        ExportPresetsLayout.setTabOrder(self.preset04PathField, self.browsePath04)
        ExportPresetsLayout.setTabOrder(self.browsePath04, self.preset04NameField)
        ExportPresetsLayout.setTabOrder(self.preset05PathField, self.browsePath05)
        ExportPresetsLayout.setTabOrder(self.browsePath05, self.preset05NameField)

    def retranslateUi(self, ExportPresetsLayout):
        _translate = QCoreApplication.translate
        ExportPresetsLayout.setWindowTitle(_translate("ExportPresetsLayout", "exportHook"))
        self.preset01Path.setText(_translate("ExportPresetsLayout", "Preset 01 Path"))
        self.browsePath.setText(_translate("ExportPresetsLayout", "browse"))
        self.preset01Name.setText(_translate("ExportPresetsLayout", "Preset 01 Name"))
#
        self.preset02Path.setText(_translate("ExportPresetsLayout", "Preset 02 Path"))
        self.browsePath02.setText(_translate("ExportPresetsLayout", "browse"))
        self.preset02Name.setText(_translate("ExportPresetsLayout", "Preset 02 Name"))

        self.preset03Path.setText(_translate("ExportPresetsLayout", "Preset 03 Path"))
        self.browsePath03.setText(_translate("ExportPresetsLayout", "browse"))
        self.preset03Name.setText(_translate("ExportPresetsLayout", "Preset 03 Name"))

        self.preset04Path.setText(_translate("ExportPresetsLayout", "Preset 04 Path"))
        self.browsePath04.setText(_translate("ExportPresetsLayout", "browse"))
        self.preset04Name.setText(_translate("ExportPresetsLayout", "Preset 04 Name"))

        self.preset05Path.setText(_translate("ExportPresetsLayout", "Preset 05 Path"))
        self.browsePath05.setText(_translate("ExportPresetsLayout", "browse"))
        self.preset05Name.setText(_translate("ExportPresetsLayout", "Preset 05 Name"))
#
        self.pushButton_save.setText(_translate("ExportPresetsLayout", "save "))

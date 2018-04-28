# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_hook_layout.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PySide.QtCore import *
from PySide.QtGui import *
import sys


class Ui_ProjectPathsLayout(object):
    def setupUi(self, ProjectPathsLayout):

        self.centralWidget = QWidget(ProjectPathsLayout)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(30, 30, 30, 30)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.projectRootPath = QLabel(self.centralWidget)
        self.projectRootPath.setEnabled(True)

        self.projectRootPath.setObjectName("projectRootPath")
        self.gridLayout.addWidget(self.projectRootPath, 0, 0, 1, 1)
        self.projectRootPathField = QLineEdit(self.centralWidget)
        self.projectRootPathField.setText("")
        self.projectRootPathField.setObjectName("projectRootPathField")
        self.gridLayout.addWidget(self.projectRootPathField, 0, 1, 1, 2)
        self.browsePath = QPushButton(self.centralWidget)
        self.browsePath.setObjectName("browsePath")
        self.gridLayout.addWidget(self.browsePath, 0, 3, 1, 1)
        self.project = QLabel(self.centralWidget)
        self.project.setObjectName("project")
        self.gridLayout.addWidget(self.project, 1, 0, 1, 1)
        self.projectNameField = QLineEdit(self.centralWidget)
        self.projectNameField.setText("")
        self.projectNameField.setObjectName("projectNameField")
        self.gridLayout.addWidget(self.projectNameField, 1, 1, 1, 2)
        self.browseProject = QPushButton(self.centralWidget)
        self.browseProject.setObjectName("browseProject")
        self.gridLayout.addWidget(self.browseProject, 1, 3, 1, 1)
        self.pushButton_save = QPushButton(self.centralWidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.gridLayout.addWidget(self.pushButton_save, 7, 3, 1, 1)
        ProjectPathsLayout.setCentralWidget(self.centralWidget)
        self.projectRootPath.setBuddy(self.projectRootPathField)
        self.project.setBuddy(self.projectNameField)
        self.retranslateUi(ProjectPathsLayout)
        QMetaObject.connectSlotsByName(ProjectPathsLayout)
        ProjectPathsLayout.setTabOrder(self.projectRootPathField, self.browsePath)
        ProjectPathsLayout.setTabOrder(self.browsePath, self.projectNameField)

    def retranslateUi(self, ProjectPathsLayout):
        _translate = QCoreApplication.translate
        ProjectPathsLayout.setWindowTitle(_translate("ProjectPathsLayout", "exportHook"))
        self.projectRootPath.setText(_translate("ProjectPathsLayout", "Root Projects Path"))
        self.browsePath.setText(_translate("ProjectPathsLayout", "browse"))
        self.project.setText(_translate("ProjectPathsLayout", "Project"))
        self.browseProject.setText(_translate("ProjectPathsLayout", "browse"))
        self.pushButton_save.setText(_translate("ProjectPathsLayout", "save "))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_hook_layout.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PySide.QtCore import *
from PySide.QtGui import *
import sys


class Ui_infoStaffLayout(object):
    def setupUi(self, infoStaffLayout):

        infoStaffLayout.setObjectName("infoStaffLayout")
        infoStaffLayout.resize(693, 353)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(infoStaffLayout.sizePolicy().hasHeightForWidth())
        infoStaffLayout.setSizePolicy(sizePolicy)
        # infoStaffLayout.setTabShape(QTabWidget.Rounded)
        self.centralWidget = QWidget(infoStaffLayout)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.projectLead = QLabel(self.centralWidget)
        self.projectLead.setObjectName("projectLead")
        self.gridLayout.addWidget(self.projectLead, 2, 0, 1, 1)
        self.projectLeadName = QLineEdit(self.centralWidget)
        self.projectLeadName.setText("")
        self.projectLeadName.setObjectName("projectLeadName")
        self.gridLayout.addWidget(self.projectLeadName, 2, 1, 1, 1)
        self.projectLeadEmail = QLineEdit(self.centralWidget)

        self.projectLeadEmail.setSizePolicy(sizePolicy)
        self.projectLeadEmail.setText("")
        self.projectLeadEmail.setObjectName("projectLeadEmail")
        self.gridLayout.addWidget(self.projectLeadEmail, 2, 2, 1, 1)
        self.producer = QLabel(self.centralWidget)
        self.producer.setObjectName("producer")
        self.gridLayout.addWidget(self.producer, 3, 0, 1, 1)
        self.producerName = QLineEdit(self.centralWidget)
        self.producerName.setText("")
        self.producerName.setObjectName("producerName")
        self.gridLayout.addWidget(self.producerName, 3, 1, 1, 1)
        self.producerEmail = QLineEdit(self.centralWidget)
        self.producerEmail.setText("")
        self.producerEmail.setObjectName("producerEmail")
        self.gridLayout.addWidget(self.producerEmail, 3, 2, 1, 1)
        self.project2dLead = QLabel(self.centralWidget)
        self.project2dLead.setObjectName("project2dLead")
        self.gridLayout.addWidget(self.project2dLead, 4, 0, 1, 1)
        self.project2dLeadName = QLineEdit(self.centralWidget)
        self.project2dLeadName.setText("")
        self.project2dLeadName.setObjectName("project2dLeadName")
        self.gridLayout.addWidget(self.project2dLeadName, 4, 1, 1, 1)
        self.project2dLeadEmail = QLineEdit(self.centralWidget)
        self.project2dLeadEmail.setText("")
        self.project2dLeadEmail.setObjectName("project2dLeadEmail")
        self.gridLayout.addWidget(self.project2dLeadEmail, 4, 2, 1, 1)
        self.project3dLead = QLabel(self.centralWidget)
        self.project3dLead.setObjectName("project3dLead")
        self.gridLayout.addWidget(self.project3dLead, 5, 0, 1, 1)
        self.project3dLeadName = QLineEdit(self.centralWidget)
        self.project3dLeadName.setText("")
        self.project3dLeadName.setObjectName("project3dLeadName")
        self.gridLayout.addWidget(self.project3dLeadName, 5, 1, 1, 1)
        self.project3dLeadEmail = QLineEdit(self.centralWidget)
        self.project3dLeadEmail.setText("")
        self.project3dLeadEmail.setObjectName("project3dLeadEmail")
        self.gridLayout.addWidget(self.project3dLeadEmail, 5, 2, 1, 1)
        self.vfxTeam = QLabel(self.centralWidget)
        self.vfxTeam.setObjectName("vfxTeam")
        self.gridLayout.addWidget(self.vfxTeam, 6, 0, 1, 1)
        self.vfxTeamAlias = QLineEdit(self.centralWidget)
        self.vfxTeamAlias.setText("")
        self.vfxTeamAlias.setObjectName("vfxTeamAlias")
        self.gridLayout.addWidget(self.vfxTeamAlias, 6, 1, 1, 1)
        self.vfxTeamEmail = QLineEdit(self.centralWidget)
        self.vfxTeamEmail.setText("")
        self.vfxTeamEmail.setObjectName("vfxTeamEmail")
        self.gridLayout.addWidget(self.vfxTeamEmail, 6, 2, 1, 1)
        self.pushButton_save = QPushButton(self.centralWidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.gridLayout.addWidget(self.pushButton_save, 7, 3, 1, 1)

        infoStaffLayout.setCentralWidget(self.centralWidget)

        self.actionSet = QAction(infoStaffLayout)
        self.actionSet.setObjectName("actionSet")
        self.actioncolorpolicy = QAction(infoStaffLayout)
        self.actioncolorpolicy.setObjectName("actioncolorpolicy")

        self.projectLead.setBuddy(self.projectLeadName)
        self.producer.setBuddy(self.producerName)
        self.project2dLead.setBuddy(self.project2dLeadName)
        self.project3dLead.setBuddy(self.project3dLeadName)
        self.vfxTeam.setBuddy(self.vfxTeamAlias)

        self.retranslateUi(infoStaffLayout)
        QMetaObject.connectSlotsByName(infoStaffLayout)
        infoStaffLayout.setTabOrder(self.projectLeadEmail, self.producerName)
        infoStaffLayout.setTabOrder(self.producerName, self.producerEmail)
        infoStaffLayout.setTabOrder(self.producerEmail, self.project2dLeadName)
        infoStaffLayout.setTabOrder(self.project2dLeadName, self.project2dLeadEmail)
        infoStaffLayout.setTabOrder(self.project2dLeadEmail, self.project3dLeadName)
        infoStaffLayout.setTabOrder(self.project3dLeadName, self.project3dLeadEmail)
        infoStaffLayout.setTabOrder(self.project3dLeadEmail, self.vfxTeamAlias)
        infoStaffLayout.setTabOrder(self.vfxTeamAlias, self.vfxTeamEmail)

    def retranslateUi(self, infoStaffLayout):
        _translate = QCoreApplication.translate
        infoStaffLayout.setWindowTitle(_translate("infoStaffLayout", "exportHook"))

        self.projectLead.setText(_translate("infoStaffLayout", "Project Lead"))
        self.producer.setText(_translate("infoStaffLayout", "Producer"))
        self.project2dLead.setText(_translate("infoStaffLayout", "2D Lead"))
        self.project3dLead.setText(_translate("infoStaffLayout", "3D Lead"))
        self.vfxTeam.setText(_translate("infoStaffLayout", "vfx team"))
        self.pushButton_save.setText(_translate("infoStaffLayout", "save "))

        self.actionSet.setText(_translate("infoStaffLayout", "Set"))
        self.actioncolorpolicy.setText(_translate("infoStaffLayout", "Color Policy"))

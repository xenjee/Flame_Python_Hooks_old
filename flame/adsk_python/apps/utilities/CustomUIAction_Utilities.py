import os
import subprocess as sb

# yaml need to be added into the Flame python's package thingy.
import yaml

# yaml config files:
import ProjectPaths_layout
import infoStaff_layout
import ExportPresets_layout

# PySide stuff, included with Flame default install.
# quick and lazy import *
from PySide.QtCore import *
from PySide.QtGui import *

print '-' * 80
print 'In customUIAction Hook:'
print "Using: PySide"

# Import the current config. Will be used later to setText (fileFullPath) in the ExportPresetsTab class
yaml_export_presets = '/var/tmp/flame/adsk_python/apps/utilities/ExportPresets_result.yaml'

with open(yaml_export_presets, 'r') as config:
    cfg = yaml.load(config)

export_preset01_name = cfg["export_preset01"]["name"]
export_preset01_path = cfg["export_preset01"]["path"]
export_preset02_name = cfg["export_preset02"]["name"]
export_preset02_path = cfg["export_preset02"]["path"]
export_preset03_name = cfg["export_preset03"]["name"]
export_preset03_path = cfg["export_preset03"]["path"]
export_preset04_name = cfg["export_preset04"]["name"]
export_preset04_path = cfg["export_preset04"]["path"]
export_preset05_name = cfg["export_preset05"]["name"]
export_preset05_path = cfg["export_preset05"]["path"]

# adds entries to Flame contextual menu.


def getCustomUIActions():

    action20 = {}
    action20["name"] = "exports_config"
    action20["caption"] = "Exports Config"

    action2 = {}
    action2["name"] = "blender_Launch"
    action2["caption"] = "Blender"

    action4 = {}
    action4["name"] = "natron_launch"
    action4["caption"] = "Natron"

    action10 = {}
    action10["name"] = "screenshot"
    action10["caption"] = "Screenshot"

    action25 = {}
    action25["name"] = "Metadata"
    action25["caption"] = "Clip Metadata"

    appGroup3 = {}
    appGroup3["name"] = "Tools"
    appGroup3["actions"] = (action20, action10, action25,)

    appGroup2 = {}
    appGroup2["name"] = "Launch"
    appGroup2["actions"] = (action2, action4,)

    return (appGroup3, appGroup2,)


# Defines a behavior for each action.
# in this case, launches a QT (PySide) app base on a main 'Qdialog' (TabDialog), with 3 types of operations split in 3 tabs.
# Each tab is a class: PathsTab, StaffTab, ExportPresetsTab.
# Each class contains a 'save' button to create or update a yaml config file that will later be used in the 'custom export hook' script.
def customUIAction(info, userData):

    if info['name'] == 'lattice_launch':
        sb.Popen('/Applications/Lattice.app/Contents/MacOS/Lattice')

    if info['name'] == 'blender_Launch':
        sb.Popen('/Applications/blender.app/Contents/MacOS/blender')

    if info['name'] == 'natron_launch':
        sb.Popen('/Applications/Natron.app/Contents/MacOS/Natron')

    if info['name'] == 'Metadata':
        class Ui_Form(object):
            def setupUi(self, Form):
                Form.setObjectName("Form")
                Form.resize(950, 495)
                self.verticalLayout_4 = QVBoxLayout(Form)
                self.verticalLayout_4.setObjectName("verticalLayout_4")
                self.horizontalLayout_2 = QHBoxLayout()
                self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.pushButton = QPushButton(Form)
                self.pushButton.setObjectName("pushButton")
                self.horizontalLayout_2.addWidget(self.pushButton)
                self.pushButton_2 = QPushButton(Form)
                self.pushButton_2.setObjectName("pushButton_2")
                self.horizontalLayout_2.addWidget(self.pushButton_2)
                self.pushButton_3 = QPushButton(Form)
                self.pushButton_3.setObjectName("pushButton_3")
                self.horizontalLayout_2.addWidget(self.pushButton_3)
                self.verticalLayout_4.addLayout(self.horizontalLayout_2)
                self.verticalLayout_5 = QVBoxLayout()
                self.verticalLayout_5.setObjectName("verticalLayout_5")
                self.textEdit = QTextEdit(Form)
                self.textEdit.setObjectName("textEdit")
                self.verticalLayout_5.addWidget(self.textEdit)
                self.verticalLayout_4.addLayout(self.verticalLayout_5)
                self.textEdit.setReadOnly(True)

                self.retranslateUi(Form)
                QMetaObject.connectSlotsByName(Form)

                # Button actions

                def frameSource():
                    cmdB1 = '/usr/discreet/wiretap/tools/current/wiretap_get_frames', '-p', '-n', nodeID
                    clip_SOURCE, err = sb.Popen(cmdB1, stdout=sb.PIPE).communicate()
                    self.textEdit.setText(clip_SOURCE)

                def frameXML():
                    cmdB2 = '/usr/discreet/wiretap/tools/current/wiretap_get_metadata', '-n', nodeID, '-s', 'XML'
                    clip_XML, err = sb.Popen(cmdB2, stdout=sb.PIPE).communicate()
                    self.textEdit.setText(clip_XML)

                def frameEDL():
                    cmdB3 = '/usr/discreet/wiretap/tools/current/wiretap_get_metadata', '-n', nodeID, '-s', 'EDL'
                    clip_EDL, err = sb.Popen(cmdB3, stdout=sb.PIPE).communicate()
                    self.textEdit.setText(clip_EDL)

                # Connect

                QObject.connect(self.pushButton, SIGNAL('clicked()'), frameSource)
                QObject.connect(self.pushButton_2, SIGNAL('clicked()'), frameXML)
                QObject.connect(self.pushButton_3, SIGNAL('clicked()'), frameEDL)

            def retranslateUi(self, Form):
                Form.setWindowTitle(QApplication.translate("Form", "Clip Info", None, QApplication.UnicodeUTF8))
                self.pushButton.setText(QApplication.translate("Form", "Source Path", None, QApplication.UnicodeUTF8))
                self.pushButton_2.setText(QApplication.translate("Form", "XML - Metadata", None, QApplication.UnicodeUTF8))
                self.pushButton_3.setText(QApplication.translate("Form", "EDL - Metadata", None, QApplication.UnicodeUTF8))

        # app = QtGui.QApplication.instance()
        app = QApplication.activePopupWidget()
        Form = QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        Form.show()
        nodeID = info['selection'][0]
        app.exec_()

    if info['name'] == 'exports_config':
        # __appname__ = "Tab Dialog"

        # general GUI 'container'
        class TabDialog(QDialog):
            def __init__(self, parent=None):
                super(TabDialog, self).__init__(parent)

                fileInfo = QFileInfo()

                w = 800
                h = 200
                self.setMinimumSize(w, h)

                tabWidget = QTabWidget()
                tabWidget.addTab(PathsTab(fileInfo), "Project Paths")
                tabWidget.addTab(StaffTab(fileInfo), "Staff Contact Infos")
                tabWidget.addTab(ExportPresetsTab(fileInfo), "Export Presets")

                # buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
                buttonBox.accepted.connect(self.accept)
                buttonBox.rejected.connect(self.reject)

                mainLayout = QVBoxLayout()
                mainLayout.addWidget(tabWidget)
                mainLayout.addWidget(buttonBox)

                self.setLayout(mainLayout)

                self.setWindowTitle("Config Utilities")

        # Project root path and project name: browse or type. Saved to ProjectPaths_config_result.yaml
        class PathsTab(QMainWindow, ProjectPaths_layout.Ui_ProjectPathsLayout):
            def __init__(self, fileInfo, parent=None):
                super(PathsTab, self).__init__(parent)

                self.setupUi(self)  # This is defined in export_hook_layout.py file automatically. It sets up layout and widgets that are defined
                self.pushButton_save.clicked.connect(self.saveYaml)  # When the button is pressed: saves the yaml config file
                self.browsePath.clicked.connect(self.browse_path)  # When the button is pressed: Execute browse_path function
                self.browseProject.clicked.connect(self.browse_project)  # When the button is pressed: Execute browse_folder function

                # Placeholders and default values
                self.projectRootPathField.setText("/var/tmp/flame/house_projects/")
                self.projectNameField.setPlaceholderText("17P000_project_name")

            def browse_path(self):
                self.projectRootPathField.clear()  # In case there are any existing elements in the list
                directory = QFileDialog.getExistingDirectory(self, "browse")
                # execute getExistingDirectory dialog and set the directory variable to be equal to the user selected directory

                if directory:  # if user didn't pick a directory don't continue
                    # self.projectNameField.saveLastOpenedDir(directory) # >>>>>>>> NOT WORKING - Crashes
                    self.projectRootPathField.setText(os.path.normpath(directory))

            def browse_project(self):
                self.projectNameField.clear()  # In case there are any existing elements in the list
                directory = QFileDialog.getExistingDirectory(self, "browse")

                if directory:
                    self.projectNameField.setText(os.path.basename(directory))

            def store_UIcontent(self):
                pass

            # YAML = Save the yaml config file for PathsTab
            def saveYaml(self):
                data = {
                    'projects_root_path': self.projectRootPathField.text(),
                    'project_name': self.projectNameField.text(),

                }
                with open('/var/tmp/flame/adsk_python/apps/utilities/ProjectPaths_config_result.yaml', 'w') as export_hook_config:
                    export_hook_config.write(yaml.safe_dump(data))

        # Choose a set of export presets to be available in the Flame contextual menu.
        class ExportPresetsTab (QMainWindow, ExportPresets_layout.Ui_ExportPresetsLayout):
            def __init__(self, fileInfo, parent=None):
                super(ExportPresetsTab, self).__init__(parent)

                self.setupUi(self)
                self.pushButton_save.clicked.connect(self.saveYaml)  # When the button is pressed: saves the yaml config file
                self.browsePath.clicked.connect(self.browse_path)  # When the button is pressed: Execute browse_path function.
                self.browsePath02.clicked.connect(self.browse_path02)  # When the button is pressed: Execute browse_path function.
                self.browsePath03.clicked.connect(self.browse_path03)  # When the button is pressed: Execute browse_path function.
                self.browsePath04.clicked.connect(self.browse_path04)  # When the button is pressed: Execute browse_path function.
                self.browsePath05.clicked.connect(self.browse_path05)  # When the button is pressed: Execute browse_path function.

                # Default values. Read from existing Yaml config file. > Always start with actual config.
                # Maybe it should also have a reset to default option, reading from a seperate file?
                self.preset01PathField.setText(export_preset01_path)
                self.preset01NameField.setText(export_preset01_name)

                self.preset02PathField.setText(export_preset02_path)
                self.preset02NameField.setText(export_preset02_name)

                self.preset03PathField.setText(export_preset03_path)
                self.preset03NameField.setText(export_preset03_name)

                self.preset04PathField.setText(export_preset04_path)
                self.preset04NameField.setText(export_preset04_name)

                self.preset05PathField.setText(export_preset05_path)
                self.preset05NameField.setText(export_preset05_name)

            def browse_path(self):
                FileFullPath = QFileDialog.getOpenFileName(self, "browse")

                if FileFullPath:  # if user didn't pick a file don't continue
                    self.preset01PathField.setText(FileFullPath[0])

            def browse_path02(self):
                FileFullPath = QFileDialog.getOpenFileName(self, "browse")

                if FileFullPath:  # if user didn't pick a file don't continue
                    self.preset02PathField.setText(FileFullPath[0])

            def browse_path03(self):
                FileFullPath = QFileDialog.getOpenFileName(self, "browse")

                if FileFullPath:  # if user didn't pick a File don't continue
                    self.preset03PathField.setText(FileFullPath[0])

            def browse_path04(self):
                # self.preset03PathField.clear()  # In case there are any existing elements in the list
                FileFullPath = QFileDialog.getOpenFileName(self, "browse")

                if FileFullPath:  # if user didn't pick a directory don't continue
                    # self.projectNameField.saveLastOpenedDir(directory)
                    self.preset04PathField.setText(FileFullPath[0])

            def browse_path05(self):
                # self.preset03PathField.clear()  # In case there are any existing elements in the list
                FileFullPath = QFileDialog.getOpenFileName(self, "browse")

                if FileFullPath:  # if user didn't pick a directory don't continue
                    # self.projectNameField.saveLastOpenedDir(directory)
                    self.preset05PathField.setText(FileFullPath[0])

            def store_UIcontent(self):
                pass

            # YAML = Save the yaml config file for ExportPresetsTab
            def saveYaml(self):
                data = {
                    'export_preset01': {
                        'path': self.preset01PathField.text(),
                        'name': self.preset01NameField.text(),
                    },
                    'export_preset02': {
                        'path': self.preset02PathField.text(),
                        'name': self.preset02NameField.text(),
                    },
                    'export_preset03': {
                        'path': self.preset03PathField.text(),
                        'name': self.preset03NameField.text(),
                    },
                    'export_preset04': {
                        'path': self.preset04PathField.text(),
                        'name': self.preset04NameField.text(),
                    },
                    'export_preset05': {
                        'path': self.preset05PathField.text(),
                        'name': self.preset05NameField.text(),
                    }
                }
                with open('/private/var/tmp/flame/adsk_python/apps/utilities/ExportPresets_result.yaml', 'w') as Export_Presets_config:
                    Export_Presets_config.write(yaml.safe_dump(data))

        # Gives a set of names and emails that will conditionaly chosen (per export type, from 'export presets types') from within the custom export hook
        class StaffTab(QMainWindow, infoStaff_layout.Ui_infoStaffLayout):
            def __init__(self, fileInfo, parent=None):
                super(StaffTab, self).__init__(parent)

                self.setupUi(self)  # This is defined in infoStaff_layout.py file automatically. It sets up layout and widgets that are defined
                self.pushButton_save.clicked.connect(self.saveYaml)
                self.projectLeadName.setText("Stefan Lead")
                self.projectLeadEmail.setText("xenjee@gmail.com")
                self.producerName.setText("Stefan Prod")
                self.producerEmail.setText("stefan@pulsevfx.com")
                self.project2dLeadName.setPlaceholderText("2d Lead's Name")
                self.project2dLeadEmail.setPlaceholderText("2dLead@company.com")
                self.project3dLeadName.setPlaceholderText("3d Lead's Name")
                self.project3dLeadEmail.setPlaceholderText("3dLead@company.com")
                self.vfxTeamAlias.setPlaceholderText("Project: team's alias")
                self.vfxTeamEmail.setPlaceholderText("team@company.com")

            def store_UIcontent(self):
                pass

            # YAML = Save the yaml config file for StaffTab
            def saveYaml(self):
                data = {
                    'staff': {
                        'producer': {
                            'name': self.producerName.text(),
                            'email': self.producerEmail.text(),
                        },
                        'project_lead': {
                            'name': self.projectLeadName.text(),
                            'email': self.projectLeadEmail.text(),
                        },
                        'project_2d_lead': {
                            'name': self.project2dLeadName.text(),
                            'email': self.project2dLeadEmail.text(),
                        },
                        'project_3d_lead': {
                            'name': self.project3dLeadName.text(),
                            'email': self.project3dLeadEmail.text(),
                        },
                        'vfx_team': {
                            'name': self.vfxTeamAlias.text(),
                            'email': self.vfxTeamEmail.text(),
                        }
                    }

                }
                with open('/var/tmp/flame/adsk_python/apps/utilities/InfoStaff_config_result.yaml', 'w') as InfoStaff_config:
                    InfoStaff_config.write(yaml.safe_dump(data))

        tabdialog = TabDialog()
        tabdialog.show()
        # sys.exit(tabdialog.exec_()) #  doesn't seem to work from Flame.
        app.exec_()

    if info['name'] == 'screenshot':
        # __appname__ = "Screenshot"

        class Screenshot(QWidget):
            def __init__(self):
                super(Screenshot, self).__init__()

                self.screenshotLabel = QLabel()
                self.screenshotLabel.setSizePolicy(QSizePolicy.Expanding,
                                                   QSizePolicy.Expanding)
                self.screenshotLabel.setAlignment(Qt.AlignCenter)
                self.screenshotLabel.setMinimumSize(240, 160)

                self.createOptionsGroupBox()
                self.createButtonsLayout()

                mainLayout = QVBoxLayout()
                mainLayout.addWidget(self.screenshotLabel)
                mainLayout.addWidget(self.optionsGroupBox)
                mainLayout.addLayout(self.buttonsLayout)
                self.setLayout(mainLayout)

                self.shootScreen()
                self.delaySpinBox.setValue(5)

                self.setWindowTitle("Screenshot")
                self.resize(300, 200)

            def resizeEvent(self, event):
                scaledSize = self.originalPixmap.size()
                scaledSize.scale(self.screenshotLabel.size(), Qt.KeepAspectRatio)
                if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
                    self.updateScreenshotLabel()

            def newScreenshot(self):
                if self.hideThisWindowCheckBox.isChecked():
                    self.hide()
                self.newScreenshotButton.setDisabled(True)

                QTimer.singleShot(self.delaySpinBox.value() * 1000,
                                  self.shootScreen)

            def saveScreenshot(self):
                format = 'png'
                initialPath = QDir.currentPath() + "/untitled." + format

                fileName, _ = QFileDialog.getSaveFileName(self, "Save As",
                                                          initialPath,
                                                          "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
                if fileName:
                    self.originalPixmap.save(fileName, format)

            def shootScreen(self):
                if self.delaySpinBox.value() != 0:
                    qApp.beep()

                # Garbage collect any existing image first.
                self.originalPixmap = None
                self.originalPixmap = QPixmap.grabWindow(QApplication.desktop().winId())
                self.updateScreenshotLabel()

                self.newScreenshotButton.setDisabled(False)
                if self.hideThisWindowCheckBox.isChecked():
                    self.show()

            def updateCheckBox(self):
                if self.delaySpinBox.value() == 0:
                    self.hideThisWindowCheckBox.setDisabled(True)
                else:
                    self.hideThisWindowCheckBox.setDisabled(False)

            def createOptionsGroupBox(self):
                self.optionsGroupBox = QGroupBox("Options")

                self.delaySpinBox = QSpinBox()
                self.delaySpinBox.setSuffix(" s")
                self.delaySpinBox.setMaximum(60)
                self.delaySpinBox.valueChanged.connect(self.updateCheckBox)

                self.delaySpinBoxLabel = QLabel("Screenshot Delay:")

                self.hideThisWindowCheckBox = QCheckBox("Hide This Window")

                optionsGroupBoxLayout = QGridLayout()
                optionsGroupBoxLayout.addWidget(self.delaySpinBoxLabel, 0, 0)
                optionsGroupBoxLayout.addWidget(self.delaySpinBox, 0, 1)
                optionsGroupBoxLayout.addWidget(self.hideThisWindowCheckBox, 1, 0, 1, 2)
                self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

            def createButtonsLayout(self):
                self.newScreenshotButton = self.createButton("New Screenshot",
                                                             self.newScreenshot)

                self.saveScreenshotButton = self.createButton("Save Screenshot",
                                                              self.saveScreenshot)

                self.quitScreenshotButton = self.createButton("Quit", self.close)

                self.buttonsLayout = QHBoxLayout()
                self.buttonsLayout.addStretch()
                self.buttonsLayout.addWidget(self.newScreenshotButton)
                self.buttonsLayout.addWidget(self.saveScreenshotButton)
                self.buttonsLayout.addWidget(self.quitScreenshotButton)

            def createButton(self, text, member):
                button = QPushButton(text)
                button.clicked.connect(member)
                return button

            def updateScreenshotLabel(self):
                self.screenshotLabel.setPixmap(self.originalPixmap.scaled(
                    self.screenshotLabel.size(), Qt.KeepAspectRatio,
                    Qt.SmoothTransformation))

        # app = QApplication(sys.argv)
        form = Screenshot()
        form.show()
        # sys.exit(app.exec_())
        app.exec_()


print '- End of customUIAction Hook:'
print '-' * 80


# Stefan Gaillot - 2017/09/28


##################################

# import os
from PySide.QtCore import *
from PySide.QtGui import *
import sys
# import mainGui
from PySide import QtCore, QtGui
import subprocess

sys.path.append('/Users/stefan/XenDrive/___VFX/DEV/PYTHON/Modules')
sys.path.append('/opt/flame_dev/_python/modules')

import snippets.connected_duplicate_02a as _dupli
reload(_dupli)
import snippets.matte_cleaner_01a as _cleaner
reload(_cleaner)
import snippets.mvr_back_to_beauty as _btb
reload(_btb)
#import snippets.find_nodes as _findNodes
# reload(_findNodes)


def getCustomUIActions():

    action1 = {}
    action1["name"] = "snippets_v1"
    action1["caption"] = "Snippets"

    appGroup1 = {}
    appGroup1["name"] = "snippets v1"
    appGroup1["actions"] = (action1,)

    return (appGroup1,)


def customUIAction(info, userData):
    if info['name'] == 'snippets_v1':
        class my_Dialog(QDialog):

            ################ CREATE MAIN WINDOW #################

            def __init__(self, parent=None):
                super(my_Dialog, self).__init__(parent)

                self.createClickIconsBox()

                mainLayout = QVBoxLayout()
                mainLayout.addWidget(self.horizontalGroupBox)

                self.setLayout(mainLayout)
                self.setWindowTitle("Toolkit Snippets")
                self.resize(400, 150)

            def createClickIconsBox(self):
                self.horizontalGroupBox = QGroupBox()
                layout = QHBoxLayout()

                button1 = QPushButton("dupli")
                button1.clicked.connect(self.runDupli)
                button1.setIcon(QIcon(":/icons/snippet01-icon.png"))
                button1.setFlat(True)
                layout.addWidget(button1)
                button2 = QPushButton("Cleaner")
                button2.clicked.connect(self.runCleaner)
                button2.setIcon(QIcon(":/icons/snippet02-icon.png"))
                button2.setFlat(True)
                layout.addWidget(button2)

                button3 = QPushButton("Btb")
                self.connect(button3, SIGNAL("clicked()"), self.dialogOpenBtb)
                button3.clicked.connect(self.runBtb)
                button3.setIcon(QIcon(":/icons/snippet03-icon.png"))
                button3.setFlat(True)
                layout.addWidget(button3)

                button6 = QPushButton("more")
                button6.clicked.connect(self.runMore)
                button6.setIcon(QIcon(":/icons/exit-icon.png"))
                button6.setFlat(True)
                layout.addWidget(button6)
                # button6.clicked.connect(QCoreApplication.instance().quit)

                self.horizontalGroupBox.setLayout(layout)
                self.resize(400, 150)

################  #################

            def dialogOpenBtb(self):
                dialog = DialogShot()

                global shot_text
                global elt_text

                if dialog.exec_():
                    shot_text = str(dialog.shotName.text())
                    elt_text = str(dialog.elementName.text())


################  BUTTONS ACTIONS (Run Snippets) #################

            def runDupli(self):
                print "The script 'Duplicate & Connect should be executed"
                _dupli.main()

            def runCleaner(self):
                print "The script 'Matte Cleaner' should be executed"
                _cleaner.main()

            def runBtb(self):
                print "The script 'Back to Beauty' should be executed"
                _btb.main(shot_text, elt_text)

            # def findNode(self):
            #     _findNodes.main()

            def runMore(self):
                print "The script 'button4' should be executed, a text file should be open"
                file_path = '/Users/stefan/XenDrive/___VFX/FLAME_STUFF/FLAME_DEV/PYTHON/Hooks_dev/run_snippets_app/openMe.txt'
                file_path2 = './openMe.txt'

                subprocess.call(["open", file_path])

################  DIALOGS FOR USER's INPUTS #################

        class DialogShot(QDialog):

            def __init__(self, parent=None):
                super(DialogShot, self).__init__(parent)

                self.setWindowTitle("Shot & Element names.")

                shotStore = None
                elementStore = None

                self.shotName = QLineEdit()
                self.shotLabel = QLabel('Shot name:')
                self.shotInput = self.shotName.text()
                self.elementName = QLineEdit()
                self.elementLabel = QLabel('Element name:')
                self.elementInput = self.elementName.text()
                buttonOk = QPushButton("OK")
                buttonCancel = QPushButton("Cancel")

                layout = QGridLayout()
                layout.addWidget(self.shotLabel, 0, 0)
                layout.addWidget(self.shotName, 0, 1)
                layout.addWidget(self.elementLabel, 1, 0)
                layout.addWidget(self.elementName, 1, 1)
                layout.addWidget(buttonOk)
                layout.addWidget(buttonCancel)

                self.setLayout(layout)

                self.connect(buttonOk, SIGNAL("clicked()"), self, SLOT("accept()"))
                self.connect(buttonCancel, SIGNAL("clicked()"), self, SLOT("reject()"))


#############################################

        # app = QtGui.QApplication.instance()
        app = QApplication.activePopupWidget()
        form = my_Dialog()
        form.show()
        app.exec_()

from PySide.QtCore import *
from PySide.QtGui import *
print "Using: PySide"
import sys


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

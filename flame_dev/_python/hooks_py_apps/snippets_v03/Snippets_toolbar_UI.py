#!/usr/bin/env python

from PySide.QtGui import *
from PySide import QtGui
from PySide import QtCore
import sys


class Snippets_toolbar(QDialog):

    def __init__(self, parent=None, data=list()):
        super(Snippets_toolbar, self).__init__(parent)

        self.mainLayout = QHBoxLayout()

        self.ButtonsToBox = QGroupBox()
        self.mainLayout.addWidget(self.ButtonsToBox)
        self.group_layout = QHBoxLayout()
        self.ButtonsToBox.setLayout(self.group_layout)
        # self.mainLayout.addLayout(self.group_layout)

        self.addButtonsToBox(data)

        self.setLayout(self.mainLayout)

        self.setGeometry(670, 30, 600, 50)

        self.setWindowTitle("Snippets Toolbar")

    def default_callback(self):
        print "No callback assigned!"

    def addButtonsToBox(self, data, update=False):

        for key in data:
            if key['widget_type'] == 'button':
                print key['label'] + ": " + key['widget_type']
                button = QPushButton()
                button.setText(key['label'])
                button.setIcon(QIcon(key['icon']))
                button.setFlat(True)
                callback = key.get('callback', self.default_callback)
                button.clicked.connect(callback)
                self.group_layout.addWidget(button)

        print '-' * 5

from PySide.QtGui import *
from PySide import QtCore, QtGui
import sys


class Snippets_toolbar(QDialog):

    def __init__(self, parent=None, data=list()):
        super(Snippets_toolbar, self).__init__(parent)

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)
        self.setWindowTitle("Main Container")
        self.resize(600, 50)

        self.create_ui(data)

    def default_callback(self):
        print "No callback assigned!"

    def create_ui(self, data, update=False):

        for key in data:
            if key['widget_type'] == 'button':
                print key['label'] + ": " + key['widget_type']
                button = QPushButton()
                button.setText(key['label'])
                button.setIcon(QIcon(key['icon']))
                button.setFlat(True)

                callback = key.get('callback', self.default_callback)
                button.clicked.connect(callback)

                self.layout().addWidget(button)

        print '-' * 5

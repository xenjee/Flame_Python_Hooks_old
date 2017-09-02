
# Stefan Gaillot - 2017/05/05

# There should be a README file in the package this file is originally part off.

# Many thanks to Bob Mapple, Mike Taylor, Lewis Saunders, Mikael Morin LeBlanc, Tommy hooper, Vlad Bakic, Tommy Furukawa and Sean Farell for their kind and well inspired help.

# 2017/05/05 ...  this project will hopefully soon be accessible there: https://github.com/xenjee

###
# About the first half of theses apps come from Bo Milanovich classes. I incorporated (adapted) them into a Flame friendly CustomUIAction python hook.
# https://github.com/xenjee/pythonbo (fork)
# https://www.youtube.com/channel/UCpjNEyIUW8E8ZQ0JbYA8isw
# http://bomilanovich.com/blog/

###
# The second half apps come from Trolltech.
# Again, i just adapted them for Flame.
# they are accessible there:
# http://www.trolltech.com/products/qt/opensource.html
# 'If you are unsure which license is appropriate for your use, please review the following information:
# http://www.trolltech.com/products/qt/licensing.html'

##################################
# I'm not sure of how to put the rest about licences, i'll look into that and will update.
# So far i'm just trying to be fair and give credits to the the right persons and organizations.
# This is a personnal research/learning project.
##################################

###
# The 'Config' app is from me.
# It imports another script for the UI, created in QT creator 5 (Pyqty5) and later manualy converted to pyside.
# it needs to import the yaml module.
# It's a first test in an attempt to modify some export presets, team infos and some paths. Work in progress.

###
# I'll try to take some time to import in a better way than the lazy import*. Good enough for this first test/step.
# For further informations or some suggestions/better ways, you can contact me at xenjee@gmail.com

##################################

# import sys
import os
# import exportHook_layout
# import yaml
import showGui
import mainGui
from PySide.QtCore import *
from PySide.QtGui import *
print "Using: PySide"


def getCustomUIActions():

    action1 = {}
    action1["name"] = "text_field"
    action1["caption"] = "Text Field *args**kwargs"

    action2 = {}
    action2["name"] = "pick_color"
    action2["caption"] = "Pick Color"

    action3 = {}
    action3["name"] = "calculator"
    action3["caption"] = "Simple Maths"

    action4 = {}
    action4["name"] = "dumb_dialog"
    action4["caption"] = "Dumb Dialog"

    action5 = {}
    action5["name"] = "standart_dialog"
    action5["caption"] = "Standart Dialog"

    action6 = {}
    action6["name"] = "Incorporating_UI"
    action6["caption"] = "Incorporating UI"

    action7 = {}
    action7["name"] = "QMainWindow"
    action7["caption"] = "QMainWindow"

    action8 = {}
    action8["name"] = "basic_layout"
    action8["caption"] = "Basic Layout"

    action9 = {}
    action9["name"] = "sliders_group"
    action9["caption"] = "Sliders Group"

    action10 = {}
    action10["name"] = "screenshot"
    action10["caption"] = "Screenshot"

    action11 = {}
    action11["name"] = "easing"
    action11["caption"] = "Easing"

    action12 = {}
    action12["name"] = "line_edit"
    action12["caption"] = "Line Edit"

    action14 = {}
    action14["name"] = "groupbox"
    action14["caption"] = "Groupbox"

    action15 = {}
    action15["name"] = "tab_dialog"
    action15["caption"] = "Tab Dialog"

    appGroup2 = {}
    appGroup2["name"] = "Examples"
    appGroup2["actions"] = (action1, action2, action3, action4, action5, action6, action7, action8, action9, action10, action11, action12, action14, action15,)

    return (appGroup2,)


def customUIAction(info, userData):
    if info['name'] == 'text_field':
        class CustomWidget(QWidget):
            def __init__(self, *args, **kwargs):
                super(CustomWidget, self).__init__(*args, **kwargs)

                self.my_layout = QHBoxLayout(self)

                self.my_label = QLabel('text field:')
                self.my_layout.addWidget(self.my_label)

                self.my_input = QLineEdit()
                self.my_layout.addWidget(self.my_input)

        # app = QApplication([])
        wdg = CustomWidget()
        wdg.show()
        app.exec_()

    if info['name'] == 'pick_color':
        class ButtonPainter(object):
            def __init__(self, button):
                self.button = button

            def choose_color(self):
                # Select color
                color = QColorDialog().getColor()

                if color.isValid():
                    self.button.setStyleSheet(u'background-color:' + color.name())
                else:
                    msgbox = QMessageBox()
                    msgbox.setWindowTitle(u'No Color was Selected')
                    msgbox.exec_()

        # Create top level window/button
        button = QPushButton('Choose Color')
        # button.clicked.connect() doesn't support passing custom parameters to handler function (reference to the  button that we want to paint), so we create object that will hold this parameter
        button_painter = ButtonPainter(button)

        button.clicked.connect(button_painter.choose_color)

        button.show()
        app.exec_()

    if info['name'] == 'calculator':
        class my_Form(QDialog):
            def __init__(self, parent=None):
                super(my_Form, self).__init__(parent)

                self.browser = QTextBrowser()
                self.lineedit = QLineEdit("Type an expression and press Enter")
                self.lineedit.selectAll()

                layout = QVBoxLayout()
                layout.addWidget(self.browser)
                layout.addWidget(self.lineedit)
                self.setLayout(layout)

                self.lineedit.setFocus()

                # self.connect(self.lineedit, SIGNAL("returnPressed()"), self.updateUi)  # not pyqt friendly
                self.lineedit.returnPressed.connect(self.updateUi)
                self.setWindowTitle("Calculate")

            def updateUi(self):
                try:
                    text = self.lineedit.text()
                    self.browser.append("%s = <b>%s</b>" % (text, eval(text)))
                except:
                    self.browser.append("<font color=red>%s is invalid</font>" % text)

        # app = QApplication(sys.argv)
        app = QApplication.activePopupWidget()
        form = my_Form()
        form.show()
        app.exec_()

    if info['name'] == 'dumb_dialog':
        __appname__ = "basic dialog"

        class Program(QDialog):

            def __init__(self, parent=None):
                super(Program, self).__init__(parent)

                self.setWindowTitle(__appname__)

                btn = QPushButton("Open Dialog")
                self.label1 = QLabel("Label 1 Result")
                self.label2 = QLabel("Label 2 Result")

                layout = QVBoxLayout()
                layout.addWidget(btn)
                layout.addWidget(self.label1)
                layout.addWidget(self.label2)
                self.setLayout(layout)

                # self.connect(btn, SIGNAL("clicked()"), self.dialogOpen)
                btn.clicked.connect(self.dialogOpen)

            def dialogOpen(self):
                dialog = Dialog()
                if dialog.exec_():
                    self.label1.setText("Spinbox value is " + str(dialog.spinBox.value()))
                    self.label2.setText("Checkbox is " + str(dialog.checkBox.isChecked()))
                else:
                    QMessageBox.warning(self, __appname__, "Dialog canceled.")

        class Dialog(QDialog):

            def __init__(self, parent=None):
                super(Dialog, self).__init__(parent)

                self.setWindowTitle("Dialog.")

                self.checkBox = QCheckBox("Check me out!")
                self.spinBox = QSpinBox()
                buttonOk = QPushButton("OK")
                buttonCancel = QPushButton("Cancel")

                layout = QGridLayout()
                layout.addWidget(self.spinBox, 0, 0)
                layout.addWidget(self.checkBox, 0, 1)
                layout.addWidget(buttonCancel)
                layout.addWidget(buttonOk)
                self.setLayout(layout)

                # self.connect(buttonOk, SIGNAL("clicked()"), self, SLOT("accept()"))
                buttonOk.clicked.connect(self, SLOT("accept()"))
                # self.connect(buttonCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
                buttonCancel.clicked.connect(self, SLOT("reject()"))

        # app = QApplication(sys.argv)
        form = Program()
        form.show()
        app.exec_()

    if info['name'] == 'standart_dialog':
        __appname__ = "Tenth Video"

        class Program2(QDialog):

            def __init__(self, parent=None):
                super(Program2, self).__init__(parent)

                self.setWindowTitle(__appname__)

                btn = QPushButton("Open Dialog")
                self.mainSpinBox = QSpinBox()
                self.mainCheckBox = QCheckBox("Main Checkbox Value")

                layout = QVBoxLayout()
                layout.addWidget(self.mainSpinBox)
                layout.addWidget(self.mainCheckBox)
                layout.addWidget(btn)
                self.setLayout(layout)

                self.connect(btn, SIGNAL("clicked()"), self.dialogOpen)

            def dialogOpen(self):
                initValues = {"mainSpinBox": self.mainSpinBox.value(), "mainCheckBox": self.mainCheckBox.isChecked()}
                dialog = Dialog2(initValues)
                if dialog.exec_():
                    self.mainSpinBox.setValue(dialog.spinBox.value())
                    self.mainCheckBox.setChecked(dialog.checkBox.isChecked())

        class Dialog2(QDialog):

            def __init__(self, initValues, parent=None):
                super(Dialog2, self).__init__(parent)

                self.setWindowTitle("Dialog2.")

                self.checkBox = QCheckBox("Check me out!")
                self.spinBox = QSpinBox()
                buttonOk = QPushButton("OK")
                buttonCancel = QPushButton("Cancel")

                layout = QGridLayout()
                layout.addWidget(self.spinBox, 0, 0)
                layout.addWidget(self.checkBox, 0, 1)
                layout.addWidget(buttonCancel)
                layout.addWidget(buttonOk)
                self.setLayout(layout)

                self.spinBox.setValue(initValues["mainSpinBox"])
                self.checkBox.setChecked(initValues["mainCheckBox"])

                self.connect(buttonOk, SIGNAL("clicked()"), self, SLOT("accept()"))
                self.connect(buttonCancel, SIGNAL("clicked()"), self, SLOT("reject()"))

            def accept(self):
                class GreaterThanFive(Exception):
                    pass

                class IsZero(Exception):
                    pass

                try:
                    if self.spinBox.value() > 5:
                        raise GreaterThanFive, ("The SpinBox value cannot be greater than 5")
                    elif self.spinBox.value() == 0:
                        raise IsZero, ("The SpinBox value cannot be equal to 0")
                    else:
                        QDialog.accept(self)

                except GreaterThanFive, e:
                    QMessageBox.warning(self, __appname__, str(e))
                    self.spinBox.selectAll()
                    self.spinBox.setFocus()
                    return

                except IsZero, e:
                    QMessageBox.warning(self, __appname__, str(e))
                    self.spinBox.selectAll()
                    self.spinBox.setFocus()
                    return

        # app = QApplication(sys.argv)
        form = Program2()
        form.show()
        app.exec_()

    if info['name'] == 'Incorporating_UI':
        __appname__ = "Thirteenth Video"

        class MainDialog(QDialog, showGui.Ui_mainDialog):

            def __init__(self, parent=None):
                super(MainDialog, self).__init__(parent)
                self.setupUi(self)

                self.connect(self.showButton, SIGNAL("clicked()"), self.showMessageBox)

            def showMessageBox(self):
                QMessageBox.information(self, "Hello!", "Hello there, " + self.nameEdit.text())

        # app = QApplication(sys.argv)
        form = MainDialog()
        form.show()
        app.exec_()

    if info['name'] == 'QMainWindow':
        __appname__ = "sixteenth Video"

        class MainWindow(QMainWindow, mainGui.Ui_MainWindow):

            mojsignal = Signal(str)

            def __init__(self, parent=None):
                super(MainWindow, self).__init__(parent)
                self.setupUi(self)

                # self.connect(self.actionExit, SIGNAL("clicked()"), self.exitApp)
                self.actionExit.triggered.connect(self.exitApp)
                self.mojsignal.connect(self.zdravo)

            def zdravo(self, lol):
                print lol

            def exitApp(self):
                self.mojsignal.emit("Zdravo!")

        # app = QApplication(sys.argv)
        form = MainWindow()
        form.show()
        app.exec_()

    if info['name'] == 'basic_layout':
        __appname__ = "Basic Layout"

        class my_Dialog(QDialog):
            NumGridRows = 3
            NumButtons = 4

            def __init__(self, parent=None):
                super(my_Dialog, self).__init__(parent)

                self.createMenu()
                self.createHorizontalGroupBox()
                self.createGridGroupBox()
                self.createFormGroupBox()

                bigEditor = QTextEdit()
                bigEditor.setPlainText("This widget takes up all the remaining space "
                                       "in the top-level layout.")

                buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

                buttonBox.accepted.connect(self.accept)
                buttonBox.rejected.connect(self.reject)

                mainLayout = QVBoxLayout()
                mainLayout.setMenuBar(self.menuBar)
                mainLayout.addWidget(self.horizontalGroupBox)
                mainLayout.addWidget(self.gridGroupBox)
                mainLayout.addWidget(self.formGroupBox)
                mainLayout.addWidget(bigEditor)
                mainLayout.addWidget(buttonBox)
                self.setLayout(mainLayout)

                self.setWindowTitle("Basic Layouts")

            def createMenu(self):
                self.menuBar = QMenuBar()

                self.fileMenu = QMenu("&File", self)
                self.exitAction = self.fileMenu.addAction("E&xit")
                self.menuBar.addMenu(self.fileMenu)

                self.exitAction.triggered.connect(self.accept)

            def createHorizontalGroupBox(self):
                self.horizontalGroupBox = QGroupBox("Horizontal layout")
                layout = QHBoxLayout()

                for i in range(my_Dialog.NumButtons):
                    button = QPushButton("Button %d" % (i + 1))
                    layout.addWidget(button)

                self.horizontalGroupBox.setLayout(layout)

            def createGridGroupBox(self):
                self.gridGroupBox = QGroupBox("Grid layout")
                layout = QGridLayout()

                for i in range(my_Dialog.NumGridRows):
                    label = QLabel("Line %d:" % (i + 1))
                    lineEdit = QLineEdit()
                    layout.addWidget(label, i + 1, 0)
                    layout.addWidget(lineEdit, i + 1, 1)

                self.smallEditor = QTextEdit()
                self.smallEditor.setPlainText("This widget takes up about two thirds "
                                              "of the grid layout.")

                layout.addWidget(self.smallEditor, 0, 2, 4, 1)

                layout.setColumnStretch(1, 10)
                layout.setColumnStretch(2, 20)
                self.gridGroupBox.setLayout(layout)

            def createFormGroupBox(self):
                self.formGroupBox = QGroupBox("Form layout")
                layout = QFormLayout()
                layout.addRow(QLabel("Line 1:"), QLineEdit())
                layout.addRow(QLabel("Line 2, long text:"), QComboBox())
                layout.addRow(QLabel("Line 3:"), QSpinBox())
                self.formGroupBox.setLayout(layout)

        # app = QApplication(sys.argv)
        form = my_Dialog()
        form.show()
        app.exec_()

    if info['name'] == 'sliders_group':
        __appname__ = "Sliders Group"

        class SlidersGroup(QGroupBox):

            valueChanged = Signal(int)

            def __init__(self, orientation, title, parent=None):
                super(SlidersGroup, self).__init__(title, parent)

                self.slider = QSlider(orientation)
                self.slider.setFocusPolicy(Qt.StrongFocus)
                self.slider.setTickPosition(QSlider.TicksBothSides)
                self.slider.setTickInterval(10)
                self.slider.setSingleStep(1)

                self.scrollBar = QScrollBar(orientation)
                self.scrollBar.setFocusPolicy(Qt.StrongFocus)

                self.dial = QDial()
                self.dial.setFocusPolicy(Qt.StrongFocus)

                self.slider.valueChanged[int].connect(self.scrollBar.setValue)
                self.scrollBar.valueChanged[int].connect(self.dial.setValue)
                self.dial.valueChanged[int].connect(self.slider.setValue)
                self.dial.valueChanged[int].connect(self.valueChanged)

                if orientation == Qt.Horizontal:
                    direction = QBoxLayout.TopToBottom
                else:
                    direction = QBoxLayout.LeftToRight

                slidersLayout = QBoxLayout(direction)
                slidersLayout.addWidget(self.slider)
                slidersLayout.addWidget(self.scrollBar)
                slidersLayout.addWidget(self.dial)
                self.setLayout(slidersLayout)

            def setValue(self, value):
                self.slider.setValue(value)

            def setMinimum(self, value):
                self.slider.setMinimum(value)
                self.scrollBar.setMinimum(value)
                self.dial.setMinimum(value)

            def setMaximum(self, value):
                self.slider.setMaximum(value)
                self.scrollBar.setMaximum(value)
                self.dial.setMaximum(value)

            def invertAppearance(self, invert):
                self.slider.setInvertedAppearance(invert)
                self.scrollBar.setInvertedAppearance(invert)
                self.dial.setInvertedAppearance(invert)

            def invertKeyBindings(self, invert):
                self.slider.setInvertedControls(invert)
                self.scrollBar.setInvertedControls(invert)
                self.dial.setInvertedControls(invert)

        class Window(QWidget):
            def __init__(self):
                super(Window, self).__init__()

                self.horizontalSliders = SlidersGroup(Qt.Horizontal,
                                                      "Horizontal")
                self.verticalSliders = SlidersGroup(Qt.Vertical, "Vertical")

                self.stackedWidget = QStackedWidget()
                self.stackedWidget.addWidget(self.horizontalSliders)
                self.stackedWidget.addWidget(self.verticalSliders)

                self.createControls("Controls")

                self.horizontalSliders.valueChanged[int].connect(self.verticalSliders.setValue)
                self.verticalSliders.valueChanged[int].connect(self.valueSpinBox.setValue)
                self.valueSpinBox.valueChanged[int].connect(self.horizontalSliders.setValue)

                layout = QHBoxLayout()
                layout.addWidget(self.controlsGroup)
                layout.addWidget(self.stackedWidget)
                self.setLayout(layout)

                self.minimumSpinBox.setValue(0)
                self.maximumSpinBox.setValue(20)
                self.valueSpinBox.setValue(5)

                self.setWindowTitle("Sliders")

            def createControls(self, title):
                self.controlsGroup = QGroupBox(title)

                minimumLabel = QLabel("Minimum value:")
                maximumLabel = QLabel("Maximum value:")
                valueLabel = QLabel("Current value:")

                invertedAppearance = QCheckBox("Inverted appearance")
                invertedKeyBindings = QCheckBox("Inverted key bindings")

                self.minimumSpinBox = QSpinBox()
                self.minimumSpinBox.setRange(-100, 100)
                self.minimumSpinBox.setSingleStep(1)

                self.maximumSpinBox = QSpinBox()
                self.maximumSpinBox.setRange(-100, 100)
                self.maximumSpinBox.setSingleStep(1)

                self.valueSpinBox = QSpinBox()
                self.valueSpinBox.setRange(-100, 100)
                self.valueSpinBox.setSingleStep(1)

                orientationCombo = QComboBox()
                orientationCombo.addItem("Horizontal slider-like widgets")
                orientationCombo.addItem("Vertical slider-like widgets")

                orientationCombo.activated[int].connect(self.stackedWidget.setCurrentIndex)
                self.minimumSpinBox.valueChanged[int].connect(self.horizontalSliders.setMinimum)
                self.minimumSpinBox.valueChanged[int].connect(self.verticalSliders.setMinimum)
                self.maximumSpinBox.valueChanged[int].connect(self.horizontalSliders.setMaximum)
                self.maximumSpinBox.valueChanged[int].connect(self.verticalSliders.setMaximum)
                invertedAppearance.toggled.connect(self.horizontalSliders.invertAppearance)
                invertedAppearance.toggled.connect(self.verticalSliders.invertAppearance)
                invertedKeyBindings.toggled.connect(self.horizontalSliders.invertKeyBindings)
                invertedKeyBindings.toggled.connect(self.verticalSliders.invertKeyBindings)

                controlsLayout = QGridLayout()
                controlsLayout.addWidget(minimumLabel, 0, 0)
                controlsLayout.addWidget(maximumLabel, 1, 0)
                controlsLayout.addWidget(valueLabel, 2, 0)
                controlsLayout.addWidget(self.minimumSpinBox, 0, 1)
                controlsLayout.addWidget(self.maximumSpinBox, 1, 1)
                controlsLayout.addWidget(self.valueSpinBox, 2, 1)
                controlsLayout.addWidget(invertedAppearance, 0, 2)
                controlsLayout.addWidget(invertedKeyBindings, 1, 2)
                controlsLayout.addWidget(orientationCombo, 3, 0, 1, 3)
                self.controlsGroup.setLayout(controlsLayout)

        # app = QApplication(sys.argv)
        form = Window()
        form.show()
        # sys.exit(app.exec_())
        app.exec_()

    if info['name'] == 'screenshot':
        __appname__ = "Screenshot"

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

    if info['name'] == 'easing':
        # import easing_rc
        from ui_form import Ui_Form
        __appname__ = "Easing"

        class Animation(QPropertyAnimation):
            LinearPath, CirclePath = range(2)

            def __init__(self, target, prop):
                super(Animation, self).__init__(target, prop)
                self.setPathType(Animation.LinearPath)

            def setPathType(self, pathType):
                self.m_pathType = pathType
                self.m_path = QPainterPath()

            def updateCurrentTime(self, currentTime):
                if self.m_pathType == Animation.CirclePath:
                    if self.m_path.isEmpty():
                        end = self.endValue()
                        start = self.startValue()
                        self.m_path.moveTo(start)
                        self.m_path.addEllipse(QRectF(start, end))

                    dura = self.duration()
                    if dura == 0:
                        progress = 1.0
                    else:
                        progress = (((currentTime - 1) % dura) + 1) / float(dura)

                    easedProgress = self.easingCurve().valueForProgress(progress)
                    if easedProgress > 1.0:
                        easedProgress -= 1.0
                    elif easedProgress < 0:
                        easedProgress += 1.0

                    pt = self.m_path.pointAtPercent(easedProgress)
                    self.updateCurrentValue(pt)
                    self.valueChanged.emit(pt)
                else:
                    super(Animation, self).updateCurrentTime(currentTime)

        # PyQt doesn't support deriving from more than one wrapped class so we use
        # composition and delegate the property.

        class Pixmap(QObject):
            def __init__(self, pix):
                super(Pixmap, self).__init__()

                self.pixmap_item = QGraphicsPixmapItem(pix)
                self.pixmap_item.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

            def set_pos(self, pos):
                self.pixmap_item.setPos(pos)

            def get_pos(self):
                return self.pixmap_item.pos()

            pos = Property(QPointF, get_pos, set_pos)

        class Window(QWidget):
            def __init__(self, parent=None):
                super(Window, self).__init__(parent)

                self.m_iconSize = QSize(64, 64)
                self.m_scene = QGraphicsScene()

                m_ui = Ui_Form()
                m_ui.setupUi(self)
                m_ui.easingCurvePicker.setIconSize(self.m_iconSize)
                m_ui.easingCurvePicker.setMinimumHeight(self.m_iconSize.height() + 50)
                m_ui.buttonGroup.setId(m_ui.lineRadio, 0)
                m_ui.buttonGroup.setId(m_ui.circleRadio, 1)

                dummy = QEasingCurve()
                m_ui.periodSpinBox.setValue(dummy.period())
                m_ui.amplitudeSpinBox.setValue(dummy.amplitude())
                m_ui.overshootSpinBox.setValue(dummy.overshoot())

                m_ui.easingCurvePicker.currentRowChanged.connect(self.curveChanged)
                m_ui.buttonGroup.buttonClicked[int].connect(self.pathChanged)
                m_ui.periodSpinBox.valueChanged.connect(self.periodChanged)
                m_ui.amplitudeSpinBox.valueChanged.connect(self.amplitudeChanged)
                m_ui.overshootSpinBox.valueChanged.connect(self.overshootChanged)

                self.m_ui = m_ui
                self.createCurveIcons()

                pix = QPixmap(':/images/qt-logo.png')
                self.m_item = Pixmap(pix)
                self.m_scene.addItem(self.m_item.pixmap_item)
                self.m_ui.graphicsView.setScene(self.m_scene)

                self.m_anim = Animation(self.m_item, 'pos')
                self.m_anim.setEasingCurve(QEasingCurve.OutBounce)
                self.m_ui.easingCurvePicker.setCurrentRow(int(QEasingCurve.OutBounce))

                self.startAnimation()

            def createCurveIcons(self):
                pix = QPixmap(self.m_iconSize)
                painter = QPainter()

                gradient = QLinearGradient(0, 0, 0, self.m_iconSize.height())
                gradient.setColorAt(0.0, QColor(240, 240, 240))
                gradient.setColorAt(1.0, QColor(224, 224, 224))

                brush = QBrush(gradient)

                # The original C++ code uses undocumented calls to get the names of the
                # different curve types.  We do the Python equivalant (but without
                # cheating)
                curve_types = [(n, c) for n, c in QEasingCurve.__dict__.items()
                               if isinstance(c, QEasingCurve.Type)
                               and c != QEasingCurve.Custom
                               and c != QEasingCurve.NCurveTypes]
                curve_types.sort(key=lambda ct: ct[1])

                painter.begin(pix)

                for curve_name, curve_type in curve_types:
                    painter.fillRect(QRect(QPoint(0, 0), self.m_iconSize), brush)
                    curve = QEasingCurve(curve_type)

                    painter.setPen(QColor(0, 0, 255, 64))
                    xAxis = self.m_iconSize.height() / 1.5
                    yAxis = self.m_iconSize.width() / 3.0
                    painter.drawLine(0, xAxis, self.m_iconSize.width(), xAxis)
                    painter.drawLine(yAxis, 0, yAxis, self.m_iconSize.height())

                    curveScale = self.m_iconSize.height() / 2.0

                    painter.setPen(Qt.NoPen)

                    # Start point.
                    painter.setBrush(Qt.red)
                    start = QPoint(yAxis,
                                   xAxis - curveScale * curve.valueForProgress(0))
                    painter.drawRect(start.x() - 1, start.y() - 1, 3, 3)

                    # End point.
                    painter.setBrush(Qt.blue)
                    end = QPoint(yAxis + curveScale,
                                 xAxis - curveScale * curve.valueForProgress(1))
                    painter.drawRect(end.x() - 1, end.y() - 1, 3, 3)

                    curvePath = QPainterPath()
                    curvePath.moveTo(QPointF(start))
                    t = 0.0
                    while t <= 1.0:
                        to = QPointF(yAxis + curveScale * t,
                                     xAxis - curveScale * curve.valueForProgress(t))
                        curvePath.lineTo(to)
                        t += 1.0 / curveScale

                    painter.setRenderHint(QPainter.Antialiasing, True)
                    painter.strokePath(curvePath, QColor(32, 32, 32))
                    painter.setRenderHint(QPainter.Antialiasing, False)

                    item = QListWidgetItem()
                    item.setIcon(QIcon(pix))
                    item.setText(curve_name)
                    self.m_ui.easingCurvePicker.addItem(item)

                painter.end()

            def startAnimation(self):
                self.m_anim.setStartValue(QPointF(0, 0))
                self.m_anim.setEndValue(QPointF(100, 100))
                self.m_anim.setDuration(2000)
                self.m_anim.setLoopCount(-1)
                self.m_anim.start()

            def curveChanged(self, row):
                curveType = QEasingCurve.Type(row)
                self.m_anim.setEasingCurve(curveType)
                self.m_anim.setCurrentTime(0)

                isElastic = (curveType >= QEasingCurve.InElastic and curveType <= QEasingCurve.OutInElastic)
                isBounce = (curveType >= QEasingCurve.InBounce and curveType <= QEasingCurve.OutInBounce)

                self.m_ui.periodSpinBox.setEnabled(isElastic)
                self.m_ui.amplitudeSpinBox.setEnabled(isElastic or isBounce)
                self.m_ui.overshootSpinBox.setEnabled(curveType >= QEasingCurve.InBack and curveType <= QEasingCurve.OutInBack)

            def pathChanged(self, index):
                self.m_anim.setPathType(index)

            def periodChanged(self, value):
                curve = self.m_anim.easingCurve()
                curve.setPeriod(value)
                self.m_anim.setEasingCurve(curve)

            def amplitudeChanged(self, value):
                curve = self.m_anim.easingCurve()
                curve.setAmplitude(value)
                self.m_anim.setEasingCurve(curve)

            def overshootChanged(self, value):
                curve = self.m_anim.easingCurve()
                curve.setOvershoot(value)
                self.m_anim.setEasingCurve(curve)

        # if __name__ == '__main__':

        # app = QApplication(sys.argv)
        form = Window()
        form.resize(600, 600)
        form.show()
        # sys.exit(app.exec_())
        app.exec_()

    if info['name'] == 'line_edit':
        __appname__ = "Line Edit"

        class Window(QWidget):
            def __init__(self):
                super(Window, self).__init__()

                echoGroup = QGroupBox("Echo")

                echoLabel = QLabel("Mode:")
                echoComboBox = QComboBox()
                echoComboBox.addItem("Normal")
                echoComboBox.addItem("Password")
                echoComboBox.addItem("PasswordEchoOnEdit")
                echoComboBox.addItem("No Echo")

                self.echoLineEdit = QLineEdit()
                self.echoLineEdit.setFocus()

                validatorGroup = QGroupBox("Validator")

                validatorLabel = QLabel("Type:")
                validatorComboBox = QComboBox()
                validatorComboBox.addItem("No validator")
                validatorComboBox.addItem("Integer validator")
                validatorComboBox.addItem("Double validator")

                self.validatorLineEdit = QLineEdit()

                alignmentGroup = QGroupBox("Alignment")

                alignmentLabel = QLabel("Type:")
                alignmentComboBox = QComboBox()
                alignmentComboBox.addItem("Left")
                alignmentComboBox.addItem("Centered")
                alignmentComboBox.addItem("Right")

                self.alignmentLineEdit = QLineEdit()

                inputMaskGroup = QGroupBox("Input mask")

                inputMaskLabel = QLabel("Type:")
                inputMaskComboBox = QComboBox()
                inputMaskComboBox.addItem("No mask")
                inputMaskComboBox.addItem("Phone number")
                inputMaskComboBox.addItem("ISO date")
                inputMaskComboBox.addItem("License key")

                self.inputMaskLineEdit = QLineEdit()

                accessGroup = QGroupBox("Access")

                accessLabel = QLabel("Read-only:")
                accessComboBox = QComboBox()
                accessComboBox.addItem("False")
                accessComboBox.addItem("True")

                self.accessLineEdit = QLineEdit()

                echoComboBox.activated[int].connect(self.echoChanged)
                validatorComboBox.activated[int].connect(self.validatorChanged)
                alignmentComboBox.activated[int].connect(self.alignmentChanged)
                inputMaskComboBox.activated[int].connect(self.inputMaskChanged)
                accessComboBox.activated[int].connect(self.accessChanged)

                echoLayout = QGridLayout()
                echoLayout.addWidget(echoLabel, 0, 0)
                echoLayout.addWidget(echoComboBox, 0, 1)
                echoLayout.addWidget(self.echoLineEdit, 1, 0, 1, 2)
                echoGroup.setLayout(echoLayout)

                validatorLayout = QGridLayout()
                validatorLayout.addWidget(validatorLabel, 0, 0)
                validatorLayout.addWidget(validatorComboBox, 0, 1)
                validatorLayout.addWidget(self.validatorLineEdit, 1, 0, 1, 2)
                validatorGroup.setLayout(validatorLayout)

                alignmentLayout = QGridLayout()
                alignmentLayout.addWidget(alignmentLabel, 0, 0)
                alignmentLayout.addWidget(alignmentComboBox, 0, 1)
                alignmentLayout.addWidget(self.alignmentLineEdit, 1, 0, 1, 2)
                alignmentGroup. setLayout(alignmentLayout)

                inputMaskLayout = QGridLayout()
                inputMaskLayout.addWidget(inputMaskLabel, 0, 0)
                inputMaskLayout.addWidget(inputMaskComboBox, 0, 1)
                inputMaskLayout.addWidget(self.inputMaskLineEdit, 1, 0, 1, 2)
                inputMaskGroup.setLayout(inputMaskLayout)

                accessLayout = QGridLayout()
                accessLayout.addWidget(accessLabel, 0, 0)
                accessLayout.addWidget(accessComboBox, 0, 1)
                accessLayout.addWidget(self.accessLineEdit, 1, 0, 1, 2)
                accessGroup.setLayout(accessLayout)

                layout = QGridLayout()
                layout.addWidget(echoGroup, 0, 0)
                layout.addWidget(validatorGroup, 1, 0)
                layout.addWidget(alignmentGroup, 2, 0)
                layout.addWidget(inputMaskGroup, 0, 1)
                layout.addWidget(accessGroup, 1, 1)
                self.setLayout(layout)

                self.setWindowTitle("Line Edits")

            def echoChanged(self, index):
                if index == 0:
                    self.echoLineEdit.setEchoMode(QLineEdit.Normal)
                elif index == 1:
                    self.echoLineEdit.setEchoMode(QLineEdit.Password)
                elif index == 2:
                    self.echoLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
                elif index == 3:
                    self.echoLineEdit.setEchoMode(QLineEdit.NoEcho)

            def validatorChanged(self, index):
                if index == 0:
                    self.validatorLineEdit.setValidator(None)
                elif index == 1:
                    self.validatorLineEdit.setValidator(QIntValidator(self.validatorLineEdit))
                elif index == 2:
                    self.validatorLineEdit.setValidator(QDoubleValidator(-999.0, 999.0, 2, self.validatorLineEdit))

                self.validatorLineEdit.clear()

            def alignmentChanged(self, index):
                if index == 0:
                    self.alignmentLineEdit.setAlignment(Qt.AlignLeft)
                elif index == 1:
                    self.alignmentLineEdit.setAlignment(Qt.AlignCenter)
                elif index == 2:
                    self.alignmentLineEdit.setAlignment(Qt.AlignRight)

            def inputMaskChanged(self, index):
                if index == 0:
                    self.inputMaskLineEdit.setInputMask('')
                elif index == 1:
                    self.inputMaskLineEdit.setInputMask('+99 99 99 99 99;_')
                elif index == 2:
                    self.inputMaskLineEdit.setInputMask('0000-00-00')
                    self.inputMaskLineEdit.setText('00000000')
                    self.inputMaskLineEdit.setCursorPosition(0)
                elif index == 3:
                    self.inputMaskLineEdit.setInputMask('>AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#')

            def accessChanged(self, index):
                if index == 0:
                    self.accessLineEdit.setReadOnly(False)
                elif index == 1:
                    self.accessLineEdit.setReadOnly(True)

        # if __name__ == '__main__':

        # app = QApplication(sys.argv)
        form = Window()
        form.show()
        # sys.exit(app.exec_())
        app.exec_()

    if info['name'] == 'groupbox':
        __appname__ = "Groupbox"

        class Window(QWidget):
            def __init__(self, parent=None):
                super(Window, self).__init__(parent)

                grid = QGridLayout()
                grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
                grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
                grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
                grid.addWidget(self.createPushButtonGroup(), 1, 1)
                self.setLayout(grid)

                self.setWindowTitle("Group Box")
                self.resize(480, 320)

            def createFirstExclusiveGroup(self):
                groupBox = QGroupBox("Exclusive Radio Buttons")

                radio1 = QRadioButton("&Radio button 1")
                radio2 = QRadioButton("R&adio button 2")
                radio3 = QRadioButton("Ra&dio button 3")

                radio1.setChecked(True)

                vbox = QVBoxLayout()
                vbox.addWidget(radio1)
                vbox.addWidget(radio2)
                vbox.addWidget(radio3)
                vbox.addStretch(1)
                groupBox.setLayout(vbox)

                return groupBox

            def createSecondExclusiveGroup(self):
                groupBox = QGroupBox("E&xclusive Radio Buttons")
                groupBox.setCheckable(True)
                groupBox.setChecked(False)

                radio1 = QRadioButton("Rad&io button 1")
                radio2 = QRadioButton("Radi&o button 2")
                radio3 = QRadioButton("Radio &button 3")
                radio1.setChecked(True)
                checkBox = QCheckBox("Ind&ependent checkbox")
                checkBox.setChecked(True)

                vbox = QVBoxLayout()
                vbox.addWidget(radio1)
                vbox.addWidget(radio2)
                vbox.addWidget(radio3)
                vbox.addWidget(checkBox)
                vbox.addStretch(1)
                groupBox.setLayout(vbox)

                return groupBox

            def createNonExclusiveGroup(self):
                groupBox = QGroupBox("Non-Exclusive Checkboxes")
                groupBox.setFlat(True)

                checkBox1 = QCheckBox("&Checkbox 1")
                checkBox2 = QCheckBox("C&heckbox 2")
                checkBox2.setChecked(True)
                tristateBox = QCheckBox("Tri-&state button")
                tristateBox.setTristate(True)
                tristateBox.setCheckState(Qt.PartiallyChecked)

                vbox = QVBoxLayout()
                vbox.addWidget(checkBox1)
                vbox.addWidget(checkBox2)
                vbox.addWidget(tristateBox)
                vbox.addStretch(1)
                groupBox.setLayout(vbox)

                return groupBox

            def createPushButtonGroup(self):
                groupBox = QGroupBox("&Push Buttons")
                groupBox.setCheckable(True)
                groupBox.setChecked(True)

                pushButton = QPushButton("&Normal Button")
                toggleButton = QPushButton("&Toggle Button")
                toggleButton.setCheckable(True)
                toggleButton.setChecked(True)
                flatButton = QPushButton("&Flat Button")
                flatButton.setFlat(True)

                popupButton = QPushButton("Pop&up Button")
                menu = QMenu(self)
                menu.addAction("&First Item")
                menu.addAction("&Second Item")
                menu.addAction("&Third Item")
                menu.addAction("F&ourth Item")
                popupButton.setMenu(menu)

                newAction = menu.addAction("Submenu")
                subMenu = QMenu("Popup Submenu", self)
                subMenu.addAction("Item 1")
                subMenu.addAction("Item 2")
                subMenu.addAction("Item 3")
                newAction.setMenu(subMenu)

                vbox = QVBoxLayout()
                vbox.addWidget(pushButton)
                vbox.addWidget(toggleButton)
                vbox.addWidget(flatButton)
                vbox.addWidget(popupButton)
                vbox.addStretch(1)
                groupBox.setLayout(vbox)

                return groupBox

        #app = QApplication(sys.argv)
        form = Window()
        form.show()
        # sys.exit(app.exec_())
        app.exec_()

    if info['name'] == 'tab_dialog':
        __appname__ = "Tab Dialog"

        class TabDialog(QDialog):
            def __init__(self, fileName, parent=None):
                super(TabDialog, self).__init__(parent)

                fileInfo = QFileInfo(fileName)

                tabWidget = QTabWidget()
                tabWidget.addTab(GeneralTab(fileInfo), "General")
                tabWidget.addTab(PermissionsTab(fileInfo), "Permissions")
                tabWidget.addTab(ApplicationsTab(fileInfo), "Applications")

                buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

                buttonBox.accepted.connect(self.accept)
                buttonBox.rejected.connect(self.reject)

                mainLayout = QVBoxLayout()
                mainLayout.addWidget(tabWidget)
                mainLayout.addWidget(buttonBox)
                self.setLayout(mainLayout)

                self.setWindowTitle("Tab Dialog")

        class GeneralTab(QWidget):
            def __init__(self, fileInfo, parent=None):
                super(GeneralTab, self).__init__(parent)

                fileNameLabel = QLabel("File Name:")
                fileNameEdit = QLineEdit(fileInfo.fileName())

                pathLabel = QLabel("Path:")
                pathValueLabel = QLabel(fileInfo.absoluteFilePath())
                pathValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

                sizeLabel = QLabel("Size:")
                size = fileInfo.size() // 1024
                sizeValueLabel = QLabel("%d K" % size)
                sizeValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

                lastReadLabel = QLabel("Last Read:")
                lastReadValueLabel = QLabel(fileInfo.lastRead().toString())
                lastReadValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

                lastModLabel = QLabel("Last Modified:")
                lastModValueLabel = QLabel(fileInfo.lastModified().toString())
                lastModValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

                mainLayout = QVBoxLayout()
                mainLayout.addWidget(fileNameLabel)
                mainLayout.addWidget(fileNameEdit)
                mainLayout.addWidget(pathLabel)
                mainLayout.addWidget(pathValueLabel)
                mainLayout.addWidget(sizeLabel)
                mainLayout.addWidget(sizeValueLabel)
                mainLayout.addWidget(lastReadLabel)
                mainLayout.addWidget(lastReadValueLabel)
                mainLayout.addWidget(lastModLabel)
                mainLayout.addWidget(lastModValueLabel)
                mainLayout.addStretch(1)
                self.setLayout(mainLayout)

        class PermissionsTab(QWidget):
            def __init__(self, fileInfo, parent=None):
                super(PermissionsTab, self).__init__(parent)

                permissionsGroup = QGroupBox("Permissions")

                readable = QCheckBox("Readable")
                if fileInfo.isReadable():
                    readable.setChecked(True)

                writable = QCheckBox("Writable")
                if fileInfo.isWritable():
                    writable.setChecked(True)

                executable = QCheckBox("Executable")
                if fileInfo.isExecutable():
                    executable.setChecked(True)

                ownerGroup = QGroupBox("Ownership")

                ownerLabel = QLabel("Owner")
                ownerValueLabel = QLabel(fileInfo.owner())
                ownerValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

                groupLabel = QLabel("Group")
                groupValueLabel = QLabel(fileInfo.group())
                groupValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

                permissionsLayout = QVBoxLayout()
                permissionsLayout.addWidget(readable)
                permissionsLayout.addWidget(writable)
                permissionsLayout.addWidget(executable)
                permissionsGroup.setLayout(permissionsLayout)

                ownerLayout = QVBoxLayout()
                ownerLayout.addWidget(ownerLabel)
                ownerLayout.addWidget(ownerValueLabel)
                ownerLayout.addWidget(groupLabel)
                ownerLayout.addWidget(groupValueLabel)
                ownerGroup.setLayout(ownerLayout)

                mainLayout = QVBoxLayout()
                mainLayout.addWidget(permissionsGroup)
                mainLayout.addWidget(ownerGroup)
                mainLayout.addStretch(1)
                self.setLayout(mainLayout)

        class ApplicationsTab(QWidget):
            def __init__(self, fileInfo, parent=None):
                super(ApplicationsTab, self).__init__(parent)

                topLabel = QLabel("Open with:")

                applicationsListBox = QListWidget()
                applications = []

                for i in range(1, 31):
                    applications.append("Application %d" % i)

                applicationsListBox.insertItems(0, applications)

                alwaysCheckBox = QCheckBox()

                if fileInfo.suffix():
                    alwaysCheckBox = QCheckBox("Always use this application to "
                                               "open files with the extension '%s'" % fileInfo.suffix())
                else:
                    alwaysCheckBox = QCheckBox("Always use this application to "
                                               "open this type of file")

                layout = QVBoxLayout()
                layout.addWidget(topLabel)
                layout.addWidget(applicationsListBox)
                layout.addWidget(alwaysCheckBox)
                self.setLayout(layout)

        # app = QApplication(sys.argv)

        # if len(sys.argv) >= 2:
        #    fileName = sys.argv[1]
        # else:
        fileName = "hop hop hop! Original sys.argv[1] line commented out, look at the code in CustomUIAction_Apps, line 1443."

        tabdialog = TabDialog(fileName)
        # sys.exit(tabdialog.exec_())
        tabdialog.show()
        app.exec_()

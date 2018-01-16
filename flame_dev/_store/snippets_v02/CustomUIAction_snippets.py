##################################

# Stefan Gaillot
# Venice, CA 90291
# 2017/10/20

# A huge thank you and many credits to Vlad Bakic for his treamendous help, regarding logic, code, and friendly support.
# Also many thamks to Tommy Furukawa, Tommy Hooper and Sean Farrell (for the same reasons)

#### LICENCING ####
# let's be a bit formaly protective there (legal form), but still giving options to poke around and re-use/modify any part ... hmmm.

##################################

# 'mvr' stands for 'maya Vray'
# 'btb' stands for 'back to beauty' > rebuilt a CG beauty pass from render passes.

from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtCore, QtGui
import sys
import subprocess

# Modules Paths
sys.path.append('/Users/stefan/XenDrive/___VFX/DEV/PYTHON/Modules')
sys.path.append('/opt/flame_dev/_python/modules')


# UIs
from Snippets_toolbar_UI import Snippets_toolbar
from input_dialog import InputDialogBox

# Snippets
from snippets.connected_duplicate_02a import main as _dupli
from snippets.matte_cleaner_01a import main as _cleaner
import snippets.mvr_back_to_beauty as _backtobeauty
from snippets.test_print2 import my_test_print as _testprint


# Contextuel Menu Entry
def getCustomUIActions():

    action2 = {}
    action2["name"] = "snippets_v2"
    action2["caption"] = "Snippets"

    appGroup2 = {}
    appGroup2["name"] = "snippets v2"
    appGroup2["actions"] = (action2,)

    return (appGroup2,)


def customUIAction(info, userData):
    if info['name'] == 'snippets_v2':

        def user_input_builds_btb():
            dialog = InputDialogBox()

            if dialog.exec_():
                shot_text = str(dialog.shotName.text())
                elt_text = str(dialog.elementName.text())

                print shot_text, elt_text
                _backtobeauty.main(shot_text, elt_text)

        add_snippets_dict = [
            {'widget_type': 'button', 'label': "open text", 'icon': ':/icons/snippet02-icon.png', 'callback': _testprint},
            {'widget_type': 'button', 'label': "Back to Beauty", 'icon': ':/icons/snippet02-icon.png', 'callback': user_input_builds_btb},
            {'widget_type': 'button', 'label': "Duplicate", 'icon': ':/icons/snippet02-icon.png', 'callback': _dupli},
            {'widget_type': 'button', 'label': "Matte Cleaner", 'icon': ':/icons/snippet02-icon.png', 'callback': _cleaner}
        ]

#############################################

        #app = QApplication(sys.argv)
        app = QApplication.activePopupWidget()
        form = Snippets_toolbar()
        form.create_ui(add_snippets_dict)
        form.show()
        app.exec_()

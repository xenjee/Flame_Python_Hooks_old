
# (c) Stefan Gaillot
# Venice, CA 90291
# 2017/11/03

from PySide.QtGui import QApplication
import sys
import yaml

# UI
import save_Load_selections_UI_04b
reload(save_Load_selections_UI_04b)
from save_Load_selections_UI_04b import SelectionsWidget

# Modules Paths
sys.path.append('/Users/stefan/XenDrive/___VFX/DEV/PYTHON/Modules')
sys.path.append('/opt/flame_dev/_python/modules')


# Contextuel Menu Entry
def getCustomUIActions():

    action1 = {}
    action1["name"] = "nodes_selection"
    action1["caption"] = "v01"

    appGroup1 = {}
    appGroup1["name"] = "Selections"
    appGroup1["actions"] = (action1,)

    return (appGroup1,)


def customUIAction(info, userData):
    if info['name'] == 'nodes_selection':
        import flame

        def get_selection():
            import flame
            return ["" + s.name + "" for s in flame.batch.selected_nodes.get_value()]

        yamlpath = '/opt/flame_dev/_python/hooks_py_apps/save_selections/saved_nodes.yaml'

    #############################################

        app = QApplication.activePopupWidget()
        # we call 'save_Load_selections_UI_04b.py' giving it 2 args:
        # -> the path to the yaml file and the selected nodes list
        form = SelectionsWidget(path=yamlpath, fromFlame=get_selection)
        form.show()
        app.exec_()

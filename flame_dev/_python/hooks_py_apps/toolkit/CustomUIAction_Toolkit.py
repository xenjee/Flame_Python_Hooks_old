import os
import subprocess as sb

# inherit absolute part of the path from the __init__.py file
from __init__ import get_absolute_path_part
ROOT_PATH = get_absolute_path_part()


def getCustomUIActions():

    action01 = {}
    action01["name"] = "search"
    action01["caption"] = "Search"

    action02 = {}
    action02["name"] = "expressions1"
    action02["caption"] = "Expressions_Cheatsheet1"

    appGroup1 = {}
    appGroup1["name"] = "Toolkit"
    appGroup1["actions"] = (action01, action02,)

    return (appGroup1,)


def customUIAction(info, userData):

    if info['name'] == 'search':
        print "-" * 20
        print ' action: search'
        print "-" * 20

    if info['name'] == 'expressions1':
        print "-" * 20
        print 'expressions1'
        print "-" * 20

        # def expressions_sheet1():

        #file_path = '/opt/flame_dev/_python/hooks_py_apps/toolkit/docs/Expressions_particles_reformated.txt'
        file_path = "{root}/_python/hooks_py_apps/toolkit/docs/Expressions_particles_reformated.txt".format(root=ROOT_PATH)
        print file_path
        print "-" * 20
        sb.call(["open", file_path])


print '- End of customUIAction Toolkit:'
print '-' * 80

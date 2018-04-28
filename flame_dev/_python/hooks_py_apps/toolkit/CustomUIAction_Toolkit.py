import os
import subprocess as sb
import sys

# turn the relative __file__ value into it's full path
absolute_path = os.path.realpath(__file__)
# Use the os module to split the filepath using '/' as a seperator to creates a list from which we pick IDs []
root_path = '/'.join(absolute_path.split('/')[0:-4])

print "root_path: ", root_path


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
        file_path = "{root}/_python/hooks_py_apps/toolkit/docs/Expressions_particles_reformated.txt".format(root=root_path)
        print file_path
        print "-" * 20
        sb.call(["open", file_path])


print '- End of customUIAction Toolkit:'
print '-' * 80

#!/bin/env python
#******************************************************************************
#
# Filename: hook_lewis.py


def getCustomUIActions():

    pathcopyaction = dict(name='pathcopy', caption='Copy to clipboard')
    pathcopygrp = dict(name='Clip path', actions=(pathcopyaction,))
    return (pathcopygrp,)


def customUIAction(info, userData):
    if info['name'] == 'pathcopy':
        print '-' * 20 + "hook_lewis" + '-' * 20

        import re
        import os
        import PySide.QtGui as qtg
        from adsk import libwiretapPythonClientAPI as wt

        qa = qtg.QApplication.instance()
        paths = []

        wt.WireTapClientInit()
        wtserver = wt.WireTapServerHandle('localhost')
        wtmeta = wt.WireTapStr()
        for wtid in info['selection']:
            wtclip = wt.WireTapNodeHandle(wtserver, wtid)
            wtclip.getMetaData('EDL', '', 1, wtmeta)
            wtedl = wtmeta.c_str()
            for line in wtedl.splitlines():
                if 'ORIGIN' in line and re.match('^DLEDL: EDIT:[0-9]+ ORIGIN: .+$', line):
                    path = line.split(':')[3][1:]
                    paths.append(path)
        pathstogether = '\n'.join(paths)
        print "Copying to clipboard: " + pathstogether
        qa.clipboard().setText(pathstogether)

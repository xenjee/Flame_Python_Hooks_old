#!/usr/bin/env python
#!/opt/Autodesk/python/2018.3/bin/python2.7

# *****************************************************************************
##
# File         listAllServers.py
##
# Description   WireTap SDK python sample program to list all WireTap servers.
##
# Copyright (c) 2016 Autodesk, Inc.
# All rights reserved.
##
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
##
# *****************************************************************************

# *****************************************************************************


class WireTapException(Exception):
  pass


# *****************************************************************************
def main():

  # Initialize the Wiretap Client API.
  #
  wireTapClient = WireTapClient()
  if not wireTapClient.init():
    raise WireTapException("Unable to initialize WireTap client API.")

  listAllServers()


# *****************************************************************************
def listAllServers():

  # Obtain the list of Wiretap servers.
  #
  list = WireTapServerList()
  count = WireTapInt()
  if not list.getNumNodes(count):
    raise WireTapException("Error acquiring server list: %s." % list.lastError())

  print "Server                IP address  Storage Id     Protocol"
  print "---------------------------------------------------------"

  # Obtain information about each server.
  #
  i = 0
  while i < count:
    info = WireTapServerInfo()
    if not list.getNode(i, info):
      raise WireTapException("Error accessing server %d: %s." % (i, list.lastError()))

    print "%-16s %15s  %-16s %d.%d" % (info.getDisplayName(),
                                       info.getHostname(),
                                       info.getStorageId(),
                                       info.getVersionMajor(),
                                       info.getVersionMinor())

    i = i + 1
    pass


# *****************************************************************************
if __name__ == '__main__':
  import sys
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  import string
  from libwiretapPythonClientAPI import *

  main()

#!/usr/bin/env python

# *****************************************************************************
##
# File         resolvesStorageId.py
##
# Description   WireTap SDK python sample program to resolve a storage ID into
# a WireTap server.
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
def main(argv):

  # check the command line options for correctness
  try:
    opts, args = getopt.getopt(argv, "s:")
  except getopt.GetoptError:
    print "Usage:\n" \
          "-s <storage Id>\n"
    sys.exit(2)

  # default host name
  hostName = "localhost"

  # parse command line option to set specified host name
  # and node ID
  for opt, arg in opts:
    if opt == '-s':
      hostName = arg

  # storageId should be set to the ID of a storage device on the Wiretap
  # network.
  storageId = argv[1]

  # Initialize the Wiretap Client API.
  #
  wireTapClient = WireTapClient()
  if not wireTapClient.init():
    raise WireTapException("Unable to initialize WireTap client API.")

  resolveStorageId(hostName, storageId)


# *****************************************************************************
def resolveStorageId(hostName, storageId):

  # Resolve the given storage ID to determine to which Wiretap server the
  # storage device is connected
  #
  list = WireTapServerList()
  server = WireTapServerId()
  serverInfo = WireTapServerInfo()

  server.setStorageId(storageId)
  if not list.resolve(server, serverInfo):
    raise WireTapException("Unable to resolve '%s' into a server ID: %s."
                           % (storageId, list.lastError()))

  # Obtain IP address of the Wiretap server
  #
  print "Successfuly resolved storage ID '%s' into server '%s'." \
      % (storageId, server.getIPAddr())

  print "Server display name : '%s'." % serverInfo.getDisplayName()


# *****************************************************************************
if __name__ == '__main__':
  import sys
  import getopt
  import string
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  from libwiretapPythonClientAPI import *
  main(sys.argv[1:])

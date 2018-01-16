#!/usr/bin/env python

# *****************************************************************************
##
# File         duplicateNode.py
##
# Description   WireTap SDK sample python program to duplicate a node.
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
    opts, args = getopt.getopt(argv, "h:n:p:d:")
  except getopt.GetoptError:
    print "Usage:\n" \
          "-h <hostname>\n" \
          "-n <source node Id>" \
          "-p <destination node Id>" \
          "-d <display name>"
    sys.exit(2)

  # default host name
  hostName = "localhost"
  nodeId = ""
  parentNodeId = ""
  displayName = ""

  # parse command line option to set specified host name
  # and node ID
  for opt, arg in opts:
    if opt == '-h':
      hostName = arg
    elif opt == '-n':
      nodeId = arg
    elif opt == '-p':
      parentNodeId = arg
    elif opt == '-d':
      displayName = arg

  # Initialize the Wiretap Client API.
  #
  wireTapClient = WireTapClient()
  if not wireTapClient.init():
    raise WireTapException("Unable to initialize WireTap client API.")

  duplicateNode(hostName, nodeId, parentNodeId, displayName)


# *****************************************************************************
def duplicateNode(hostName, nodeId, parentNodeId, displayName):

  # Instantiate an IFFFS server handle.
  #
  ifffsServerId = WireTapServerId("IFFFS", hostName)
  ifffsServer = WireTapServerHandle(ifffsServerId)

  # Instantiate the source node handle for the given server and node ID.
  #
  sourceNode = WireTapNodeHandle(ifffsServer, nodeId)

  if len(displayName) == 0:
    sourceDisplayName = WireTapStr()
    if not sourceNode.getDisplayName(sourceDisplayName):
      raise WireTapException("Unable to obtain source node display name: %s" % sourceNode.lastError())
    displayName = "Duplicate of " + sourceDisplayName.c_str()

  # Instantiate the destination node handle for the given server and node ID.
  #
  parentNode = WireTapNodeHandle(ifffsServer, parentNodeId)

  newNode = WireTapNodeHandle()
  if not parentNode.duplicateNode(sourceNode, displayName, newNode):
    raise WireTapException("Unable to duplicate node: %s" % parentNode.lastError())

  print("Duplicated '%s' to '%s'" % (sourceNode.getNodeId().id(), newNode.getNodeId().id()))


# *****************************************************************************
if __name__ == '__main__':
  import sys
  import getopt
  import string
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  from libwiretapPythonClientAPI import *
  main(sys.argv[1:])

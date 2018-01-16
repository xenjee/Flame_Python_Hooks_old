#!/usr/bin/env python

# *****************************************************************************
##
# File         listChildren.py
##
# Description   WireTap SDK sample python program to list all child nodes of a
# specified node on a server.
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
    opts, args = getopt.getopt(argv, "h:n:")
  except getopt.GetoptError:
    print "Usage:\n" \
          "-h <hostname>\n" \
          "-n <node Id>"
    sys.exit(2)

  # default host name
  hostName = "localhost"
  nodeId = ""

  # parse command line option to set specified host name
  # and node ID
  for opt, arg in opts:
    if opt == '-h':
      hostName = arg
    elif opt == '-n':
      nodeId = arg

  # Initialize the Wiretap Client API.
  #
  wireTapClient = WireTapClient()
  if not wireTapClient.init():
    raise WireTapException("Unable to initialize WireTap client API.")

  listChildren(hostName, nodeId)


# *****************************************************************************
def listChildren(hostName, nodeId):

  # Instantiate a server handle
  #
  server = WireTapServerHandle(hostName)

  # Obtain the root node of the server.
  #
  parent = WireTapNodeHandle(server, nodeId)

  # Iterate across the first level of children.
  #
  child = WireTapNodeHandle()
  numChildren = WireTapInt(0)
  if not parent.getNumChildren(numChildren):
    raise WireTapException('Unable to obtain number of children: %s.' % parent.lastError())

  i = 0
  while i < numChildren:
    # Get the child node.
    #
    parent.getChild(i, child)

    # Get the node's display name and type.
    #
    name = WireTapStr()
    typeStr = WireTapStr()
    if not child.getDisplayName(name):
      raise WireTapException('Unable to obtain node name: %s.' % child.lastError())

    if not child.getNodeTypeStr(typeStr):
      raise WireTapException('Unable to obtain node type: %s.' % child.lastError())

    # Print the node info.
    #
    print "Node: '%s' type: %s" % (name.c_str(), typeStr.c_str())

    i = i + 1


# *****************************************************************************
if __name__ == '__main__':
  import sys
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  import getopt
  import string
  from libwiretapPythonClientAPI import *
  main(sys.argv[1:])

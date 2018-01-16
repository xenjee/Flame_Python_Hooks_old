#!/usr/bin/env python

# *****************************************************************************
##
# File         createOpenClips.py
##
# Description   WireTap SDK sample python program to import all clip node in a
# directory to a specified node on a server.
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
    opts, args = getopt.getopt(argv, "h:n:d:")
  except getopt.GetoptError:
    print "Usage:\n" \
          "-h <hostname>\n" \
          "-n <node Id>" \
          "-d <directory>"
    sys.exit(2)

  # default host name
  hostName = "localhost"
  parentNodeId = ""
  directory = ""

  # parse command line option to set specified host name
  # and node ID
  for opt, arg in opts:
    if opt == '-h':
      hostName = arg
    elif opt == '-n':
      parentNodeId = arg
    elif opt == '-d':
      directory = arg

  # Initialize the Wiretap Client API.
  #
  wireTapClient = WireTapClient()
  if not wireTapClient.init():
    raise WireTapException("Unable to initialize WireTap client API.")

  importOpenClips(hostName, parentNodeId, directory)


# *****************************************************************************
def importOpenClips(hostName, parentNodeId, directory):

  # Instantiate a gateway server handle.
  #
  gatewayServerId = WireTapServerId("Gateway", hostName)
  gatewayServer = WireTapServerHandle(gatewayServerId)

  # Instantiate a gateway directory node handle.
  #
  directoryNode = WireTapNodeHandle(gatewayServer, directory)

  # Instantiate an IFFFS server handle.
  #
  ifffsServerId = WireTapServerId("IFFFS", hostName)
  ifffsServer = WireTapServerHandle(ifffsServerId)

  # Instantiate a clip node handle for the given server and node ID.
  #
  parentNode = WireTapNodeHandle(ifffsServer, parentNodeId)

  # Loop thru all directory node children and import all clip nodes.
  #
  numChildren = WireTapInt(0)
  if not directoryNode.getNumChildren(numChildren):
    raise WireTapException("Unable to obtain number of children: %s" % directoryNode.lastError())

  for child in range(0, numChildren):
    # Get the child node.
    #
    childNode = WireTapNodeHandle()
    directoryNode.getChild(child, childNode)

    # Get the child node type
    #
    childType = WireTapStr()
    if not childNode.getNodeTypeStr(childType):
      raise WireTapException("Unable to obtain node type: %s" % childNode.lastError())

    # Ignore non clip children
    #
    if "CLIP" == childType.c_str():
      clipName = WireTapStr()
      if not childNode.getDisplayName(clipName):
        raise WireTapException("Unable to obtain node display name: %s" % childNode.lastError())

      sourceData = WireTapStr()
      if not childNode.getMetaData("SourceData",  # stream name
                                   "",            # filter
                                   0,             # depth
                                   sourceData):  # metadata
        raise WireTapException("Unable to obtain node source data: %s" % childNode.lastError())

      # Define a clip format. The parameter allow the server to determine the
      # source information to import.
      #
      format = WireTapClipFormat()
      format.setMetaDataTag("SourceData")
      format.setMetaData(sourceData.c_str())

      # Create a new node of type "CLIP" (a node type defined by
      # the IFFFS Wiretap Server).  Each Wiretap server defines a set of
      # node types (specified as string constants).
      #
      clipNode = WireTapNodeHandle()
      if not parentNode.createClipNode(clipName.c_str(),  # display name
                                       format,           # clip format
                                       "CLIP",           # node type (server-specific)
                                       clipNode):       # created node returned here
        raise WireTapException("Unable to create clip node: %s.", parentNode.lastError())

      print("Imported '%s' to '%s'" % (clipName, clipNode.getNodeId().id()))

  return 0



# *****************************************************************************
if __name__ == '__main__':
  import sys
  import getopt
  import string
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  from libwiretapPythonClientAPI import *
  main(sys.argv[1:])

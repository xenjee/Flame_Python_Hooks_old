#!/usr/bin/env python

# *****************************************************************************
##
# File         listFrames.py
##
# Description   WireTap SDK sample python program to list all frames IDs and
# frame paths in a clip.
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

  # default host name and node ID
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

  listFrames(hostName, nodeId)


# *****************************************************************************
def listFrames(hostName, nodeId):

  # Instantiate a server handle
  #
  server = WireTapServerHandle(hostName)

  # Instantiate the clip node handle for the given server and node ID.
  #
  clip = WireTapNodeHandle(server, nodeId)

  # Get the list of clip frames.
  #
  numFrames = WireTapInt(0)
  if not clip.getNumFrames(numFrames):
    raise WireTapException('Unable to obtain number of frames: %s.' % clip.lastError())

  # Read all frames ID and paths.
  #
  i = 0
  while i < numFrames:
    # A frame ID is an opaque string, unique to the server.
    #
    frameId = WireTapStr()
    if not clip.getFrameId(i, frameId):
      raise WireTapException('Unable to obtain frame ID %d: %s.' % (i, clip.lastError()))

    # Frame IDs have an optional path representation. If paths are available,
    # a Wiretap client can use them to access frames directly, instead of
    # calling readFrame(). The frame path will be an empty string if a path
    # representation of the frame ID does not exist.
    # If path translation services are enabled and configured,
    # the mount point of the current machine will be used
    # (for more info, see the Stone and Wire Filesystem and Networking Guide).
    #
    frameIdPath = WireTapStr()
    if not clip.getFrameIdPath(i, frameIdPath):
      raise WireTapException('Unable to obtain frame ID path %d: %s.' % (i, clip.lastError()))

    p = frameIdPath.c_str()
    p1 = p
    if (frameIdPath.length() == 0):
      p1 = "none"

    print "Frame %d. ID: '%s'  File Path: %s." % (i, frameId.c_str(), p1)

    i = i + 1


# *****************************************************************************
if __name__ == '__main__':
  import sys
  import getopt
  import string
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  from libwiretapPythonClientAPI import *
  main(sys.argv[1:])

#!/usr/bin/env python

# *****************************************************************************
##
# File         readFrames.py
##
# Description   WireTap SDK sample python program to read all frames of a clip.
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

  readFrames(hostName, nodeId)


# *****************************************************************************
def readFrames(hostName, nodeId):

  # Instantiate a server handle
  #
  server = WireTapServerHandle(hostName)

  # Instantiate the clip node handle for the given server and node ID.
  #
  clip = WireTapNodeHandle(server, nodeId)

  # Get the number of frames in the clip.
  #
  numFrames = WireTapInt()
  if not clip.getNumFrames(numFrames):
    raise WireTapException('Unable to obtain number of frames: %s.' % clip.lastError())

  # Get the clip format.  This is required to know how to interpret the frame
  # data, and to know how big the frame buffer must be.
  #
  format = WireTapClipFormat()
  if not clip.getClipFormat(format):
    raise WireTapException('Unable to obtain clip format: %s.' % clip.lastError())

  # Interpret the format tag (see WireTapTypes.h for a list of tags).
  #
  if (cmp(format.formatTag(), WireTapClipFormat.FORMAT_RGB()) == 0):
    print "This is an RGB clip."
  elif (cmp(format.formatTag(), WireTapClipFormat.FORMAT_YUV()) == 0):
    print "This is a YUV clip."
  else:
    print "Unknown clip format: %s." % format.formatTag()

  # buff is a buffer initialized to zero
  #
  buff = '0' * format.frameBufferSize()

  # Read all frames.
  #
  i = 0
  while i < numFrames:
    print "Reading frame %i." % i
    if not clip.readFrame(i, buff, format.frameBufferSize()):
      raise WireTapException('Unable to obtain read frame %i: %s.' % (i, clip.lastError()))
    # Print the frame info.
    #
    print "Successfully read frame %i." % i
    i = i + 1
    pass


# *****************************************************************************
if __name__ == '__main__':
  import sys
  import getopt
  import string
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  from libwiretapPythonClientAPI import *
  main(sys.argv[1:])

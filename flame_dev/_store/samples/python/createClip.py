#!/usr/bin/env python

# *****************************************************************************
##
# File    createClip.py
##
# Description   WireTap SDK sample python program to create a clip.
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

  createClip(hostName, nodeId)


# *****************************************************************************
def createClip(hostName, nodeId):

  # Instantiate a server handle
  #
  server = WireTapServerHandle(hostName)

  # Instantiate the clip node handle for the given server and node ID.
  #
  parent = WireTapNodeHandle(server, nodeId)

  # Define a clip format. The parameters allow the server to
  # determine the frame buffer size for the specified frame format
  # (in this example, an NTSC raw RGB frame). The buffer size calculated
  # by the server can be obtained after the clip has been created.
  #
  format = WireTapClipFormat(720, 486,      # width, height
                             3 * 8,             # bits per pixel
                             3,     # number of channels
                             29.97,   # frame rate
                             0.9,   # pixel ratio
                             WireTapClipFormat.ScanFormat.SCAN_FORMAT_FIELD_1_ODD,
                             WireTapClipFormat.FORMAT_RGB())

  # Create a new node of type "CLIP" (a node type defined by
  # the IFFFS Wiretap Server).  Each Wiretap server defines a set of
  # node types (specified as string constants).
  #
  clip = WireTapNodeHandle()
  if not parent.createClipNode("MyNewClip",  # display name
                               format,        # clip format
                               "CLIP",        # extended (server-specific) type
                               clip):       # created node returned here
    raise WireTapException('Unable to create clip node: %s.' % parent.lastError())

  # Set the number of frames.
  #
  numFrames = 5
  if not clip.setNumFrames(numFrames):
    raise WireTapException("Unable to set the number of frames: %s." % clip.lastError())

  # Get the clip format back from the clip node. Even though we defined the
  # format above, we must query the updated format to get the size of the
  # frame buffer calculated by the server.  The server will also fill in
  # any format metadata that was not specified (for example: timecode,
  # drop mode, and so on).
  #
  if not clip.getClipFormat(format):
    raise WireTapException("Unable to obtain clip format: %s." % clip.lastError())

  # buf is a buffer initialized to zero
  #
  buf = '0' * format.frameBufferSize()

  # Write the frames.
  #
  i = 0

  while i < numFrames:
    if not clip.writeFrame(i, buf, format.frameBufferSize()):
      raise WireTapException('Unable to obtain write frame %i: %s.' % i % clip.lastError())
    # Print the frame info.
    #
    print "Successfully wrote frame %i." % i
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

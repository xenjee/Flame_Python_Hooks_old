#!/usr/bin/env python

# *****************************************************************************
##
# File         reaadAudio.py
##
# Description WireTap SDK sample python program to read all samples of an
# audio clip.
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

  readAudio(hostName, nodeId)


# *****************************************************************************
def readAudio(hostName, nodeId):

  # Instantiate a server handle
  #
  server = WireTapServerHandle(hostName)

  # Instantiate the clip node handle for the given server and node ID.
  #
  clip = WireTapNodeHandle(server, nodeId)

  # Get the list of audio blocks.  Each frame is a block of samples.  The
  # server decides the size of the audio blocks.
  #
  numFrames = WireTapInt()
  if not clip.getNumFrames(numFrames):
    raise WireTapException('Unable to obtain number of frames: %s.' % clip.lastError())

  # Get the clip format.  This is required to know how to interpret the frame
  # data, and to know how big the frame buffer must be.
  #
  format = WireTapAudioFormat()
  if not clip.getClipFormat(format):
    raise WireTapException('Unable to obtain clip format: %s.' % clip.lastError())

  # Interpret the format tag (see WireTapTypes.h for a list of tags).
  #
  if (cmp(format.formatTag(), WireTapClipFormat.FORMAT_DL_AUDIO_FLOAT()) == 0):
    print "Audio clip contains floating point samples."
  elif (cmp(format.formatTag(), WireTapClipFormat.FORMAT_DL_AUDIO_INT24()) == 0):
    print "Audio clip contains 24 bit integer samples."
  else:
    print "Unsupported clip format: %s." % format.formatTag()

  # Audio samples are interlaced across channels.
  #
  print "Audio stream has %d channels." % format.numChannels()

  # The number of samples is stored in the clip format's width.
  #
  print "Audio stream has %d samples per channel." % format.numSamples()

  # Allocate the audio block sample buffer.  See sections above to determine
  # how to interpret the raw buffers.
  #
  buff = '0' * format.frameBufferSize()

  # Read all blocks of samples.
  #
  i = 0
  while i < numFrames:
    print "Reading sample block %i." % i
    if not clip.readFrame(i, buff, format.frameBufferSize()):
      raise WireTapException('Unable to obtain read sample block %i: %s.' % (i, clip.lastError()))
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

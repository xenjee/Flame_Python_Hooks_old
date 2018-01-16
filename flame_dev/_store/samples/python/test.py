#!/usr/bin/env python
#!/opt/Autodesk/python/2018.3/bin/python2.7

# *****************************************************************************
##
# File         test.py
##
# Description   WireTap SDK sample python program ping a server.
##
# Copyright (c) 2016 Autodesk, Inc.
# All rights reserved.
##
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
##
# *****************************************************************************


class WireTapException(Exception):
  pass


# *****************************************************************************
def main(argv):
  # check the command line options for correctness
  try:
    opts, args = getopt.getopt(argv, "h:")
  except getopt.GetoptError:
    print "Usage:\n" \
          "-h <hostname>\n"
    sys.exit(2)

  # default host name
  hostName = "localhost"

  # parse command line option to set specified host name
  for opt, arg in opts:
    if opt == '-h':
      hostName = arg

  # Initialize the Wiretap Client API.
  wireTapClient = WireTapClient()
  if not wireTapClient.init():
    raise WireTapException("Unable to initialize WireTap client API.")

  pingTest(hostName)


# *****************************************************************************
def pingTest(hostName):
  # Instantiate a server handle, and traverse.
  server = WireTapServerHandle(hostName)

  # Ping test.
  if not server.ping():
    raise WireTapException("Ping to host: '%s' failed: %s." % (hostName, server.lastError()))
  else:
    print 'Ping of host: \'%s\' successful.' % hostName


# *****************************************************************************
if __name__ == '__main__':
  import sys
  import getopt
  import string
  import sys
  sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
  from libwiretapPythonClientAPI import *
  main(sys.argv[1:])

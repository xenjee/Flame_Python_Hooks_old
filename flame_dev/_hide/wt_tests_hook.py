#!/bin/env python
#******************************************************************************


def getCustomUIActions():
    pathcopyaction = dict(name='wt_test', caption='wt_test_01')
    pathcopygrp = dict(name='wt tests', actions=(pathcopyaction,))
    return (pathcopygrp,)


def customUIAction(info, userData):
    if info['name'] == 'wt_test':

        import sys
        import getopt
        import string
        sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
        from libwiretapPythonClientAPI import WireTapClient
        from libwiretapPythonClientAPI import WireTapServerHandle
        #from libwiretapPythonClientAPI import WireTapNodeHandle
        #from libwiretapPythonClientAPI import WireTapInt
        #from libwiretapPythonClientAPI import WireTapServerId
        #from libwiretapPythonClientAPI import WireTapServerList
        #from libwiretapPythonClientAPI import WireTapServerInfo
        #from libwiretapPythonClientAPI import WireTapClipFormat

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
        # if __name__ == '__main__':
            # main(sys.argv[1:])
        main(sys.argv[1:])

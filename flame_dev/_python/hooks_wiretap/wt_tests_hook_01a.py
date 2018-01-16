#!/bin/env python
#******************************************************************************


def getCustomUIActions():
    hostnameaction = dict(name='print_hostname', caption='Print hostname')
    listserversaction = dict(name='list_servers', caption='List all servers')
    timelineaction = dict(name='create_timeline', caption='Create timeline')
    hostnamegroup = dict(name='Wiretap Examples', actions=(hostnameaction, listserversaction, timelineaction,))
    return (hostnamegroup,)


def customUIAction(info, userData):

    # *****************************************************************************
    # print_hostname
    # *****************************************************************************

    if info['name'] == 'print_hostname':
        import sys
        import getopt
        import string
        sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
        from libwiretapPythonClientAPI import WireTapClient
        from libwiretapPythonClientAPI import WireTapServerHandle

        # *****************************************************************************
        class WireTapException(Exception):
            pass

        # *****************************************************************************
        def mainHostName():

            # default host name
            hostName = "localhost"

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
                print '-' * 80
                print 'Ping of host: \'%s\' successful.' % hostName
                print '-' * 80
        # *****************************************************************************

        mainHostName()

    # *****************************************************************************
    # list_servers
    # *****************************************************************************

    if info['name'] == 'list_servers':
        import string
        import sys
        sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
        from libwiretapPythonClientAPI import WireTapClient
        from libwiretapPythonClientAPI import WireTapServerHandle
        from libwiretapPythonClientAPI import WireTapServerList
        from libwiretapPythonClientAPI import WireTapServerInfo
        from libwiretapPythonClientAPI import WireTapInt

        # *****************************************************************************
        class WireTapException(Exception):
            pass

        # *****************************************************************************
        def mainServers():

            # Initialize the Wiretap Client API.
            #
            wireTapClient = WireTapClient()
            if not wireTapClient.init():
                raise WireTapException("Unable to initialize WireTap client API.")

            listAllServers()

        # *****************************************************************************
        def listAllServers():

            # Obtain the list of Wiretap servers.
            #
            list = WireTapServerList()
            count = WireTapInt()
            if not list.getNumNodes(count):
                raise WireTapException("Error acquiring server list: %s." % list.lastError())

            print "Server                IP address  Storage Id     Protocol"
            print '-'*40 + " servers " + '-'*40

            # Obtain information about each server.
            #
            i = 0
            while i < count:
                info = WireTapServerInfo()
                if not list.getNode(i, info):
                    raise WireTapException("Error accessing server %d: %s." % (i, list.lastError()))

                print "%-16s %15s  %-16s %d.%d" % (info.getDisplayName(),
                                                   info.getHostname(),
                                                   info.getStorageId(),
                                                   info.getVersionMajor(),
                                                   info.getVersionMinor())

                i = i + 1
                pass
            print '-'*89

        # *****************************************************************************

        mainServers()

    # *****************************************************************************
    # Create Timeline
    # *****************************************************************************

    if info['name'] == 'create_timeline':
        import sys
        import getopt
        import string
        sys.path.append('/opt/Autodesk/python/2018.3/lib/python2.7/site-packages/adsk/')
        from libwiretapPythonClientAPI import WireTapClient
        from libwiretapPythonClientAPI import WireTapServerHandle
        from libwiretapPythonClientAPI import WireTapNodeHandle
        from libwiretapPythonClientAPI import WireTapClipFormat
        from libwiretapPythonClientAPI import WireTapStr

        ##*****************************************************************************
        class WireTapException( Exception ):
          pass


        ##*****************************************************************************
        # Creation of a source clip node.
        #
        def createClipNode( parent, name, tapeName, numFrames, clip):

          # Define an IFFS XML stream to provide the tape name to the
          # source clip that will be created.
          # Note that pre-2008 verions of the IFFFS Wiretap server accept
          # "IFFFS_XML" as the metadata stream name and root tag.
          #
          xmlStream = "<XML Version=\"1.0\">" 
          xmlStream += "<ClipData>" 
          xmlStream += "<TapeName>" 
          xmlStream += tapeName 
          xmlStream += "</TapeName>"
          xmlStream += "</ClipData>"
          xmlStream += "</XML>"  

          print xmlStream

          # Define a clip format.  The parameters allow the server to
          # determine the frame buffer size for an NTSC raw RGB frame,
          # which can be queried when the clip is created.
          # The XML metadata tag allows you to specify the source tape
          # name, among other things.
          # Other information, such as the source timecode and the drop
          # mode, could be also provided to the source clip using the same
          # XML stream and XML metadata tag.
          #
          format = WireTapClipFormat( 720, 486,         # width, height 
                          3 * 8,            # bits per pixel
                          3,        # # channels
                          29.97,        # frame rate 
                          0.9,      # pixel ratio 
                          WireTapClipFormat.ScanFormat.SCAN_FORMAT_FIELD_1_ODD, 
                          WireTapClipFormat.FORMAT_RGB(),
                          "XML",
                          xmlStream ) 

          # Create the new clip node.  Each server will provide a list of
          # extended types (specifyable as a string or an enum).
          # 
          if not parent.createClipNode( name,     # display name 
                                format,   # clip format 
                            "CLIP",   # extended (server-specific) type 
                                clip ):   # created node returned here 
            raise WireTapException ( '"Unable to create clip node: %s.' % parent.lastError() )
            return False
             

          # Set the number of frames.
          #
          if not clip.setNumFrames( numFrames ): 
            raise WireTapException( 'Unable to set the number of frames: %s.' % clip.lastError() )
            return False

          print "Clip %s successfully created." % name
          return True


        ##*****************************************************************************
        def main(argv):

          # check the command line options for correctness
          try:
            options, value = getopt.getopt(argv, "h:n:")
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
          for key, value in options:
            if options == '-h':
              hostName = value
            elif key == '-n':
              nodeId = value

          # Initialize the Wiretap Client API.
          #
          wireTapClient = WireTapClient()
          if not wireTapClient.init():
            raise WireTapException( "Unable to initialize WireTap client API." )

          createTimeline( hostName, nodeId )


        ##*****************************************************************************
        def createTimeline( hostName, nodeId ):

          # Instantiate a server handle
          #
          server = WireTapServerHandle( hostName )

          # Instantiate the clip node handles for the given server and the node ID
          #
          # To assemble a timeline from sources nodes, all sources nodes and
          # the resulting timeline needs to be located in the same reel.
          # The nodeId is the reel where the sources nodes will be created
          # and the timeline assembled.
          #
          parentReel = WireTapNodeHandle ( server, nodeId )

          # Verify that the parent nodeId is effectively a reel
          #
          reelTypeStr = WireTapStr( "REEL" ) # IFFFS server specific type

          parentTypeStr = WireTapStr()
          if not parentReel.getNodeTypeStr( parentTypeStr ):
            raise WireTapException( 'Unable to get the type of the parent node - %s.' \
                  % parentReel.lastError() )

          if not parentTypeStr == reelTypeStr :
            raise WireTapException( 'Unable to assemble a timeline without a parent reel.' )

          # Creation of 3 sources clips. Clip name, tape name and number of
          # frames are specified for each clip.
          #
          clip1 = WireTapNodeHandle()
          clip2 = WireTapNodeHandle()
          clip3 = WireTapNodeHandle()
          if not createClipNode( parentReel, "SOURCE_1", "TAPE1", 10, clip1 ):
            return False

          if not createClipNode( parentReel, "SOURCE_2", "TAPE2", 20, clip2 ):
            return False

          if not createClipNode( parentReel, "SOURCE_3", "TAPE2", 30, clip3 ):
            return False

          # Define an DMXEDL stream describing the timeline we want to
          # create. DMXEDL is an EDL type metadata stream specific to the
          # IFFFS wiretap server.
          # This DMXEDL refers to the previously created sources clip.
          # The resulting timeline will have a cut between the first two
          # sources clips and a dissolve of 5 frames between the second and
          # third sources clips.
          # Note that the tape name indicated in the DMXEDL should match the
          # tape name of the sources clip previously created.

          metadata = (
             "TITLE: TIMELINE\n" \
             "FCM: NON-DROP FRAME\n\n" \
             "TITLE: ASSEMBLY RESOLUTION: " \
             "720:486:24:3:0.899998:1049776:BE:F1:29.969999    \n" \
             "FCM: NON-DROP FRAME\n\n" \
             "001  TAPE1   V     C        " \
             "00:00:00:00 00:00:00:10 00:00:00:10 00:00:00:20  \n" \
             "FROM CLIP NAME: SOURCE_1\n" \
             "DLEDL: START TC: 00:00:00:00\n\n" \
             "002  TAPE2   V     C        " \
             "00:00:00:00 00:00:00:13 00:00:00:20 00:00:01:03  \n" \
             "FROM CLIP NAME: SOURCE_2\n" \
             "DLEDL: START TC: 00:00:00:00\n\n" \
             "003  TAPE2   V     C        " \
             "00:00:00:13 00:00:00:13 00:00:01:03 00:00:01:03  \n" \
             "003  TAPE2   V     D    " \
             "005 00:00:00:03 00:00:00:20 00:00:01:03 00:00:02:00  \n" \
             "FROM CLIP NAME: SOURCE_2\n" \
             "TO CLIP NAME: SOURCE_3\n" \
             "DLEDL: START TC: 00:00:00:00\n" \
             "DLEDL: FOCUS_DESCR CENTERED\n" )

          # Define a clip format.
          #
          format = WireTapClipFormat( 720, 486,   # width, height
                                     3 * 8,      # bits per pixel
                                     3,      # # channels
                                     29.97,  # frame rate
                                     0.9,    # pixel ratio
                                     WireTapClipFormat.ScanFormat.SCAN_FORMAT_FIELD_1_ODD,
                                     WireTapClipFormat.FORMAT_RGB() )

          # Create the timeline node which is a regular clip node
          #
          clip = WireTapNodeHandle()
          if not parentReel.createClipNode( "Timeline", # display name
                                            format,     # clip format
                                            "CLIP",     # extended (server-specific) type
                                            clip ):     # created node returned here
            raise WireTapException( 'Unable to create clip node: %s.' % parentReel.lastError() )

          print "Timeline node successfully created"

          # Apply the metadata stream to the created clip node.
          # The IFFFS timeline is assembled from the 3 sources clips.
          #
          #if not clip.setMetaData( IFFFS_WT_STREAM_DMXEDL, metadata ):
          if not clip.setMetaData( "DMXEDL", metadata ):
            raise WireTapException( 'Unable to apply the metadata stream - %s.' % clip.lastError() )

          print "Timeline successfully assembled"


        ##*****************************************************************************
        if __name__ == '__main__':
          main(sys.argv[1:])















        #

//*****************************************************************************/
//
// Filename     createTimeline.C
//
// Description  Wiretap SDK sample program to create a new clip based on an
//              IFFFS timeline from three source clip nodes.
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.
//
//*****************************************************************************/

#include <WireTapClientAPI.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#ifdef _WIN32
  #ifndef snprintf
  # define snprintf _snprintf	
  #endif
#endif

namespace
{
  // Global variables.  Get values from environment variables if available.
  // Default "localhost" will work for hostName if a Wiretap server 
  // is running on your machine.
  // 
  const char *hostEnv = getenv( "WIRETAP_HOST" );
  const char *hostName = hostEnv == 0 ? "localhost" : hostEnv;
  const char *nodeIdEnv = getenv( "WIRETAP_NODE_ID" );
  const char *nodeId = nodeIdEnv == 0 ? "" : nodeIdEnv;

  // Global function to create a source clip node.
  //
  bool createClipNode( WireTapNodeHandle& parent,
		       const char* name,
		       const char* tapeName,
		       const int numFrames,
		       const char* startKeycode,
		       const char* filmGauge,
		       const int footReference,
		       const char* telecineSpeed,
		       WireTapNodeHandle& clip ) 
  {
    // Define an XML stream to supply a tape name for the
    // source clip that will be created.
    // NOTE: Pre-2008 versions of the IFFFS Wiretap Server accept
    // "IFFFS_XML" as the metadata stream name and root tag.
    //
    const char* xmlStreamFmt = "<XML Version=\"1.0\">"
                               "<ClipData>"
                               "<TapeName>%s</TapeName>"
                               "<FilmData>"
                               "<StartKeycode>%s</StartKeycode>"
                               "<FilmGauge>%s</FilmGauge>"
                               "<FootReference>%d</FootReference>"
                               "<TelecineSpeed>%s</TelecineSpeed>"
                               "</FilmData>"
                               "</ClipData>"
                               "</XML>";
    char xmlStream[300];
    snprintf( xmlStream, 
	      sizeof(xmlStream), 
	      xmlStreamFmt, 
	      tapeName, 
	      startKeycode, 
	      filmGauge, 
	      footReference, 
	      telecineSpeed );

    // Define a clip format.  The parameters allow the server to
    // determine the frame buffer size for an NTSC raw RGB frame.
    // The buffer size calculated by the server can be obtained from the
    // clip format after the clip node has been created.
    // The XML metadata allows you to specify the name of the source tape.
    // Other information, such as the source timecode and the drop
    // mode, could be also provided to the source clip in the same
    // XML stream.
    //
    WireTapClipFormat format( 720, 486,     	// width, height 
			      3 * 8,           	// bits per pixel
			      3, 		// # channels
			      29.97f,		// frame rate 
			      0.9f,		// pixel ratio 
			      WireTapClipFormat::SCAN_FORMAT_FIELD_1_ODD, 
			      WireTapClipFormat::FORMAT_RGB(),
			      "XML",
			      xmlStream ); 

    // Create a new node of type "CLIP" (a node type defined by 
    // the IFFFS Wiretap Server).  Each Wiretap server defines a set of 
    // node types (specified as string constants).
    // 
    if ( !parent.createClipNode( name,     // display name 
				 format,   // clip format 
				 "CLIP",   // extended (server-specific) type 
				 clip ) )  // created node returned here 
    { 
      printf( "Unable to create clip node: %s.\n", parent.lastError() ); 
      return false; 
    } 

  // Allocate the number of frames on the server.
  //
    if ( !clip.setNumFrames( numFrames ) ) { 
      printf( "Unable to set the number of frames: %s\n", clip.lastError() ); 
      return false; 
    }

    printf( "Clip %s successfully created \n", name );

    return true;
  }
}
			

int main( int argc, char **argv)
{
  // Initialize the Wiretap Client API.
  //
  WireTapClient wireTapClient;
  if ( !wireTapClient.init() ) {
    printf( "Unable to initialize WireTap client API.\n" );
    return 1;
  }

  // Instantiate a server handle.
  //
  WireTapServerId serverId( "IFFFS", hostName );
  WireTapServerHandle server( serverId );

  // Instantiate a node handle for the given server and the node ID
  //
  // To assemble a timeline from sources nodes, all sources nodes and
  // the resulting timeline must be located in the same reel.
  // nodeId is the ID of the reel in which the source nodes will be 
  // created and the timeline assembled.
  //
  WireTapNodeHandle parentReel( server, nodeId );

  // Verify that parent nodeId is the ID of a reel
  //
  WireTapStr reelTypeStr( "REEL" ); // Type defined by IFFFS Wiretap Server
  WireTapStr parentTypeStr;
  if ( !parentReel.getNodeTypeStr( parentTypeStr ) ) {
    printf( "Unable to get the type of the parent node - %s \n",
	    parentReel.lastError() );
    return 1;
  }
  if ( !(parentTypeStr == reelTypeStr) ) {
    printf( "Unable to assemble a timeline without a parent reel \n");
    return 1;
  }

  // Create three dummy source clips. Clip name, tape name, and number of
  // frames are specified for each clip.
  //
  WireTapNodeHandle clip1, clip2, clip3;
  if ( !createClipNode( parentReel, 
			"SOURCE_1", 
			"TAPE1", 
			10, 
			"FR123411 0011+00",
			"35MM 3PERF",
			2,
			"29.97 fps NDF",
			clip1 ) ) {
    return 1;
  }
  if ( !createClipNode( parentReel, 
			"SOURCE_2", 
			"TAPE2", 
			20, 
			"EE123411 0011+00",
			"35MM 4PERF",
			1,
			"29.97 fps NDF",
			clip2 ) ) {
    return 1;
  }    
  if ( !createClipNode( parentReel, 
			"SOURCE_3", 
			"TAPE2", 
			30,
			"AF123411 0011+00",
			"65MM",
			1,
			"29.97 fps NDF",
			clip3 ) ) {
    return 1;
  }

  // Define an DMXEDL stream describing the timeline we want to
  // create. DMXEDL is an EDL type metadata stream specific to the
  // IFFFS Wiretap Server.
  // This DMXEDL stream refers to the three source clips defined above.
  // The resulting timeline will have a cut between the first two
  // source clips and a dissolve of 5 frames between the second and
  // third source clips.
  // Note that the tape name indicated in the DMXEDL should match the
  // tape name for the three source clips.

  WireTapStr metadata =
     "TITLE: TIMELINE\n"
     "FCM: NON-DROP FRAME\n\n"
     "TITLE: ASSEMBLY RESOLUTION: "
     "720:486:24:3:0.899998:1049776:BE:F1:29.969999    \n"
     "FCM: NON-DROP FRAME\n\n"
     "001  TAPE1   V     C        "
     "00:00:00:00 00:00:00:10 00:00:00:10 00:00:00:20  \n"
     "FROM CLIP NAME: SOURCE_1\n"
     "DLEDL: START TC: 00:00:00:00\n\n"
     "002  TAPE2   V     C        "
     "00:00:00:00 00:00:00:13 00:00:00:20 00:00:01:03  \n"
     "FROM CLIP NAME: SOURCE_2\n"
     "DLEDL: START TC: 00:00:00:00\n\n"
     "003  TAPE2   V     C        "
     "00:00:00:13 00:00:00:13 00:00:01:03 00:00:01:03  \n"
     "003  TAPE2   V     D    "
     "005 00:00:00:03 00:00:00:20 00:00:01:03 00:00:02:00  \n"
     "FROM CLIP NAME: SOURCE_2\n"
     "TO CLIP NAME: SOURCE_3\n"
     "DLEDL: START TC: 00:00:00:00\n"
     "DLEDL: FOCUS_DESCR CENTERED\n";

  // Define a clip format.
  // 
  WireTapClipFormat format( 720, 486,  // width, height 
			    3 * 8,     // bits per pixel
			    3, 	       // # channels
			    29.97f,    // frame rate 
			    0.9f,      // pixel ratio 
			    WireTapClipFormat::SCAN_FORMAT_FIELD_1_ODD, 
			    WireTapClipFormat::FORMAT_RGB() );


  // Create the timeline node which is a node of type "CLIP".
  // It is empty at first.
  //
  WireTapNodeHandle clip; 
  if ( !parentReel.createClipNode( "Timeline", // display name 
				   format,     // clip format 
				   "CLIP",     // node type (server-specific) 
				   clip ) )    // created node returned here 
  { 
    printf( "Unable to create clip node: %s.\n", parentReel.lastError() ); 
    return 1; 
  } 

  printf( "Timeline node successfully created \n");

  // Apply the metadata stream to the clip node just created.
  // This call actually assembles the frames from the three source clips
  // into the empty clip node.
  //
  if ( !clip.setMetaData( "DMXEDL", metadata ) ) {
    printf( "Unable to apply the metadata stream - %s \n",clip.lastError() );
    return 1;
  }

  printf( "Timeline successfully assembled \n" );

  return 0;
}

//*****************************************************************************/
//
// Filename     createClip.C
//
// Description  Wiretap SDK sample program to create a video clip.
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

  // Instantiate a clip node handle for the given server and node ID.
  //
  WireTapNodeHandle parent( server, nodeId );

  // Define a clip format. The parameters allow the server to
  // determine the frame buffer size for the specified frame format
  // (in this example, an NTSC raw RGB frame). The buffer size calculated
  // by the server can be obtained after the clip has been created.
  //
  WireTapClipFormat format( 720, 486,   // width, height 
                            3 * 8,      // bits per pixel
			    3,          // # channels
                            29.97f,     // frame rate 
                            0.9f,       // pixel ratio 
                            WireTapClipFormat::SCAN_FORMAT_FIELD_1_ODD, 
                            WireTapClipFormat::FORMAT_RGB() ); 

  // Create a new node of type "CLIP" (a node type defined by 
  // the IFFFS Wiretap Server).  Each Wiretap server defines a set of 
  // node types (specified as string constants).
  //
  WireTapNodeHandle clip; 
  if ( !parent.createClipNode( "MyNewClip", // display name 
                               format,	    // clip format 
                               "CLIP",      // node type (server-specific)
                               clip ) )     // created node returned here 
  { 
    printf( "Unable to create clip node: %s.\n", parent.lastError() ); 
    return 1; 
  } 

  // Allocate the number of frames on the server.
  //
  const int numFrames = 5;
  if ( !clip.setNumFrames( numFrames ) ) { 
    printf( "Unable to set the number of frames: %s\n", clip.lastError() ); 
    return 1; 
  }

  // Get the clip format back from the clip node. Even though we defined the 
  // format above, we must query the updated format to get the size of the 
  // frame buffer calculated by the server.  The server will also fill in 
  // any format metadata that was not specified (for example: timecode, 
  // drop mode, and so on).
  //
  if ( !clip.getClipFormat( format ) ) {
    printf( "Unable to obtain clip format: %s\n", clip.lastError() );
    return 1;
  } 

  // Allocate the frame buffer.
  //
  char *buffer = (char *)malloc( format.frameBufferSize() ); 
  if ( buffer == 0 ) { 
    printf( "Out of memory." ); 
    return 1; 
  }

  // Read frames from the buffer and write them to the clip node.
  //
  for ( int i = 0; i < numFrames; i++ ) { 
    if ( !clip.writeFrame( i, buffer, format.frameBufferSize() ) ) { 
      printf( "Unable to obtain write frame %d: %s\n", i, clip.lastError() ); 
      break; 
    } 
    // Print the frame index.
    //
    printf( "Successfully wrote frame %d.\n", i ); 

  }

  // Free the buffer.
  //
  free( buffer ); 

  return 0;
}


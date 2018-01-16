//*****************************************************************************/
//
// Filename     readFrames.C
//
// Description  Wiretap SDK sample program to read all frames from a clip into
//              a buffer.
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

  // Instantiate a node handle for the given server and node ID.
  //
  WireTapNodeHandle clip( server, nodeId );

  // Get the number of frames in the clip.
  //
  unsigned numFrames;
  if ( !clip.getNumFrames( numFrames ) ) {
    printf( "Unable to obtain number of frames: %s\n", clip.lastError() );
    return 1;
  }

  // Get the clip format.  This is required to know how to interpret the frame
  // data, and to know how big the frame buffer must be.
  //
  WireTapClipFormat format;
  if ( !clip.getClipFormat( format ) ) {
    printf( "Unable to obtain clip format: %s\n", clip.lastError() );
    return 1;
  } 

  // Interpret the format tag (see WireTapTypes.h for a list of tags).
  //
  if ( !strcmp( format.formatTag(), WireTapClipFormat::FORMAT_RGB() ) ) {
    printf( "This is an RGB clip.\n" );
  } else
  if ( !strcmp( format.formatTag(), WireTapClipFormat::FORMAT_YUV() ) ) {
    printf( "This is a YUV clip.\n" );
  } else {
    printf( "Unknown clip format: %s.\n", format.formatTag() ); 
  }

  // Allocate the frame buffer.
  //
  char *buffer = (char *)malloc( format.frameBufferSize() );
  if ( buffer == 0 ) {
    printf( "Out of memory." );
    return 1;
  }

  // Read all frames.
  //
  for ( unsigned i = 0; i < numFrames; i++ ) {
    printf( "Reading frame %d.\n", i ); 
    if ( !clip.readFrame( i,
                          0 /* params */, 0 /* paramsSize */,
                          buffer, format.frameBufferSize() ) ) {
      printf( "Unable to obtain read frame %d: %s\n", i, clip.lastError() );
      break;
    }
  } 
  free( buffer ); 

  return 0;
}


//*****************************************************************************/
//
// Filename     listFrames.C
//
// Description  Wiretap SDK sample program to list frame IDs and frame file
//              paths for all the frames in a clip.
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

  // Read all frame IDs and frame file paths.
  //
  for ( unsigned i = 0; i < numFrames; i++ ) {
    // A frame ID is an opaque string, unique to the server.
    //
    WireTapStr frameId;
    if ( !clip.getFrameId( i, frameId ) ) {
      printf( "Unable to obtain frame ID %d: %s\n", i, clip.lastError() );
      return 1;
    }

    // Frame IDs have an optional path representation. If paths are available, 
    // a Wiretap client can use them to access frames directly, instead of 
    // calling readFrame(). The frame path will be an empty string if a path 
    // representation of the frame ID does not exist.
    // If path translation services are enabled and configured,
    // the mount point of the current machine will be used
    // (for more info, see the Stone and Wire Filesystem and Networking Guide).
    //
    WireTapStr frameIdPath;
    if ( !clip.getFrameIdPath( i, frameIdPath ) ) {
      printf( "Unable to obtain frame ID path %d: %s\n", i, clip.lastError() );
      return 1;
    }
    const char *p = frameIdPath.c_str();
    printf( "Frame %d. ID: '%s'  File Path:'%s'.\n", i,
	    frameId.c_str(), p[0] == '\0' ? "none" : p ); 
  } 

  return 0;
}


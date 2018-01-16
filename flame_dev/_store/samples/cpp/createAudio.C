//*****************************************************************************/
//
// Filename     createAudio.C
//
// Description  Wiretap SDK sample program to create an audio clip.
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
  // Global variables.  
  // Get values from environment variables if available.
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

  // Instantiate a node handle for the given server and parent node ID.
  //
  WireTapNodeHandle parent( server, nodeId );

  // Define an audio clip format representing one channel of 10 minutes of
  // 48kHz little-endian floating point audio samples.  
  // Additional audio parameters can be set via the format metadata, though
  // none are set in this example.  
  // See the Wiretap Developer's Guide for details.
  //
  const float rate = 48000.0f;
  const int durationSec = 600;
  const int bitsPerSample = 32;
  const int bytesPerSample = bitsPerSample / 8;
  const int numSamples = durationSec * int( rate );
  WireTapAudioFormat format( numSamples,            // number of samples 
                             bitsPerSample,         // bits per sample
                             1,                     // # channels
                             rate,                  // sample rate
                             WireTapClipFormat::FORMAT_DL_AUDIO_FLOAT_LE(),
                             0 );                   // format metadata

  // Create a new node of type "AUDIOSTREAM" (a node type defined by 
  // the IFFFS Wiretap Server).  Each Wiretap server defines a set of 
  // node types (specified as string constants).
  //
  WireTapNodeHandle audioClip; 
  if ( !parent.createClipNode( "MyNewClip",   // display name 
                               format,	      // clip format 
                               "AUDIOSTREAM", // server-specific node type
                               audioClip ) )  // created node returned here 
  { 
    printf( "Unable to create audio clip node: %s.\n", parent.lastError() ); 
    return 1; 
  } 

  // Get the clip format to obtain the size of the audio tiles the server is
  // expecting to receive. The server calculates audio tile size 
  // from the values set above in the clip format.
  //
  if ( !audioClip.getClipFormat( format ) ) {
    printf( "Unable to obtain audio clip format: %s\n", audioClip.lastError() );
    return 1;
  } 

  // Allocate the audio tile buffer.
  //
  int tileSize = format.frameBufferSize();
  char *buffer = (char *)malloc( tileSize ); 
  if ( buffer == 0 ) { 
    printf( "Out of memory." ); 
    return 1; 
  }

  // Write the tiles.
  //
  int numTiles = ( bytesPerSample * numSamples - 1 ) / tileSize + 1;
  for ( int i = 0; i < numTiles; i++ ) { 
    if ( !audioClip.writeFrame( i, buffer, tileSize ) ) { 
      printf( "Unable to write tile %d: %s\n", i, audioClip.lastError() ); 
      break; 
    } 
    // Print the frame index.
    //
    printf( "Successfully wrote tile %d.\n", i ); 

  }

  // Free the buffer.
  //
  free( buffer ); 

  return 0;
}


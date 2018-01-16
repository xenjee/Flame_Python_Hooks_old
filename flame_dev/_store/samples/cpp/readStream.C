//*****************************************************************************/
//
// Filename     readStream.C
//
// Description  WireTap SDK sample program to read a binary stream.
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
  const char *hostEnv = getenv( "WIRETAP_HOST" );
  const char *hostName = hostEnv == 0 ? "localhost" : hostEnv;
  const char *streamIdEnv = getenv( "WIRETAP_STREAM_ID" );
  const char *streamId = streamIdEnv == 0 ? "unknown" : streamIdEnv;
}

int main( int argc, char **argv)
{
  int ret = 0;

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

  // Set up stream chunk/item variables.  Need to use a big enough chunk size
  // to optimize network IO.  256 KB to 1 MB is good for fast networks.
  //
  const int numItemsPerChunk = 256*1024;
  const int itemSize = 1;		// 1 byte per item
  const int chunkBufSizeInBytes = numItemsPerChunk * itemSize;
  char *chunkBuf = new char [ chunkBufSizeInBytes ];

  // Iterate across all chunks in the stream.  Unless specified, parameters
  // are specified in ITEMS, not bytes.
  //
  int itemOffset = 0, numItemsToRead = numItemsPerChunk;
  for ( ; ; )
  {
    // Read the data from the server.
    //
    if ( !server.readStream( streamId, chunkBuf, chunkBufSizeInBytes,
			     itemOffset, itemSize, numItemsToRead ) )
    {
      printf( "Unable to read stream '%s' from server '%s': %s.\n",
	      streamId, hostName, server.lastError() );
      ret = 1;
      break;
    }

    // The server reads the specified number of items and returns the ACTUAL
    // number of items it read.  This number will only differ from the
    // specified value at the END of the stream.
    //
    if ( numItemsToRead != numItemsPerChunk ) {
      break;
    }

    // Increment the ITEM offset of the next chunk.
    //
    itemOffset += numItemsToRead;
  } 

  // Were all chunks read successfully?
  //
  if ( ret == 0 ) {
    printf( "Successfully read stream '%s' from server '%s'.\n",
	    streamId, hostName );
  }

  // Uninitialize WireTap services.
  //
  delete [] chunkBuf; 

  return ret;
}


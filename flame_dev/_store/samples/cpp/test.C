//*****************************************************************************/
//
// Filename     test.C
//
// Description  Wiretap SDK sample program to ping a server.
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

namespace
{
  // Global variable for a Wiretap server (can be IP address or name). 
  // Get the value from an environment variable if available.
  // Default "localhost" will work if a Wiretap server 
  // is running on your machine.
  // 
  const char *hostEnv = getenv( "WIRETAP_HOST" );
  const char *hostName = hostEnv == 0 ? "localhost" : hostEnv;
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

  int majorV, minorV, maintV;
  WireTapClientGetVersion( majorV, minorV, maintV );
  printf( "Using WireTap Client API v%d.%d.%d.\n", majorV,minorV,maintV );
  
  // Instantiate a server handle and ping it.
  //
  WireTapServerId serveId( "IFFFS", hostName );
  WireTapServerHandle server( serveId );
  
  // Ping test.
  //
  if ( !server.ping() ) {
    printf( "Ping to host: '%s' failed: %s.", hostName, server.lastError() );
    return 1;
  }
  printf( "Ping of host: '%s' successful.\n", hostName );

  return 0;
}

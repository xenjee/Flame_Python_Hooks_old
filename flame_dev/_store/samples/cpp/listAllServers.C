//*****************************************************************************/
//
// Filename     listAllServers.C
//
// Description  Wiretap SDK sample program to list all WireTap servers.
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

int main( int argc, char **argv)
{
  // Initialize the Wiretap Client API.
  //
  WireTapClient wireTapClient;
  if ( !wireTapClient.init() ) {
    printf( "Unable to initialize WireTap client API.\n" );
    return 1;
  }

  // Obtain the list of Wiretap servers.
  //
  WireTapServerList list;
  int count = 0;
  if ( !list.getNumNodes( count ) ) {
    printf( "Error acquiring server list: %s.", list.lastError() );
    return 1;
  }

  printf( "Server                IP address  Database\n" );
  printf( "---------------------------------------------------\n" );
   
  // Obtain information about each server.
  //
  for ( int i = 0; i < count; ++ i ) {
    WireTapServerInfo info;
    if ( !list.getNode( i, info ) ) {
       printf( "Error accessing server %d: %s.", i, list.lastError() );
       return 1;
    }
    printf( "%-16s %15s  %s\n",
	    info.getDisplayName(),
            info.getId().getIPAddr(),
            info.getDatabase() );
  }

  return 0;
}

//*****************************************************************************/
//
// Filename     resolveStorageId.C
//
// Description  Wiretap SDK sample program to resolve a storage ID (unique
//              identifier of a storage device) into a Wiretap server ID.
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
  if ( argc <= 1 ) {
    printf( "Usage: %s <storage id>\n", argv[0] );
    return 1;
  }

  // storageId should be set to the ID of a storage device on the Wiretap
  // network. 
  char *storageId = argv[1];

  // Initialize the Wiretap Client API.
  //
  WireTapClient wireTapClient;
  if ( !wireTapClient.init() ) {
    printf( "Unable to initialize WireTap client API.\n" );
    return 1;
  }

  // Resolve the given storage ID to determine to which Wiretap server the
  // storage device is connected
  //
  WireTapServerList list;
  WireTapServerId id;
  WireTapServerInfo server;
  id.setStorageId( storageId );
  if ( !list.resolve( id, server ) ) {
    printf( "Unable to resolve '%s' into a server ID: %s.\n",
	    storageId, list.lastError() );
    return 1;
  }
  
  // Obtain IP address of the Wiretap server
  //
  printf( "Successfuly resolved storage ID '%s' into server '%s'.\n",
          storageId, server.getId().getId() );
  return 0;
}

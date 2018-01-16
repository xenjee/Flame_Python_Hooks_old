//*****************************************************************************/
//
// Filename     createUser.C
//
// Description  Wiretap SDK sample program to create an empty user node and set
//              its metadata.
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.
//
//*****************************************************************************/

// 
// Please see the Wiretap Developer's Guide for an explanation of the user
// node hierarchy.
//
// NOTE: To create a new user with a preferences hierarchy, copy a user created
// in an IFFFS application (see the copyUser.cpp sample program).
//

#include <WireTapClientAPI.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

namespace
{
  // Global variable for a Wiretap server (can be IP address or name). 
  // Get value from environment variable if available.
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

  // Instantiate a server handle.
  //
  WireTapServerId serverId( "IFFFS", hostName );
  WireTapServerHandle server( serverId );

  // Instantiate a user node handle for the given server and node ID.
  // We hard-code the node ID here to create an IFFFS "editing" user.
  // This will just create a user database entry. The new user node 
  // will be empty. No preferences hierarchy will be created beneath it.
  //
  WireTapNodeHandle parent( server, "/stonefs/users/editing" );
  WireTapNodeHandle user;
  if ( !parent.createNode( "Paul", "USER", user ) ) {
    printf( "Unable to create user node: %s\n", parent.lastError() );
    return 1;
  }

  // Prepare user metadata stream in XML format.
  // 
  WireTapStr metadata = 
    "<User>"
    "<Name>Paul</Name>"
    "<PreferenceDir>/stonefs/users/editing/Paul/preferences</PreferenceDir>"
    "<Default>True</Default>"
    "</User>";
    
  // Set the user meta data
  // 
  if ( !user.setMetaData( "XML", metadata ) ){
    fprintf(stderr, "Error setting user metadata : %s\n",
	    user.lastError() );
    return 1;     
  }
  else {
    fprintf(stderr, "User set metadata successful.\n" );
  }

  return 0;
}

//*****************************************************************************/
//
// Filename     listChildren.C
//
// Description  Wiretap SDK sample program to list all child nodes.
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

  // Instantiate a server object.
  //
  WireTapServerId serverId( "IFFFS", hostName );
  WireTapServerHandle server( serverId );

  // Obtain the root node of the server.
  //
  WireTapNodeHandle rootNode;
  if ( !server.getRootNode( rootNode ) ) {
    printf( "Unable to obtain server root node: %s\n", server.lastError() );
    return 1;
  } 

  // Iterate across the first level of children.
  //
  WireTapNodeHandle child;
  unsigned numChildren;
  if ( !rootNode.getNumChildren( numChildren ) ) {
    printf( "Unable to obtain number of children: %s\n", rootNode.lastError() );
    return 1;
  }
  for ( unsigned i = 0; i < numChildren; i++ )
  {
    // Get the child node.
    //
    rootNode.getChild( i, child );

    // Get the node's display name and type.
    //
    WireTapStr name, typeStr;
    if ( !child.getDisplayName( name ) ) {
      printf( "Unable to obtain node name: %s\n", child.lastError() );
      return 1;
    }
    if ( !child.getNodeTypeStr( typeStr ) ) {
      printf( "Unable to obtain node type: %s\n", child.lastError() );
      return 1;
    }

    // Print the node info.
    //
    printf( "Node: '%s' type: %s\n", name.c_str(), typeStr.c_str() );
  }

  return 0;
}

//*****************************************************************************/
//
// Filename     importOpenClips.C
//
// Description  Wiretap SDK sample program to import an Open clip.
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
#include <string>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <unistd.h>

int main( int argc, char **argv)
{
  std::string hostname = "localhost";
  std::string parentNodeId;
  std::string directory;

  int c;
  extern char *optarg;
  while ( ( c = getopt(argc, argv, "h:n:d:") ) != -1 ) {
    switch (c) {
      case 'h':
        hostname = optarg;
        break;
      case 'n':
        parentNodeId = optarg;
        break;
      case 'd':
        directory = optarg;
        break;
    }
  }


  // Initialize the Wiretap Client API.
  //
  WireTapClient wireTapClient;
  if ( !wireTapClient.init() ) {
    printf( "Unable to initialize WireTap client API.\n" );
    return 1;
  }

  // Instantiate a gateway server handle.
  //
  WireTapServerId gatewayServerId( "Gateway", hostname.c_str() );
  WireTapServerHandle gatewayServer( gatewayServerId );

  // Instantiate a gateway directory node handle.
  //
  WireTapNodeHandle directoryNode( gatewayServer, directory.c_str() );

  // Instantiate an IFFFS server handle.
  //
  WireTapServerId ifffsServerId( "IFFFS", hostname.c_str() );
  WireTapServerHandle ifffsServer( ifffsServerId );

  // Instantiate a clip node handle for the given server and node ID.
  //
  WireTapNodeHandle parentNode( ifffsServer, parentNodeId.c_str() );

  // Loop thru all directory node children and import all clip nodes.
  //
  unsigned numChildren = 0;
  if ( !directoryNode.getNumChildren( numChildren ) ) {
    printf( "Unable to obtain number of children: %s\n",
            directoryNode.lastError() );
    return 1;
  }

  for ( unsigned child = 0; child < numChildren; ++ child ) {
    // Get the child node.
    //
    WireTapNodeHandle childNode;
    directoryNode.getChild( child, childNode );

    // Get the child node type
    //
    WireTapStr childType;
    if ( !childNode.getNodeTypeStr( childType ) ) {
      printf( "Unable to obtain node type: %s\n", childNode.lastError() );
      return 1;
    }

    // Ignore non clip children
    //
    if ( strcmp( childType.c_str(), "CLIP" ) != 0 ) {
      continue;
    }

    WireTapStr clipName;
    if ( !childNode.getDisplayName( clipName ) ) {
      printf( "Unable to obtain node display name: %s\n", childNode.lastError() );
      return 1;
    }

    WireTapStr sourceData;
    if ( !childNode.getMetaData( "SourceData",  // stream name
                                 0,             // filter
                                 0,             // depth
                                 sourceData ) ) // metadata
    {
      printf( "Unable to obtain node source data: %s\n", childNode.lastError() );
      return 1;
    }
    
    // Define a clip format. The parameter allow the server to determine the
    // source information to import.
    //
    WireTapClipFormat format;
    format.setMetaDataTag( "SourceData" );
    format.setMetaData( sourceData );

    // Create a new node of type "CLIP" (a node type defined by 
    // the IFFFS Wiretap Server).  Each Wiretap server defines a set of 
    // node types (specified as string constants).
    //
    WireTapNodeHandle clipNode; 
    if ( !parentNode.createClipNode( clipName,    // display name 
                                     format,      // clip format 
                                     "CLIP",      // node type (server-specific)
                                     clipNode ) ) // created node returned here 
    { 
      printf( "Unable to create clip node: %s.\n", parentNode.lastError() ); 
      return 1;
    }
    
    printf( "Imported '%s' to '%s'\n", clipName.c_str(), clipNode.getNodeId().id() );
  }

  return 0;
}


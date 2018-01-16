//*****************************************************************************/
//
// Filename     duplicateNode.C
//
// Description  Wiretap SDK sample program to duplicate a node.
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.
//
//*****************************************************************************/

#include "WireTapClientAPI.h"
#include <cstdlib>
#include <cstdio>
#include <string>

#include <cstring>

namespace
{
   // Global variables.
   // Default "localhost" will work for hostName if a Wiretap server 
   // is running on your machine.
   // 
   const char *hostEnv = getenv( "WIRETAP_HOST" );
   const char *hostName = hostEnv == 0 ? "localhost" : hostEnv;
   const char *srcNodeId = getenv( "WIRETAP_SRC_NODE_ID" );
   const char *dstNodeId = getenv( "WIRETAP_DST_NODE_ID" );

   int duplicateNode( WireTapNodeHandle & srcNode,
                      WireTapNodeHandle & dstParentNode )
   {
      WireTapStr srcDisplayName;
      if ( !srcNode.getDisplayName( srcDisplayName ) )
      {
        printf( "Unable to duplicate node: %s\n",
                srcNode.lastError() );
        return 1;
      }

      std::string displayName = std::string( "Duplicate of " )
                              + std::string( srcDisplayName.c_str() );

      WireTapNodeHandle newNode;
      if ( !dstParentNode.duplicateNode( srcNode,
                                         displayName.c_str(),
                                         newNode ) )
      {
        printf( "Unable to duplicate node: %s\n",
                 dstParentNode.lastError() );
        return 1;
      }

      return 0;
   }
}

int main( int argc, char **argv) 
{
   // Initialize the Wiretap Client API.
   //
   WireTapClient wireTapClient;
   if ( !wireTapClient.init() )
   {
      printf( "Unable to initialize WireTap client API.\n" );
      return 1;
   }

   if ( srcNodeId == 0 || dstNodeId == 0 )
   {
      printf( "Must specify source and destination node ids\n" );
      return 1;
   }

   // Instantiate server handles.
   //
   WireTapServerId serverId( "IFFFS", hostName );
   WireTapServerHandle server( serverId );

   // Instantiate node handles for the source node and the destination parent
   // node.
   //
   WireTapNodeHandle srcNode( server, srcNodeId );
   WireTapNodeHandle dstParentNode( server, dstNodeId );

   if ( !duplicateNode( srcNode,
                        dstParentNode ) )
   {
      return 1;
   }
   
   printf( "Operation successful.\n" );

   return 0;
}

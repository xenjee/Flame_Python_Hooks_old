//*****************************************************************************/
//
// Filename     copyProject.C
//
// Description  Wiretap SDK sample program to copy a project subtree (but not
//              its clip libraries). 
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.
//
//*****************************************************************************/

// Please refer to the Wiretap SDK document for an explanation of the project
// node hierarchy.

#include "WireTapClientAPI.h"
#include <stdlib.h>
#include <stdio.h>
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
   const char *srcProjectNodeId = "/stonefs/OldProject";
   const char *dstProjectParentNodeId = "/stonefs";
   const char *newProjectName = "NewProject";

   // Recursive function to copy a project hierarchy.  If the name of the new
   // node is specified, use it. Otherwise, use the name of the source.
   // Note: We do NOT copy clip libraries.
   //
   bool copyProjectHierarchy( WireTapServerHandle& srcServer,
                              WireTapNodeHandle& srcNode,
                              WireTapServerHandle& dstServer,
			      WireTapNodeHandle& dstParentNode, 
                              const char *newDisplayName = 0 )
   {
      // Retrieve source node display name and type.  These will be used to
      // create the destination node.
      //
      WireTapStr typeStr, name;
      if ( !srcNode.getDisplayName( name ) ) {
         printf( "Unable to get display name: %s.", srcNode.lastError() );
	 return false;
      }
      if ( !srcNode.getNodeTypeStr( typeStr ) ) {
         printf( "Unable to get node type: %s.", srcNode.lastError() );
	 return false;
      }

      // Skip clip libraries.
      //
      if ( strcmp( typeStr, "LIBRARY" ) == 0 ) {
         return true;
      }

      printf( "Copying node: '%s' type: %s.\n", name.c_str(), typeStr.c_str() );

      // If a new node name is specified, use it; 
      // otherwise the source display name is used.
      //
      if ( newDisplayName != 0 ) {
         name = newDisplayName;
      }
      
      // Create node on destination server with the required name and type.
      //
      WireTapNodeHandle dstNode;
      if ( !dstParentNode.createNode( name.c_str(), typeStr.c_str(), dstNode ) )
      {
         printf( "Unable to create node: %s.\n", dstParentNode.lastError() );
         return false;
      }
   
      // Project nodes may have an associated data stream.  Call getStreamId()
      // to retrieve stream id for this node.
      //
      WireTapStr srcStreamId, dstStreamId;
      if ( !srcNode.getStreamId( srcStreamId ) ||
           !dstNode.getStreamId( dstStreamId ) )
      {
         printf( "Unable to get stream Id: %s.\n", srcNode.lastError() );
         return false;
      }

      // Check if this node has stream.  An empty stream ID ("") signifies
      // that there is no data stream.  If it has a stream, copy it.
      // A stream may be the content of a setup file.
      //   
      if ( srcStreamId.length() != 0 && dstStreamId.length() != 0 ) {
      
         // Pull the node's data stream into a temporary file.
         //
         const char *tmpFileName = "data.tmp";
         if ( !srcServer.pullStream( srcStreamId.c_str(), tmpFileName ) ) {
            printf( "Unable to read stream: %s.\n", srcServer.lastError() );
            return false;
         }
      
         // Push the stream stored in the temporary file to the newly 
         // created node.
         //
         if ( !dstServer.pushStream( dstStreamId, tmpFileName ) )  {
            printf( "Unable to write stream: %s\n.", dstServer.lastError() );
            return false;
         }
      }
   
      // Now, iterate across all children of the source node and recusively 
      // copy.
      //
      unsigned numChildren = 0;
      if ( !srcNode.getNumChildren( numChildren ) ) {
         printf( "Unable to obtain number of children: %s\n", 
                 srcNode.lastError() );
         return false;
      }
      for ( unsigned i = 0; i < numChildren; i++ )
      {
         // Get the child node 
         //
         WireTapNodeHandle child;
         srcNode.getChild( i, child );

         // Copy child node and its children
         //
         if ( !copyProjectHierarchy( srcServer, child, dstServer, dstNode ) ) {
            return false;
         }
      }

      // After we have successfully copied the project, set its metadata to
      // match the source
      //
      if ( strcmp( typeStr, "PROJECT" ) == 0 )  {
        WireTapStr metadata;
        if ( !srcNode.getMetaData( "XML", "", 1 , metadata ) ) {
          printf( "Unable to retrieve meta data: %s\n", srcNode.lastError() );
          return false;
        }

        if ( !dstNode.setMetaData( "XML", metadata ) ) {
          printf( "Unable to set meta data: %s\n", dstNode.lastError() );
          return false;
        }
      }

      return true;
   }
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

   // Instantiate server handles. 
   // For this example, copy the project to the same server.
   //
   WireTapServerId serverId( "IFFFS", hostName );
   WireTapServerHandle srcServer( serverId );
   WireTapServerHandle dstServer( serverId );

   // Instantiate node handles for the source project node and the parent
   // of the destination project to be created.
   //
   WireTapNodeHandle srcProjectNode( srcServer, srcProjectNodeId );
   WireTapNodeHandle dstParentNode( dstServer, dstProjectParentNodeId );

   // Recursively create and copy the source project and its hierarchy.
   //
   if ( !copyProjectHierarchy( srcServer, 
                               srcProjectNode, 
                               dstServer,
                               dstParentNode,
                               newProjectName ) )
   {
      return 1;
   }
   
   printf( "Operation successful.\n" );

   return 0;
}

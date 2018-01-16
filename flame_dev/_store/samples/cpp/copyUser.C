//*****************************************************************************/
//
// Filename     copyUser.C
//
// Description  Wiretap SDK sample program to copy a user subtree (including
//              user preferences). 
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.
//
//*****************************************************************************/

// Please refer to the Wiretap SDK document for an explanation of the user node
// hierarchy.

#include "WireTapClientAPI.h"
#include <stdlib.h>
#include <stdio.h>
#include <string>

namespace
{
   // Global variables.
   // Default "localhost" will work for hostName if a Wiretap server 
   // is running on your machine.
   // 
   const char *hostEnv = getenv( "WIRETAP_HOST" );
   const char *hostName = hostEnv == 0 ? "localhost" : hostEnv;
   const char *srcUserNodeId = "/stonefs/users/editing/OldUser";
   const char *dstUserParentNodeId = "/stonefs/users/editing";
   const char *newUserName = "NewUser";

   // Recursive function to copy a user hierarchy.  If the name of the new
   // node is specified, use it. Otherwise, use the name of the source.
   //
   bool copyUserHierarchy( WireTapServerHandle& srcServer,
                           WireTapNodeHandle srcNode,
                           WireTapServerHandle &dstServer,
			   WireTapNodeHandle dstParentNode, 
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

       printf( "Copying node: '%s' type: %s.\n", name.c_str(), 
             typeStr.c_str() );
  
       // If a new node name is specified, use it; 
       // otherwise the source display name is used.
       //
       if (newDisplayName != 0 ) {
          name = newDisplayName;
       }
      
       // Create node on destination server with the required name and type.
       //
       WireTapNodeHandle dstNode;
       if ( !dstParentNode.createNode( name.c_str(),typeStr.c_str(),dstNode ) )
       {
          printf( "Unable to create node: %s.\n", dstParentNode.lastError() );
          return false;
       }
   
       // User nodes may have an associated data stream.  Call getStreamId()
       // to retrieve stream id for this node.
       //
       WireTapStr srcStreamId, dstStreamId;
       if ( !srcNode.getStreamId( srcStreamId ) ||
	    !dstNode.getStreamId( dstStreamId )
       ){
          printf( "Unable to get stream Id: %s.\n", srcNode.lastError() );
          return false;
       }

       // Check if this node has stream.  An empty stream ID ("") signifies
       // that there is no data stream.  If it has a stream, copy it.
       //   
       if ( srcStreamId.length() != 0 && dstStreamId.length() != 0 ) {
      
          // Pull the node's data stream into a temporary file.
          // This stream may be the content of a user preference file.
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
             printf( "Unable to write stream: %s.\n", dstServer.lastError() );
             return false;
          }
       }
   
       // Now, iterate across all children of the source node and recusively 
       // copy.
       //
       unsigned numChildren = 0;
       if ( !srcNode.getNumChildren( numChildren ) ) {
          printf( "Unable to obtain number of children: %s.\n", 
                srcNode.lastError() );
          return false;
       }
       for ( unsigned i = 0; i < numChildren; i++ )
       {
          // Get the child node 
          //
          WireTapNodeHandle child;
          srcNode.getChild( i, child );

          // Copy child node and his children
          //
          if ( !copyUserHierarchy( srcServer, child, dstServer, dstNode ) ) {
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

   // Instantiate server handles.  For now, copy the user to the same server.
   //
   WireTapServerId serverId( "IFFFS", hostName );
   WireTapServerHandle srcServer( serverId );
   WireTapServerHandle dstServer( serverId );

   // Instantiate node handles for the source user node and the parent of
   // the destination user to be created.
   //
   WireTapNodeHandle srcUserNode( srcServer, srcUserNodeId );
   WireTapNodeHandle dstParentNode( dstServer, dstUserParentNodeId );

   // Recursively create and copy the source user and its hierarchy.
   //
   if ( !copyUserHierarchy( srcServer, 
                            srcUserNode, 
                            dstServer,
                            dstParentNode,
                            newUserName ) )
   {
      return 1;
   }
   
   printf( "Operation successful.\n" );

   return 0;
}

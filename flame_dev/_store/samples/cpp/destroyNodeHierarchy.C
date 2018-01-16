//*****************************************************************************/
//
// Filename     destroyNodeHierarchy.C
//
// Description  Wiretap sample to destroy node hierarchy from a specific node.
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
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <cstring>

namespace  {
   const char *hostEnv = getenv( "WIRETAP_HOST" );
   const char *hostName = hostEnv == 0 ? "localhost" : hostEnv;
}

bool destroyNodeHierarchy( WireTapNodeHandle destroyNode);


int main( int argc, char **argv)
{
   // Give the path of parent node to destroy node under.
   //
   WireTapStr destroyNodeAndNodeUnder = "/stonefs/NewProject";

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

   // Instantiate the node handle for the given server and node ID.
   //
   WireTapNodeHandle parent( server, destroyNodeAndNodeUnder.c_str() );

   // Call function that delete all children of the parent node and 
   // finally delete the parent node.
   //
   if ( !destroyNodeHierarchy( parent ) ) {
      printf( "Unable to delete node: %s.\n", parent.lastError() );
      return 1;
   }
   
   printf( "Node %s and his children has been deleted !\n", 
         destroyNodeAndNodeUnder.c_str() );

   return 0;
}


// Call function that delete all children of the parent node and 
// finally delete the parent node because all children must be 
// delete before parent.
//
bool destroyNodeHierarchy( WireTapNodeHandle destroyNode)
{
   // Retrieve how many child node as this node
   //
   unsigned numChildren = 0;
   if ( !destroyNode.getNumChildren( numChildren ) ) {
      printf( "Unable to obtain number of children: %s.\n", 
            destroyNode.lastError());
      return false;
   }

   // Retrieve node type to check if it's a library.
   //
   WireTapStr typeStr;
   if ( !destroyNode.getNodeTypeStr(typeStr) ) {
      return false;
   }
   
   // If it's a library, we don't automatically delete media 
   //
   if ( strcmp( "LIBRARY", typeStr.c_str() ) != 0 ) {
      WireTapNodeHandle child;
      for ( unsigned i = 0; i < numChildren; i++ ) {
      
         // Retrieve the child node 
         //
         destroyNode.getChild( i, child );

         // Destroy child node and his children
         //
         if ( !destroyNodeHierarchy( child ) ) {
            return false;
         }
      }
   }
   
   // Retrive node name to display
   //
   WireTapStr name;
   if (!destroyNode.getDisplayName( name ) ) {
      return false;
   }
   printf( "Destroy node: '%s' type: %s, \n.", name.c_str(), 
         typeStr.c_str() );

   // Destroy node 
   //
   if ( !destroyNode.destroyNode() ) {
      printf( "Unable to destroy the node: %s.\n", 
            destroyNode.lastError() );
      return false;
   }
   return true;
}

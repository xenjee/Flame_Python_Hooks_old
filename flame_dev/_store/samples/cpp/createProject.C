//*****************************************************************************/
//
// Filename     createProject.C
//
// Description  Wiretap SDK sample program to create an empty project node and
//              set its metadata.
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
// Please see the Wiretap Developer's Guide for an explanation of the 
// project node hierarchy.
// 
// NOTE: To create a new project with a complete setup hierarchy, copy a project 
// created in an IFFFS application (see the copyProject.cpp sample program).
//
// LOCATION OF PROJECT DTD:
// <INSTALLATION_PATH>/xml/<wiretapversion>/dtd/project.dtd
//
// LOCATION OF PROJECT SCHEMA: 
// <INSTALLATION_PATH>/xml/<wiretapversion>/schema/project.xsd
// 

#include <WireTapClientAPI.h>
#include <stdlib.h>
#include <stdio.h>

namespace 
{
  // Global variables.  Get values from environment variables if available.
  // Defaults ("localhost" for hostName and "stonefs" for parentNodeId)
  // will work if a Wiretap server is running on your machine.
  // 
  const char *hostEnv = getenv( "WIRETAP_HOST" );
  const char *hostName = hostEnv == 0 ? "localhost" : hostEnv;
  const char *parentNodeIdEnv = getenv( "WIRETAP_PARENT_NODE_ID" );  
  const char *parentNodeId = parentNodeIdEnv == 0 ?
    "/stonefs" :  parentNodeIdEnv;
  const char *projectNameEnv = getenv( "WIRETAP_PROJECT_NAME" );
  const char *projectName = projectNameEnv == 0 ? "testProject" :projectNameEnv; 
}

    
int main(int argc, char** argv )
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
  
  // Instantiate the project node 
  // 
  WireTapNodeHandle parentNode( server, parentNodeId );
  WireTapNodeHandle projectNode;
  
  // Create the project node. 
  // This will just create a project database entry. It will be empty.
  // No setup hierarchy will be created beneath it.
  // 
  if ( !parentNode.createNode( projectName, "PROJECT", projectNode ) ){
    printf( "Unable to create project node: %s\n", parentNode.lastError() );
    return 1;
  }
  else {
    printf( "Project node created.\n" );
  }
  
  // Prepare project metadata stream in XML format.
  // Frame parameters: 1920x1080, 12-bit unpacked depth, aspect ratio 1.7778.
  // Proxies are conditional (determined by setting ProxyEnable to false and 
  // ProxyMinFrameSize to a value > 24). 
  // Proxies will be generated for images whose width > 720.
  // Proxy width is 0.2 * width of the clip resolution. Proxy depth is 8 bits.
  // Proxy quality is 'medium'.
  // The project scan format is set to PROGRESSIVE.
  // 
  WireTapStr metadata = 
    "<Project>"
    "<Description>Test setting project metadata</Description>"
    "<FrameWidth>1920</FrameWidth>"
    "<FrameHeight>1080</FrameHeight>"
    "<FrameDepth>12-bit u</FrameDepth>"
    "<AspectRatio>1.7778</AspectRatio>"
    "<ProxyEnable>false</ProxyEnable>"
    "<ProxyWidthHint>0.2</ProxyWidthHint>"
    "<ProxyDepthMode>8-bit</ProxyDepthMode>"
    "<ProxyMinFrameSize>720</ProxyMinFrameSize>"
    "<ProxyAbove8bits>false</ProxyAbove8bits>"
    "<ProxyQuality>medium</ProxyQuality>"
    "<FieldDominance>PROGRESSIVE</FieldDominance>"
    "</Project>";
    
  // Set the project meta data
  // 
  if ( !projectNode.setMetaData( "XML", metadata ) ){
    fprintf(stderr, "Error setting project metadata : %s\n",
	    projectNode.lastError() );
    return 1;     
  }
  else {
    fprintf(stderr, "Project set metadata successful.\n" );
  }

  return 0;
  
}

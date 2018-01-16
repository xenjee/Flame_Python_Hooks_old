//*****************************************************************************/
//
// Filename     submitjob.C
//
// Description  WireTap SDK sample program to submit a backburner job.
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
#include <string>

int main( int argc, char **argv)
{
  // Initialize the Wiretap Client API.
  //
  WireTapClient wireTapClient;
  if ( !wireTapClient.init() ) {
    printf( "Unable to initialize WireTap client API.\n" );
    return 1;
  }

  // Instantiate a handle to the Backburner manager.  We are connecting to 
  // the BackBurner database, which we specify via a WireTapServerId.
  //
  WireTapServerHandle bbManager( 
      	 WireTapServerId( "Backburner", argc <= 1 ? "localhost" : argv[1] ) );
  
  // Create the job node.  The resulting node is an empty job in the suspended
  // state.  It is automatically tagged with the current user and host names. 
  //
  WireTapNodeHandle parentNode( bbManager, "/jobs" );
  WireTapNodeHandle jobNode;
  if ( !parentNode.createNode( "My job name", "JOB", jobNode ) ) {
    printf( "Cannot create job: %s\n", parentNode.lastError() );
    return 1;
  }

  // A job has basic metadata that must first be populated via an XML metadata
  // stream.
  //
  std::string jobInfo;

  // The job description is typically a one-line entry, but can be longer. 
  // Newlines are allowed, but are not necessary.
  //
  jobInfo += "<description>This is the description of my job.</description>\n";

  // A job is made up of tasks (i.e. sub-jobs) which define the granularity of
  // the job.  Blocks of tasks can be delegated to multiple servers by the
  // manager in any order it sees fit.  The number of tasks is specific to the
  // job type and it details (see below).  Some jobs have hundreds of tasks,
  // while others have only one (the default value)
  //
  jobInfo += "<numTasks>10</numTasks>\n";

  // The servers tag determines the list of servers that are eligible to
  // process tasks of a job.  An empty server list tells the manager that the
  // job can run on any/all eligible servers.
  //
  jobInfo += "<servers>hostname1,hostname2</servers>\n";

  // A job is assigned to a specific plug-in (or renderer).  The manager will
  // use the plug-in name to determine which servers are eligible to handle a
  // given job.  The name of the plug-in must be an exact match.  If required,
  // plug-in version information can be stored in the details section.
  //
  jobInfo += "<pluginName>MyBBPlugin</pluginName>\n";

  // A job's priority within the queue is given as an integer value between 0
  // and 100, with 100 representing the lowest priority.  The default priority
  // (if unspecified) is 0.
  //
  jobInfo += "<priority>50</priority>\n";

  // Apply the basic job metadata using the job's "info" stream.
  //
  if ( !jobNode.setMetaData( "info", jobInfo.c_str() ) ) {
    printf( "Cannot set job info: %s\n", jobNode.lastError() );
    jobNode.destroyNode();
    return 1;
  }

  // This sample program does not come with a plug-in; it simply submits a
  // dummy job.  At this point, specific job details related to the plug-in
  // would be required (in XML format).  For the purpose of the example, a
  // dummy stream is passed in using the "details" stream name.
  //
  const char *jobDetails = "<MyJobDetails>bla bla bla</MyJobDetails>";
  if ( !jobNode.setMetaData( "details", jobDetails ) ) {
    printf( "Cannot set job details: %s\n", jobNode.lastError() );
    jobNode.destroyNode();
    return 1;
  }

  // Some jobs will have large attachments that must be transferred to the
  // manager, and then passed onto the render nodes.  WireTap provides a
  // stream API for this purpose.  The stream API provides a high-bandwidth
  // out-of-phase connection to the WireTap server which will not block
  // concurrent metadata and node hierarchy requests.
  //
  // The WireTap stream API requires a unique stream identifier in order to
  // work.  Job nodes come with a pre-defined (unique) stream identifier
  // reserved for attachment data.  The identifier is simply the job node ID.
  //
  // Normally, attachment data is stored in a local file.  The stream API will
  // read the data from the specified file.  It is suggested to compress the
  // local file prior to sending.  This will greatly speed up the transfer,
  // reduce the storage requirements on the manager, and will improve
  // scalability.
  //
  const char *attachmentFile = "test.zip";
  if ( !bbManager.pushStream( jobNode.getNodeId().id(), attachmentFile ) ) {
    printf( "Cannot set send attachment file: %s\n", bbManager.lastError() );
    jobNode.destroyNode();
    return 1;
  }

  // Now that the job has been successfully set up, set its state to "waiting"
  // so that the manager can delegate it to a server.  Recall that the job
  // node was initially / implicitly created in the "suspended" state.  This
  // same mechanism can be used to suspend or activate the job at any time.
  //
  if ( !jobNode.setMetaData( "state", "waiting" ) ) {
    printf( "Cannot set job state: %s\n", jobNode.lastError() );
    jobNode.destroyNode();
    return 1;
  }

  printf("Successfully submitted job %s\n", jobNode.getNodeId().id()  );
 
  return 0;
}

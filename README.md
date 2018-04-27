# README
GNU General Public license v3.0.

————————————————————————————————————————————————

Also look in the wiki section for Scripts Flowgraph, Screengrabs ...

————————————————————————————————————————————————

The ‘flame_dev’ folder contains all scripts and infos in subfolders.
Place it anywhere on your system and add the "_python" subfolder to your env PATH:
Something like this (on mac): 
export DL_PYTHON_HOOK_PATH=/opt/flame_dev/_python, or export DL_PYTHON_HOOK_PATH=/var/tmp/_python ...

List of folders and files contained in ‘flame_dev’:

- _python
- _ _init__.py (double '_' formating issue)
- _shared	
- house_projects
- README_INFOS
- test_init_file_for_path.py

————————————————————————————————————————————————

FLAME CUSTOM HOOKS and APPs
- Custom export.
- Config yaml Files (x3):
	- ProjectPaths_config_result (+ _Layout .py)
	- InfoStaff_config_result (+ _Layout .py)
	- ExportPresets_result (+ _Layout .py)

- Custom UI Action Apps

OTHER APPS/UTILITIES
- Snippets: 
	- Duplicate with input connections
	- Matte Cleaner Snippet/module/ gizmo
	- Back to Beauty (reconstructs a CG beauty pass using render layers)
- Save and Reload Selection (and run snippets from there as well)
- Toolkit (expressions cheatsheet ...)

WIRETAP TESTS SCRIPTS
- Copy clip's path to clipboard (From Lewis Saunders)
- Clip Metadata (From Michael Tailor)
- Wiretap test prints: print hostname, list servers, Create timeline. (From Autodesk? Sorry, need to dig in, i don't remember who/where i got this from)



————————————————————————————————————————————————

Paths

- The hooks are loaded if the path is declared in the OS environment: 
example:
~/.bash_profile
export DL_PYTHON_HOOK_PATH=/opt/flame_dev/_python
export DL_DEBUG_PYTHON_HOOKS=1

> export_hook_custom.py is now (for me) in /opt/flame_dev/_python
> Debug mode is on

————————————————————————————————————————————————

ToDo:
Hmmm ...

————————————————————————————————————————————————

FEATURE REQUESTS To Autodesk: 
- provide a ‘clipName’ key for preCustomExport.
- Allow Subfolders to the Custom export menu (like CustomUIaction groups?)
- A way to sort the list of export presets

————————————————————————————————————————————————

Questions:

- many

————————————————————————————————————————————————

Reminders: 

- On macOS, CTF files must be copied into /Applications/Autodesk/Synergy/SynColor/Shared/transforms
- On Linux it's in opt/autodesk/synergy/syncolor ... (not in front now, but it should be close, sorry)

These export presets use a set of Custom CTFs. 
All CTF stacks use a conversion to ACES as a connecting space for the first step, then go down to whatever needed.
The Ones …_to_Video are also the ones used for viewing rules.

————————————————————————————————————————————————

UPDATES:

20180426:
- Trying to make _python the top module.
- Added a _init__.py root in _python containing a def to get the absolute part of paths further used.
- modified all scripts so every path is a combination of what "def get_absolute_path_part():" returns and various combined relative paths.
The whole thing should now be more portable, simply adding the path to _python to the env PATH

20180416:
- Added a flowgraph to the wiki, for the Snippets Apps. 
- Updated the Readme file.

20180115:
- Updated the folder structure and root path to /opt/flame_dev/
- Added batch functions/scripts/snippets (python API)

20170909:
- Project path and name now open showing the actual configuration as opposed to the default placeholder
- added export presets to /flame/adsk_share/export/presets/sequence_publish > these presets must be copied in opt/autodesk/shared/export/presets/sequence_publish

20170521:
- Reload the previous (last) state? (reload fields values) > done
- Add export path to email content (text)
- Export presets, profiles … are now dependent on the various .yaml config files (3 files)
- Available export presets are now defined in the ExportPresets TAB in the QT APP. (Which is defined/created in CustomUIAction.py)

20170418:
- Print info dictionaries from within each hook > >>
	for k, v in info.iteritems():
           	print "%-24s: %s" % (k, v)

20170415:
- Send email when export done: postCustomExport  (using smtplib)

20170414:
- Added browse and display ‘ complete path’ (for project’s root path)
- Added browse and display ‘project’  (project folder = name)

20170412:
- In the UI app: added placeholders and defaults for value fields (path, project, names, emails)
 



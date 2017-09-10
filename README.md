# README
The 'flame' folder is for Autodesk Flame python hooks
Place it in /var/tmp/
Read the readme files inside the 'README_INFOS' folder.

xenjee@gmail.com


FLAME CUSTOM HOOKS

- Custom export
- Custom UI Action
- Config yaml Files (x3):
	. ProjectPaths_config_result (+ _Layout .py)
	. InfoStaff_config_result (+ _Layout .py)
	. ExportPresets_result (+ _Layout .py)

————————————————————————————————————————————————

If you got this as a completely package:

The ‘flame’ folder contains all scripts in subfolders.
Copy this folder in /var/tmp/

List of folders contained in ‘flame’:

- adsk_python
- adsk_shared
- house_projects
- README_INFOS
- yaml_to_copy


Copy yaml folder 
from: 
/usr/local/lib/python2.7/site-packages/yaml 
to:
/opt/Autodesk/python/2018.1.prxx/lib/python2.7/


The config .yaml files are saved by the QT APP (which is created in CustomUIAction.py) available in Flame, in the contextual menu.

————————————————————————————————————————————————

Paths

- The hooks are loaded if the path is declared in the OS environment: 
example:
~/.bash_profile
export DL_PYTHON_HOOK_PATH=/var/tmp/flame/adsk_python
export DL_DEBUG_PYTHON_HOOKS=1

> export_hook_custom.py is now (for me) in /var/tmp/flame/adsk_python
> Debug mode is on

————————————————————————————————————————————————

ToDo:

CONFIG
- Add a behavior if value field not filled properly (no real entry’, not an email @ format …) > if not test.strip(): print “empty!!!” thingy.
- Ability to add lines for more individuals (name + email)? ("add" button)
- In export_hook_custom >  somewhat make the path to the .yaml config more ‘relative’ or extracted from reading in the OS filesystem. (Less hardcoded) >> ‘yaml_config_Path’ would be extracted rather than hardcoded

HOOK
- FEATURE REQUEST: provide a ‘clipName’ key for preCustomExport.

————————————————————————————————————————————————

Questions:

- Can we add a comment lines (PyYaml) to the generated .yaml file?

————————————————————————————————————————————————

Reminders: 
- On macOS, CTF files must be copied into /Applications/Autodesk/Synergy/SynColor/Shared/transforms
- On Linux it's in ... (don't remember right now)

————————————————————————————————————————————————

Updates:

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
 




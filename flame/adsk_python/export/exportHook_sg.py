# CUSTOM EXPORT HOOK for Autodesk Flame.
# Adds export options (list) to the contextual (right click) menu inside Flame (right click on a clip, but not in batch flowgraph)
# Many thanks to Bob Maple, Vlad Bakic, Tommy hooper, Lewis Sanders and Tommy Furukawa for their Time, explanations, patience, pieces of code and overall kindness!
# The rest is still a base in developement. Alpha stage per say.
# @ Stefan Gaillot - xenjee@gmail.com
# Date: 20170509

# -----------------------------------------------------------------

# Hooks in this files are called in the following order:
# preCustomExport ( optional depending on getCustomExportProfiles )
#  preExport
#   preExportSequence
#    preExportAsset
#    postExportAsset  ( could be done in backburner depending of useBackburnerPostExportAsset )
#    ...
#   postExportSequence
#   ...
#  postExport
# postCustomExport ( optional depending on getCustomExportProfiles  )

# -----------------------------------------------------------------

# A class(export_settings) is created to gather successive hook functions infos and use them later in the script.

# -----------------------------------------------------------------

# ------------- Scripts names, order and connexions ---------------
# Please open the pdf scripts flowgraph that should be part of this zip or github package: ProjectPaths_config_result.yaml
# -----------------------------------------------------------------

# Import 'os' and module for filesystem access
import os
import yaml
import smtplib


# --------------
# IMPORT YAML CONFIG FILES>

# >>>>>>>>>>>>>>>> HARDCODED PATH for yaml file !!! >>>>>>>>>>>>>>>>>>>>

yaml_Pathnames_Path = '/var/tmp/flame/adsk_python/apps/utilities/ProjectPaths_config_result.yaml'
yaml_Staff = '/var/tmp/flame/adsk_python/apps/utilities/InfoStaff_config_result.yaml'
yamlGmail = '/Users/stefan/Dropbox/STEF/yaml_gmail/yamlGmail.yaml'
yaml_export_presets = '/var/tmp/flame/adsk_python/apps/utilities/ExportPresets_result.yaml'

with open(yaml_Pathnames_Path, 'r') as config1:
    cfg1 = yaml.load(config1)

with open(yaml_Staff, 'r') as config2:
    cfg2 = yaml.load(config2)

with open(yamlGmail, 'r') as config3:
    cfg3 = yaml.load(config3)

with open(yaml_export_presets, 'r') as config4:
    cfg4 = yaml.load(config4)

# PROJECT INFOS:
projects_root_path = cfg1["projects_root_path"]
project_name = cfg1["project_name"]
export_path = projects_root_path + '/' + project_name

# Project's STAFF: Names and emails
project_lead_name = cfg2["staff"]["project_lead"]["name"]
project_lead_email = cfg2["staff"]["project_lead"]["email"]
producer_name = cfg2["staff"]["producer"]["name"]
producer_email = cfg2["staff"]["producer"]["email"]

# email infos. Private info is kept in a seperate .yaml file, saved somewhere else on the system.
# Keep this private and add encryption to the process for safety.
passmot = cfg3["whatIneed"]

# Export Presets (path and name) from yaml config File (ExportPresets_result.yaml)
# later used to define what which export preset is available in from the contextual menu (custom exports)
# Also used to define profiles in 'getCustomExportProfiles' function.
# Also used for emails parametres. 
export_preset01_name = cfg4["export_preset01"]["name"]
export_preset01_path = cfg4["export_preset01"]["path"]
export_preset02_name = cfg4["export_preset02"]["name"]
export_preset02_path = cfg4["export_preset02"]["path"]
export_preset03_name = cfg4["export_preset03"]["name"]
export_preset03_path = cfg4["export_preset03"]["path"]
export_preset04_name = cfg4["export_preset04"]["name"]
export_preset04_path = cfg4["export_preset04"]["path"]
export_preset05_name = cfg4["export_preset05"]["name"]
export_preset05_path = cfg4["export_preset05"]["path"]

# TEST YAMLs config input'sinput PRINTS to Flame shell.
print '-' * 80
print 'In CustomExport Hook:'
print '-'
print 'YAML config PRINTS:'
print '-' * 5
print 'Network Projects root path: ' + projects_root_path
print 'Network Project name: ' + project_name
print 'Network Export path: ' + export_path
print '-' * 5
print 'STAFF: '
print 'Project lead: ' + project_lead_name + ', ' + project_lead_email
print 'Producer: ' + producer_name + ', ' + producer_email
print '-' * 5
# USING ExportPresets_result.yaml created by 'ExportPresetsTab' class in CustomUIAction_utilities.py
print 'Export Presets, from ExportPresets_result.yaml: '
print 'Name - Path to .ctf >'
print export_preset01_name + ' - ' + export_preset01_path
print export_preset02_name + ' - ' + export_preset02_path
print export_preset03_name + ' - ' + export_preset03_path
print export_preset04_name + ' - ' + export_preset04_path
print export_preset05_name + ' - ' + export_preset05_path
print '-' * 5

# END IMPORT YAML CONFIG
# --------------


# --------------
# Initialize and Project change (literraly when switching projects) >

# Store the loaded project name
def appInitialized(projectName):
    global globFlameProject
    globFlameProject = projectName

# Do the same in projectChanged


def projectChanged(projectName):
    global globFlameProject
    globFlameProject = projectName

# END - Initialize and Project change
# --------------


# --------------
# CREATE Global Object >
# There (settings) to store later pass infos from preExportAsset - info['resolvedPath'] and info['namePattern']

class export_settings(object):
    pass


print '-' * 80
print 'export setting object class created:' ' class export_settings(object): ... settings = export_settings()'
settings = export_settings()
print '-' * 80

# END - CREATE Global Object
# --------------


# --------------
# Add Export Profiles in menu ... >

# Add some custom export profiles to the contextual menu
# 'exportType' will be called later and assiociated with an export preset.

# profiles is a dictionary
# Profile's values (see below) come from the variables earlier assigned to ExportPresets_result.yaml imported values.
# Ordering is a mystery so far

def getCustomExportProfiles(profiles):
    profiles[export_preset02_name] = {'exportType': export_preset02_name}
    profiles[export_preset01_name] = {'exportType': export_preset01_name}
    profiles[export_preset03_name] = {'exportType': export_preset03_name}
    profiles[export_preset04_name] = {'exportType': export_preset04_name}
    profiles[export_preset05_name] = {'exportType': export_preset05_name}


# END - Add Export Profiles
# --------------


# --------------
# preCustomExport >

def preCustomExport(info, userData):  # info and userData are dictionaries
    global globFlameProject

    print '-' * 50
    print "From globFlameProject: Current Flame Project is: " + globFlameProject
    print '-' * 50

    # Setup some default properties all exports will share
    # Override as desired in any given 'if' statement for a particular preset
    info['useTopVideoTrack'] = True
    info['isBackground'] = True
    info['exportBetweenMarks'] = False

    # Destination: root part of where the clip will be exported. the rest of the path is defined in the export preset itself.
    info['destinationPath'] = export_path + '/'
    print export_path + '/'

    # Make sure the destination directory exists and make it if not,
    if not os.path.exists(info['destinationPath']):
        os.makedirs(info['destinationPath'])

    # Figure out which custom export menu was called and chose the corresponding Export Preset: ExportPresets_result.yaml
    # the rest of the destination path in set in the export preset using tokens.
    if userData['exportType'] == export_preset02_name:
        info['presetPath'] = export_preset02_path

    elif userData['exportType'] == export_preset01_name:
        info['presetPath'] = export_preset01_path

    elif userData['exportType'] == export_preset03_name:
        info['presetPath'] = export_preset03_path

    elif userData['exportType'] == export_preset04_name:
        info['presetPath'] = export_preset04_path

    elif userData['exportType'] == export_preset05_name:
        info['presetPath'] = export_preset05_path

    print '-' * 50
    print "Selected Profile is " + userData['exportType']
    print "Destination Path: " + info['destinationPath']
    print '-' * 50

# END - preCustomExport
# --------------


# --------------
# SEQUENCE & ASSETS PUBLISH >
# Prints only, to show what they can pass.

def preExportSequence(info, userData):
    # PRINT # - from Tommy H
    print '-' * 50
    print 'Within preExportSequence ------- for k, v in info.iteritems(): print "%-24s: %s" % (k, v)'
    for k, v in info.iteritems():
        print "%-24s: %s" % (k, v)
    print '-' * 50


def preExportAsset(info, userData):
    # PRINT #
    print '-' * 50
    print 'Within preExportAsset ------- for k, v in info.iteritems(): print "%-24s: %s" % (k, v)'
    for k, v in info.iteritems():
        print "%-24s: %s" % (k, v)
    print '-' * 50

    settings.export_filePath = info['resolvedPath']
    settings.name_pattern = info['namePattern']


def postExportAsset(info, userData):
    pass


def postExportSequence(info, userData):
    pass

# END SEQUENCE & ASSETS PUBLISH
# --------------


# --------------
# postCustomExport: EMAILS >

def postCustomExport(info, userData):

    # ### ------ UNSECURED TEMP WAY (I beleive) - for internal dev only -------

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # >>>>>> ToDo: search for non TLS emails
    server.login("xenjee@gmail.com", passmot)

    # Using ExportPresets_result.yaml extracted values again. 
    # Subjects and Text are Attached as a header

    if userData['exportType'] == export_preset01_name:
        SUBJECT = "[SHOT EXPORTS]"

    elif userData['exportType'] == export_preset02_name:
        SUBJECT = "[SHOT EXPORTS]"

    elif userData['exportType'] == export_preset03_name:
        SUBJECT = "[SHOT EXPORTS]"

    elif userData['exportType'] == export_preset04_name:
        SUBJECT = "[POSTING]"

    elif userData['exportType'] == export_preset05_name:
        SUBJECT = "[POSTING]"

    TEXT = projects_root_path + project_name + settings.export_filePath

    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    if userData['exportType'] == export_preset01_name:
        server.sendmail(project_lead_email, project_lead_email, msg)
        server.quit()

    elif userData['exportType'] == export_preset02_name:
        server.sendmail(project_lead_email, project_lead_email, msg)
        server.quit()

    elif userData['exportType'] == export_preset03_name:
        server.sendmail(project_lead_email, project_lead_email, msg)
        server.quit()

    elif userData['exportType'] == export_preset04_name:
        server.sendmail(producer_email, producer_email, msg)
        server.quit()

    elif userData['exportType'] == export_preset05_name:
        server.sendmail(producer_email, producer_email, msg)
        server.quit()


# END EMAIL
# --------------

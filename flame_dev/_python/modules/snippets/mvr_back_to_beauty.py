
def main(shotname, elementname):
    shot_name = shotname
    element_name = elementname
    print ''
    print "RUNNING SNIPPET = CG SLAPCOMP = Back to beauty"
    print ''

    import flame

    ###########################################################################
    #            PART 1 - import modules and declare global variables
    ###########################################################################

    # 1. Exposing modules to python
    # import modules from a specific place (VFX pipeline's central folder for all python modules)
    global sys
    import sys
    # sys.path.append('/Users/stefan/XenDrive/___VFX/DEV/PYTHON/Modules/')

    # now we can import the modules previously declared as global (Because of the exec function behaviour)
    global os
    import os
    global clique
    import clique

    # turn the relative __file__ value into it's full path
    absolute_path = os.path.realpath(__file__)
    # Use the os module to split the filepath using '/' as a seperator to creates a list from which we pick IDs []
    root_path = '/'.join(absolute_path.split('/')[0:-4])
    # navigate down to the desired folder
    sys.path.append("{root}/_python/modules".format(root=root_path))
    print "{root}/_python/modules".format(root=root_path)

# Declare global variables: PROJECT NAME + SHOT NUMBER
    global projectName
    projectName = '17P998_python_console'

    global shotNumber
    shotNumber = str(shot_name)
    global passElement
    passElement = str('_' + element_name)
    print "shot number and name from CG_slapcomp.py: -> "
    print shotNumber
    print passElement

    ###########################################################################
    #            PART 2 - Create batch group
    ###########################################################################

    print "current project: " + flame.project.current_project.project_name

    schematicReels = ['CG_passes', 'Plates']  # create/name schematic reels
    shelfReels = ['Misc', ]  # create/name shelf reels

    # Create batch group
    flame.batch.create_batch_group(shotNumber + '_' + 'Vray_BackToBeauty',
                                   start_frame=1001,
                                   duration=5,
                                   reels=schematicReels,
                                   shelf_reels=shelfReels)

    # use this command to switch to the batch tab
    flame.batch.go_to()

    ###########################################################################
    #            PART 3 - get list and import clips from in-house jobs' structure
    ###########################################################################

    # 2. For iterating through all shot folders that have images in the lighting folder
    # This will get all shots and should perform a little better than using glob, which might not have great performance.
    global get_shot_folders

    def get_shot_folders(project_name):
        all_paths = []
        #project_root = r'/opt/flame_dev/house_projects/{project_name}/shots'.format(project_name=project_name)
        # NEXT TIME TRY THIS >>>>>>>>>>>>>>
        project_root = "{root}/house_projects/{project_name}/shots".format(root=root_path, project_name=project_name)

        print "From_mvr_back_to_beauty >Project's root 'shots' folder on server: " + project_root
        print ''
        print 'FILES FOUND (Filepaths): '

        for sequence in os.listdir(project_root):
            sequence_root = os.path.join(project_root, sequence)
            if os.path.isdir(sequence_root):
                for shots in os.listdir(sequence_root):
                    renders_root = os.path.join(sequence_root, shots, 'img/output/3D/lighting')
                    if os.path.isdir(renders_root):
                        all_paths.append(renders_root)
        return all_paths

    # > 3. Iterating through all the files in all subfolders in a specific path

    global get_all_files

    def get_all_files(path, ext=None):
        filepaths = []

        for parent, flds, files in os.walk(path):
            for file in files:
                if ext == None or file.endswith(ext):
                    filepath = os.path.join(parent, file)
                    filepaths.append(filepath)
        return filepaths

    # 4. Using previous functions to iterate through a specific folder and load all the frames to create clips

    def get_flame_clip_paths(path, ext=None):
        clip_paths = []
        collections, remainder = clique.assemble(
            get_all_files(path, ext=ext),
            patterns=[clique.PATTERNS['frames']],
            minimum_items=1
        )

        for collection in collections:

            start = min(collection.indexes)
            end = max(collection.indexes)

            clip_path = collection.head + '[{start}-{end}]'.format(start=str(start).zfill(collection.padding), end=str(end).zfill(collection.padding)) + collection.tail
            clip_paths.append(clip_path)
        return clip_paths

    # get_flame_clip_paths('/var/tmp/flame/house_projects/17P998_python_console/shots/STF/STF_0010/img/output/3D/lighting')
    for root in get_shot_folders(projectName):

        for path in get_flame_clip_paths(root, ext='exr'):
            # limit to one shot for now and therefore only build one batchgroup.
            if shotNumber in path:
                if passElement in path:
                    flame.batch.import_clip(path, "CG_passes")
                    print path

    ###########################################################################
    #                PART 4 - Do something with imported clips
    ###########################################################################

    # Organize/layout clips ==>>> That's what needs to be replaced with:
    # - clip names variables extracted from file names,
    # - a pre-defined nodes layout and connections based on file names' tokens

    # Initiate variables for CG render passes
    beauty_pass = ''
    diffuse_pass = ''
    reflection_pass = ''
    refraction_pass = ''
    specular_pass = ''
    AO_pass = ''
    Zdepth_pass = ''
    shadow_pass = ''
    normal_pass = ''
    uv_pass = ''
    sss_pass = ''
    GI_pass = ''
    lighting_pass = ''
    alpha_pass = ''
    selfIllumination_pass = ''
    caustics_pass = ''

    # Assign variables to returned files (passes)
    # Main passes
    for clip in flame.batch.nodes:
        if "beauty" in clip.name.get_value():
            beauty_pass = clip
            beauty_pass.pos_x = 0
            beauty_pass.pos_y = -200

    for clip in flame.batch.nodes:
        if "diffuse" in clip.name.get_value():
            diffuse_pass = clip
            diffuse_pass.pos_x = 0
            diffuse_pass.pos_y = 0

    for clip in flame.batch.nodes:
        if "reflect" in clip.name.get_value():
            reflection_pass = clip
            reflection_pass.pos_x = 0
            reflection_pass.pos_y = 450

    for clip in flame.batch.nodes:
        if "refract" in clip.name.get_value():
            refraction_pass = clip
            refraction_pass.pos_x = 0
            refraction_pass.pos_y = 900

    for clip in flame.batch.nodes:
        if "specular" in clip.name.get_value():
            specular_pass = clip
            specular_pass.pos_x = 0
            specular_pass.pos_y = 1350

    # Secondary passes
    for clip in flame.batch.nodes:
        if "AO" in clip.name.get_value():
            AO_pass = clip
            AO_pass.pos_x = 2600
            AO_pass.pos_y = 1600

    for clip in flame.batch.nodes:
        if "Zdepth" in clip.name.get_value():
            Zdepth_pass = clip
            Zdepth_pass.pos_x = 3400
            Zdepth_pass.pos_y = 1000

    # Extra passes
    for clip in flame.batch.nodes:
        if "normals" in clip.name.get_value():
            normal_pass = clip
            normal_pass.pos_x = 0
            normal_pass.pos_y = 2200

    for clip in flame.batch.nodes:
        if "UV" in clip.name.get_value():
            UV_pass = clip
            UV_pass.pos_x = 0
            UV_pass.pos_y = 2350

    for clip in flame.batch.nodes:
        if "worldposition" in clip.name.get_value():
            position_pass = clip
            position_pass.pos_x = 0
            position_pass.pos_y = 2500

    for clip in flame.batch.nodes:
        if "GI" in clip.name.get_value():
            GI_pass = clip
            GI_pass.pos_x = 0
            GI_pass.pos_y = 2650

    for clip in flame.batch.nodes:
        if "SSS" in clip.name.get_value():
            SSS_pass = clip
            SSS_pass.pos_x = 0
            SSS_pass.pos_y = 2800

    for clip in flame.batch.nodes:
        if "selfIllum" in clip.name.get_value():
            selfIllumination_pass = clip
            selfIllumination_pass.pos_x = 0
            selfIllumination_pass.pos_y = 2950

    for clip in flame.batch.nodes:
        if "shadow" in clip.name.get_value():
            shadow_pass = clip
            shadow_pass.pos_x = 0
            shadow_pass.pos_y = 3100

    for clip in flame.batch.nodes:
        if "caustics" in clip.name.get_value():
            caustics = clip
            caustics.pos_x = 0
            caustics.pos_y = 3250

    for clip in flame.batch.nodes:
        if "Alpha" in clip.name.get_value():
            alpha = clip
            alpha.pos_x = 0
            alpha.pos_y = 3400

    for clip in flame.batch.nodes:
        if "lighting" in clip.name.get_value():
            lighting_pass = clip
            lighting_pass.pos_x = 0
            lighting_pass.pos_y = 3550

    for clip in flame.batch.nodes:
        if "cryptomatte" in clip.name.get_value():
            cryptomatte_pass = clip
            cryptomatte_pass.pos_x = 0
            cryptomatte_pass.pos_y = 3700

    ###########################################################################
    #                PART 5 - add other nodes: mux, cc, comp, dof, writeFIle ...
    ###########################################################################

    mux_diffuse = flame.batch.create_node("Mux")
    mux_diffuse.name = "mux_diffuse"
    mux_diffuse.pos_x = 300
    mux_diffuse.pos_y = 0

    mux2_diffuse = flame.batch.create_node("Mux")
    mux2_diffuse.name = "mux_diffuse"
    mux2_diffuse.pos_x = 1750
    mux2_diffuse.pos_y = 0

    mux_reflection = flame.batch.create_node("Mux")
    mux_reflection.name = "mux_reflection"
    mux_reflection.pos_x = 300
    mux_reflection.pos_y = 450

    mux_refraction = flame.batch.create_node("Mux")
    mux_refraction.name = "mux_refraction"
    mux_refraction.pos_x = 300
    mux_refraction.pos_y = 900

    mux_specular = flame.batch.create_node("Mux")
    mux_specular.name = "mux_specular"
    mux_specular.pos_x = 300
    mux_specular.pos_y = 1350

    mux_torender = flame.batch.create_node("Mux")
    mux_torender.name = "mux_to_render"
    mux_torender.pos_x = 4300
    mux_torender.pos_y = 1350

    cc_diffuse = flame.batch.create_node("Colour Correct")
    cc_diffuse.name = "cc_diffuse"
    cc_diffuse.pos_x = 1000
    cc_diffuse.pos_y = 0
    # print cc_diffuse.type
    # print cc_diffuse.attributes
    # cc_diffuse.master.saturation.set_value(200)
    # cc_diffuse.master_saturation.set_value("200")

    # for n in flame.batch.nodes:
    #    if n.name == "cc_diffuse":
    #        n.flame_master_saturation = "200"

    cc_reflections = flame.batch.create_node("Colour Correct")
    cc_reflections.name = "cc_reflections"
    cc_reflections.pos_x = 1000
    cc_reflections.pos_y = 450

    cc_refraction = flame.batch.create_node("Colour Correct")
    cc_refraction.name = "cc_refraction"
    cc_refraction.pos_x = 1000
    cc_refraction.pos_y = 900

    cc_specular = flame.batch.create_node("Colour Correct")
    cc_specular.name = "cc_specular"
    cc_specular.pos_x = 1000
    cc_specular.pos_y = 1350

    cc_AO = flame.batch.create_node("Colour Correct")
    cc_AO.name = "cc_AO"
    cc_AO.pos_x = 2900
    cc_AO.pos_y = 1600

    cc_Zdepth = flame.batch.create_node("Colour Correct")
    cc_Zdepth.name = "cc_Zdepth"
    cc_Zdepth.pos_x = 3730
    cc_Zdepth.pos_y = 1000

    comp_reflection = flame.batch.create_node("Comp")
    comp_reflection.name = "comp_reflection"
    comp_reflection.flame_blend_mode = "Add"
    comp_reflection.pos_x = 1800
    comp_reflection.pos_y = 450

    comp_refraction = flame.batch.create_node("Comp")
    comp_refraction.name = "comp_reflection"
    comp_refraction.flame_blend_mode = "Add"
    comp_refraction.pos_x = 1850
    comp_refraction.pos_y = 900

    comp_specular = flame.batch.create_node("Comp")
    comp_specular.name = "comp_reflection"
    comp_specular.flame_blend_mode = "Add"
    comp_specular.pos_x = 1900
    comp_specular.pos_y = 1350

    comp_AO = flame.batch.create_node("Comp")
    comp_AO.name = "comp_AO"
    comp_AO.flame_blend_mode = "Multiply"
    comp_AO.pos_x = 2960
    comp_AO.pos_y = 1350

    dof = flame.batch.create_node("Depth Of Field")
    dof.name = "dof"
    dof.pos_x = 3800
    dof.pos_y = 1350

    ##############################
    # Write file
    ##############################

    # Path & name + position
    writeFile01 = flame.batch.create_node("Write File")
    writeFile01.name = "<batch name>"
    writeFile01.pos_x = 4600
    writeFile01.pos_y = 1350
    # media
    writeFile01.media_path = "/opt/flame_dev/house_projects/17P998_python_console/shots/STF/"
    writeFile01.media_path_pattern = shotNumber + "/img/output/2D/flame/renders/<batch iteration>/<batch iteration>."
    writeFile01.frame_padding = 4
    writeFile01.file_type = 'OpenEXR'
    writeFile01.format_extension = 'exr'
    writeFile01.bit_depth = '16 bit fp'
    # open clip
    writeFile01.create_clip = True
    writeFile01.create_clip_path = "./" + shotNumber + "/img/output/2D/flame/clip/<name>"
    # Setup
    writeFile01.include_setup = True
    writeFile01.include_setup_path = "./" + shotNumber + "/img/output/2D/flame/setups/<batch iteration>"
    # range
    writeFile01.range_start = 1001
    writeFile01.range_end = 1003

    writeFile01.version_mode = "Follow Iteration"
    writeFile01.version_padding = 3

    ###########################################################################
    #                PART 6 - Create compass areas
    ###########################################################################

    compass01 = flame.batch.create_node("Compass")
    compass01.name = "main_passes"
    compass01.width = 700
    compass01.height = 2300
    compass01.pos_x = -200
    compass01.pos_y = -400

    compass02 = flame.batch.create_node("Compass")
    compass02.name = "color_tweaks"
    compass02.width = 600
    compass02.height = 2300
    compass02.pos_x = 700
    compass02.pos_y = -400

    compass03 = flame.batch.create_node("Compass")
    compass03.name = "comp_passes"
    compass03.width = 600
    compass03.height = 2300
    compass03.pos_x = 1500
    compass03.pos_y = -400

    compass04 = flame.batch.create_node("Compass")
    compass04.name = "AO"
    compass04.width = 750
    compass04.height = 2300
    compass04.pos_x = 2350
    compass04.pos_y = -400

    compass04 = flame.batch.create_node("Compass")
    compass04.name = "DOF"
    compass04.width = 800
    compass04.height = 2300
    compass04.pos_x = 3200
    compass04.pos_y = -400

    compass05 = flame.batch.create_node("Compass")
    compass05.name = "writeFile"
    compass05.width = 550
    compass05.height = 2300
    compass05.pos_x = 4200
    compass05.pos_y = -400

    compass06 = flame.batch.create_node("Compass")
    compass06.name = "extra_passes"
    compass06.width = 700
    compass06.height = 2000
    compass06.pos_x = -200
    compass06.pos_y = 2050

    # Encompass all other comapsses (and therefore all nodes)
    compass07 = flame.batch.encompass_nodes([compass01, compass02, compass03, compass04, compass05, compass06])
    compass07.name = "CG_element_01"

    ###########################################################################
    #                PART 7 - Connections ?
    ###########################################################################

    # Clips to IN mux
    flame.batch.connect_nodes(diffuse_pass, shotNumber + passElement + ".diffuse.0001_ABGR", mux_diffuse, "Input_0")
    flame.batch.connect_nodes(reflection_pass, shotNumber + passElement + ".reflect.0001_ABGR", mux_reflection, "Input_0")
    flame.batch.connect_nodes(refraction_pass, shotNumber + passElement + ".refract.0001_ABGR", mux_refraction, "Input_0")
    flame.batch.connect_nodes(specular_pass, shotNumber + passElement + ".specular.0001_ABGR", mux_specular, "Input_0")

    # In mux to CC
    flame.batch.connect_nodes(mux_diffuse, "Result", cc_diffuse, "Front")
    flame.batch.connect_nodes(mux_reflection, "Result", cc_reflections, "Front")
    flame.batch.connect_nodes(mux_refraction, "Result", cc_refraction, "Front")
    flame.batch.connect_nodes(mux_specular, "Result", cc_specular, "Front")

    # comp passes
    flame.batch.connect_nodes(cc_diffuse, "Result", mux2_diffuse, "Input_0")
    flame.batch.connect_nodes(mux2_diffuse, "Result", comp_reflection, "Back")
    flame.batch.connect_nodes(cc_reflections, "Result", comp_reflection, "Front")
    flame.batch.connect_nodes(comp_reflection, "Result", comp_refraction, "Back")
    flame.batch.connect_nodes(cc_refraction, "Result", comp_refraction, "Front")
    flame.batch.connect_nodes(comp_refraction, "Result", comp_specular, "Back")
    flame.batch.connect_nodes(cc_specular, "Result", comp_specular, "Front")

    # AO pass, cc and comp
    flame.batch.connect_nodes(AO_pass, shotNumber + passElement + ".AO.0001_ABGR", cc_AO, "Front")
    flame.batch.connect_nodes(comp_specular, "Result", comp_AO, "Back")
    flame.batch.connect_nodes(cc_AO, "Result", comp_AO, "Front")

    # Depth of field
    flame.batch.connect_nodes(comp_AO, "Result", dof, "Front")
    flame.batch.connect_nodes(Zdepth_pass, shotNumber + passElement + ".Zdepth.0001_ABGR", cc_Zdepth, "Front")
    flame.batch.connect_nodes(cc_Zdepth, "Result", dof, "Z-Depth")

    # To render
    flame.batch.connect_nodes(dof, "Result", mux_torender, "Input_0")
    flame.batch.connect_nodes(mux_torender, "Result", writeFile01, "Front")

    ###########################################################################
    #                PART 8 - Batch display
    ###########################################################################

    flame.batch.frame_all()

    ###########################################################################
    #                PART 9 - render
    ###########################################################################

    flame.batch.render("Foreground", 0, 0)

import os


def get_absolute_path_part():

    # turn the relative __file__ value into it's full path
    absolute_path = os.path.realpath(__file__)

    # the full path contains this file which we don't want, we just want it's path
    # use the os module to split the filepath using '/' as a seperator. This creates a list from which we
    # chose what elements we'll joint back together:
    module_path = '/'.join(absolute_path.split('/')[0:-2])

    # see if we're matching our hard coded target
    auto_cfg_file = '%s/_python/__init__.py' % (module_path)

    print "FROM __init__:"
    print "  MODULE   PATH:", module_path
    print "  __INIT__ PATH:", auto_cfg_file

    return module_path

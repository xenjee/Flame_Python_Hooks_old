
import subprocess


def my_test_print():

    print "Test print: should come from the callback ('callback': _testprint) in Snippets_list_dict.py"
    print "It should also open a text file (Hard coded path)"

    file_path = '/Users/stefan/XenDrive/___VFX/FLAME_STUFF/FLAME_DEV/PYTHON/Hooks_dev/run_snippets_app/openMe.txt'

    subprocess.call(["open", file_path])

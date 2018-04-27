# inherit absolute part of the path from the __init__.py file
from __init__ import get_absolute_path_part
ROOT_PATH = get_absolute_path_part()

print ""
print "FROM test file:"
print "ROOT_PATH:", ROOT_PATH

print "Add custom path to ROOT_PATH:", "{root}/path/to/script".format(root=ROOT_PATH)

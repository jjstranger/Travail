import sys
getPythonPathEnv=sys.path
if trvScriptsPath not in getPythonPathEnv:
    sys.path.append(trvScriptsPath)
    print "Travail scripts path is added into system PYTHONPATH."
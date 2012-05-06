'''
All code copyleft (GNU GPL v3) by Unobtanium @ XBMC Forums
'''

#so that we can import stuff from parent of parent dir (settings)
import sys, os
sys.path.append( os.path.dirname( os.path.dirname( os.getcwd() ) ) )
import settings

import pysvn

# check if aggregate repo dir is already a git or svn repo
# if it is not make it an svn/git repo

# do a new commit and push of all files, also update remote repo with any deletions on local repo

def execute(): svn()

class svn:
    # uses pysvn as svn backend
    def __init__():
            pass


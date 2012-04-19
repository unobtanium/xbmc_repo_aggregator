'''
All code copyleft (GNU GPL v3) by Unobtanium @ XBMC Forums

Running settings.py on it's own enables limited error reporting on the settings.

You may want to change aggregate_repo_path to a publically accessable directory if you are hosting the repo
on your own server rather than uploading to somewhere via svn or git If you do so, you should also change the
push setting to None.

Note, repository aggregator ONLY produces repositories of COMPRESSED addons. You must make
sure the datadir zip parameter in your repository file is set to true.

'''
import os

# don't hack these values.
current_dir = os.getcwd()
version_number = '1.0'
compress_addons = True


# --------- Begin Repeater Settings ----------- #

### Repeater handles triggering the script every X minutes. Code for this is contained with execute.py

# Disable if you want to instead use CRON on your server to trigger the aggregator.
enable_repeat = False

# It is reccommended to keep this value above 3 minutes, so as to not use too much CPU / memory on host machine
mins_before_repeat = 3


# --------- Begin Merge Settings ------------- #

###  Merge handles pulls from the repositories you are merging into the local directory of your aggregate repo.

# Directory containing addons.xml and the results of aggregator.py
aggregate_repo_path = os.path.join( current_dir, 'aggregate-repo' )

# Directory containing all of the unzipped repository files of the repos whose content (addons) you wish to merge into your aggregate repo.
repo_sources_path = os.path.join( current_dir, 'repo-sources' )

# Used to solve conflicts between multiple repositories containing different (or the same) versions of the same addon.
# See README for documentation on how to use this.
merge_rules = {}


# --------- Begin Push Settings -------------- #

### Push handles syncing your repository to a remote server via svn or git.

# Disable pusher if you are hosting the repo on your own server.
enable_push = False

# Values are: 'svn' or 'git' 
push_type = 'svn'

# git or svn path that you have read/write permissions to, and where your repository will be uploaded to.
push_path = ''

# The commit note to use for every update
commit_note = " Auto synced by repository-aggregator v" + version_number


#---------End all settings. -------------------#

# Error reporting on settings.py
if __name__ == "__main__":
            if push_type is not ('svn' or 'git'):
                                raise Execption( 'The only valid setting for push_type is git or svn')

            if not os.path.exists( aggregate_repo_path ):
                                  raise Exception("Aggregate repository directory does not exist!")

            if not os.path.exists( repo_sources_path ):
                                  raise Exception("Repository source directory does not exist!")

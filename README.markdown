xbmc-repo-aggregator
====================

Server-like script capable of merging multiple xbmc repositories.

v1.0

Licensed under GNU GPL v3


Credits
-------

Thanks to the original unknown author of addons_xml_generator.py , whose code is used in repo-prep.py

All other code copyleft (GNU GPL v3) by Unobtanium @ XBMC Forums


Instructions
------------

To execute, run execute.py

You must adjust settings.py before executing.

If calling from another python script do this
'''python
import execute
execute.execute()
'''



Extra information about settings.py
------------------------------------

settings.py already contains extensive annotation for the various settings, but here is some more information for some settings.

__Merge Rules__

Within the rules dictionary, add a entry specifying:
key) name of the addon you want to solve the conflict for
value) name of the preferred repo you would like to pull it from

Example:

```python
rules = {
    
          'plugin.video.troublesomeaddon' : 'repository.preferredsource',
          'plugin.video.anothertroublesomeaddon' : 'repository.anotherpreferredsource'

        }
```
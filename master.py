'''
All code copyleft (GNU GPL v3) by Unobtanium @ XBMC Forums
'''
import time
import settings

import urllib
import random

from lib import merge
from lib import repo_prep

# The below is imported in _execute_aggregator()
# from lib import push

def execute():
    # wrap the actual executer with repeat function (if settings.py tells us to).   
    if settings.enable_repeat:
        
            # create infinite loop (repeater)
            x = 1
            while x == 1:
                    _wait_mins( settings.mins_before_repeat )
                    _execute_aggregator()
            
    else: _execute_aggregator()

def _execute_aggregator():
    # master function of the various scripts

    # only execute if we have a working internet connection.
    if _check_internet_connection():
    
                # if we made changes to the repo, then prep the repo and (if enabled) push
                if merge.execute():
                    
                            repo-prep.execute()
                            
                            if settings.enable_push:
                                        from lib import push
                                        push.execute()

def _check_internet_connection():
         urls = [         'google.com',
                                'facebook.com',
                                'youtube.com',
                                'yahoo.com',
                                'baidu.com',
                                'wikipedia.org',
                                'live.com',
                                'qq.com',
                                'twitter.com',
                                'blogspot.com',
                                'amazon.com',
                                'linkedin.com',
                                'google.co.in'
                          ]
         #this code block is run for the same number of times as urls in the url list.
         for x in urls:
            if urls:
                #choose a random url
                choice = random.choice( urls )
                url = 'http://www.' + choice
                
                try: u = urllib.urlopen( url )
                except:
                    #delete url from list so it is not tried again.
                    urls.remove(choice)
                    connected = False
                else:
                    connected = True
                    break
            else: break
         return connected
        
def _wait_mins( z ):
    time.sleep( z*60 )
    
if __name__ == "__main__": execute()

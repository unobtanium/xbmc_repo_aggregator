'''
All code copyleft (GNU GPL v3) by Unobtanium @ XBMC Forums
'''
import time
import settings

import urllib
import random

from lib import merge
from lib import repo-prep

# The below is imported in _execute_aggregator()
# from lib import push

def execute():
    # wrap the actual executer with repreat function.    
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
         urls = [         'www.google.com',
                                'www.facebook.com',
                                'www.youtube.com',
                                'www.yahoo.com',
                                'www.baidu.com',
                                'www.wikipedia.org',
                                'www.live.com',
                                'www.qq.com',
                                'www.twitter.com',
                                'www.blogspot.com',
                                'www.amazon.com',
                                'www.linkedin.com',
                                'www.google.co.in'
                          ]
         #this code block is run for the same number of times as urls in the url list.
         for x in urls:
            if urls:
                #choose a random url
                choice = random.choice( urls )

                #hit the choice
                try: u = urllib.urlopen( choice )
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

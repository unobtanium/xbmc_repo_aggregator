'''
All code copyleft (GNU GPL v3) by Unobtanium @ XBMC Forums

addons.xml and addons.md5 are downloaded direct to the repo folder, all addons are placed in one single folder.
'''

import settings
import os
import re
import urllib
import urlparse

class Merge:
        def __init__( self ):
                # Define the various variables used throughout the class.
                self.local_repo_path = None
                self.repo_name = None
                
                self.addon_xml_path = None
                self.addon_xml = None
                
                self.addons_xml_path = None
                self.addons_md5_path = None
                
                self.remote_addons_md5 = None
                
                self.addons_xml = None
                self.remote_addons_xml_raw = None
                

        def master( self ):
                # now start loop to perform these tasks for each repository
                repo_dir_contents = os.listdir( settings.repo_sources_path )
                
                for repo in repo_dir_contents:
                    
                            if not os.path.isfile(repo):
                                                                           
                                        # check that addon.xml exists, as a way to verify it is a repo file
                                        self.addon_xml_path = os.path.join( repo, 'addon.xml )
                                        if os.path.exists( self.addon_xml_path ):
                                    
                                                            # set the various variables we need to know
                                                            self.local_repo_path = repo
                                                            self.repo_name = str( (os.path.split( repo ) )[1] )                                                       
                                                            self.addons_xml_path = os.path.join( repo, 'addons.xml' )
                                                            self.addons_md5_path = os.path.join( repo, 'addons.xml.md5' )
                                        
                                                            # get the urls we need for the repository                                                                         
                                                            self._read_addon_xml()
                                                                                                               
                                                            # if we can find local md5, compare it to remote md5. if it has changed run the update checker.
                                                            if os.path.exists( self.addons_md5_path ):
                                                                            if self._has_md5_changed( self.addons_md5_path, (self.addon_xml)['md5'] ):
                                                                                            _handle_addon_updates()
                                                            
                                                            # If no md5, then we have to do a manual addons.xml compare every time we want to check for updates!!!
                                                            # This is also used if we haven't downloaded anything from this repo before.
                                                            else: _handle_addon_updates()
                                                                            

       def _handle_addon_updates():
                                updates = _create_list_of_updates()
                                # if there are updates, continue
                                if updates != False:
                                                # check if the repository packages it's addons as zips. use different methods depending on this.
                                                if self.addon_xml['datadirzip'] == True: self._download_compressed_updates( updates )
                                                else: self._download_uncompressed_updates( updates )
                                                                            
                                                # update local files (addons.xml and addons.xml.md5)
                                                self._create_file( self.addons_xml_path, self.remote_addons_xml_raw )
                                                self._create_file( self.addons_md5_path, self.remote_addons_md5 )

        def _download_uncompressed_updates ( updates ):
                                pass
                                # this is going to be difficult.
                                # How do we recursively download a directory of files from a http server when we do not know the names of those files and cannot walk the directory??!!
                                                                            
        def _download_compressed_updates ( updates ):
                                for key, value in updates:
                                                                # download directory for the addon.
                                                                addon_dir = os.path.join( settings.aggregate_repo_path, key )

                                                                base_url = urlparse.urljoin( self.addon_xml['datadir'], key )

                                                                # create the urls for the various files in the addon release directory.
                                                                zip_url = urlparse.urljoin( base_url, key + '-' + value + '.zip' )
                                                                xml_url = urlparse.urljoin( base_url, 'addon.xm')
                                                                changelog_url = urlparse.urljoin( base_url, 'changelog-'+value+'.txt' )
                                                                fanart_url = urlparse.urljoin( base_url, 'fanart.jpg' )
                                                                icon_url = urlparse.urljoin( base_url, 'icon.png' )

                                                                # These downloads are essential. Need to delete the whole addon folder if these files aren't downloaded.
                                                                if not self._download_file( addon_dir, zip_url  ):
                                                                            shutil.rmtree( addon_dir )
                                                                            break                                                                           
                                                                if not self._download_file(  addon_dir, xml_url ):
                                                                            shutil.rmtree( addon_dir )
                                                                            break

                                                                # These downloads are not so essential. Allow addon folder to continue existing if they fail.
                                                                self._download_file( addon_dir, changelog_url  )
                                                                self._download_file( addon_dir, fanart_url )
                                                                self._download_file( addon_dir, icon_url )
                                

        def _download_file( path, url ):
                        # download and also display a status bar for the download
                                                                            
                        file_name = url.split( '/' )[-1]
                        path = os.path.join( path, file_name )
                                                                            
                        u = urllib2.urlopen( url )
                        meta = u.info()
                                                                            
                        try: file_size = int( meta.getheaders( "Content-Length" )[0] )
                        except:
                                        print 'Download Failed: '+ file_name
                                        return False
                        else:
                                        # create the file and begin downloading.
                                                                            
                                         f = open( path, 'wb' )
                                                                            
                                        print "Downloading: %s Bytes: %s" % ( file_name, file_size )

                                        file_size_dl = 0
                                        block_sz = 8192
                                        while True:
                                                    buffer = u.read(block_sz)
                                                    if not buffer: break

                                                    file_size_dl += len( buffer )
                                                    f.write( buffer )
                                                    status = r"%10d  [%3.2f%%]" % ( file_size_dl, file_size_dl * 100. / file_size )
                                                    status = status + chr(8)*( len( status ) + 1 )
                                                    print status,

                                        f.close()
                                        return True
                                                                            
        def _create_list_of_updates( self ):
                                    try:
                                        self.remote_addons_xml_raw = urllib.urlopen( self.addons_xml_url ).read()
                                        remote = self._addons_xml_reader( self.remote_addons_xml_raw )
                                    except:
                                        print 'Could not access ' + self.repo_name + ' remote addons.xml! Skipping updates from this repository.'
                                        updates = False
                                    else:
                                                # if the local addons.xml exists (ie. repo has be), cross reference with the remote to find what has been updated.
                                                # take into account "rules" and also whether addon dir actually exists locally.
                                                if os.path.exists( self.addons_xml_path ):
                                                                local = self._addons_xml_reader( self._read_local_file( self.addons_xml_path ) )
                                                                updates = self._find_dfferences( local, remote )
                                                                self._delete_deprecated_addons( local, remote )
                                                                            
                                                # if we didn't find the local addons.xml , download all addons apart from those specified by rules.
                                                # addons.xml will only be present if this repo's content has already been downloaded.
                                                else: updates = self._add_addons_from_new_repo( remote )
                                                                                                                           
                                                # return a list of addon names to update. if no updates, return False
                                                return updates

                                                                                                                           
        def _add_addons_from_new_repo( self, remote ):
                                for key, value in remote:
                                                                            
                                                local_path = os.path.join( settings.aggregate_repo_path, key )
                                                downloaded = os.path.exists( ) )

                                                # if there is a rule for downloading this addon from a different repository, remove it from the update list.
                                                if self._dont_download_rule( key ): del remote[key]

                                return remote                                        
                                                                                                                          
        def _dont_download_rule( key ):                                                                          
                                #check if there is a rule for this addon, and whether it doesn't want it downloaded from this repo.
                                variable = False
                                has_rule = (settings.specify_repository_for_addon).has_key( key )                              
                                if has_rule:
                                                                            
                                                # check if rule doesn't want addon downloaded from this repo.
                                                if (settings.specify_repository_for_addon)[key] != ( self.repo_name ): variable = True

                               # check if user has specified a ban for this addon. 
                               has_ban = (settings.ban).has_key( key ) 
                               if has_ban: variable = True
                                                                            
                                return variable

        def _find_dfferences( self, local, remote ):
                        # Creates a dictionary of addons that we want to download from the server.
                        
                        updates = remote
                                                                            
                        # start going through the addons in the remote addons.xml
                        for key, value in remote:
  
                                        downloaded = os.path.exists( os.path.join( settings.aggregate_repo_path, key ) )

                                        # if there is a rule for downloading this addon from a different repository, remove it from the update list.
                                        if self._dont_download_rule( key ): del updates[key]
                                        else:                                                                           
                                                # if the addon exists locally and is not awaiting an update, remove it from the update list.                                                                         
                                                if local.has_key( key ) and downloaded:
                                                             if local[key] == value: del updates[key]                                                                                                                                                                                                                                                                                                                                                                                
                        return updates

        def _delete_deprecated_addons( self, local, remote ):
                         # This function also deletes deprecated addons that no longer exist on the server
                                                                                                                                        
                        for key, value in local:

                                        # If local addons.xml contains an addon that does not exist in the remote addons.xml continue.
                                        if key is not in remote:

                                                        # if rules specify this repo is its source, continue.
                                                        if not self._dont_download_rule( key ):
                                                                        local_path = os.path.join( settings.aggregate_repo_path, key )
                                                                        
                                                                        # delete the addon directory if it exists.
                                                                        if os.path.exists(local_path):
                                                                                        print 'Addon ' + (os.path.split( local_path ))[1] + ' has been deprecated! Deleting local file.'
                                                                                        shutil.rmtree( local_path )

        def _create_file( self, filepath, contents ):
                if os.path.exists( filepath ): os.remove( filepath )

                f = open( filepath, "w")
                f.write( contents.strip() )                       
                f.close()
                                                                            
       def _read_local_file( self , filepath ):
                  # check for addon.xml or addons.xml and try and read it.
                  if os.path.exists( filepath ):
                                     
                                # load whole text into string
                                f = open( filepath, "r")
                                contents = f.read()                       
                                f.close()

                                # return contents if we found and read the addon.xml 
                                return contents
                            
                  # return False if we couldn't  find the addon.xml 
                  else: return False

        def _has_md5_changed( self, local, remote ):
                if local == remote: return False
                else: return True
                
        def _addons_xml_reader( self, addons_xml ):
            # hacky regex's to read addons.xml
            
            # find the headers of the addon.s
            headers = re.compile( "\<addon (.+?)>", re.DOTALL ).findall( addons_xml )

            addons = {}
            for header in headers:
                              # clean line of quotation characters so that it is easier to read.
                              header = re.sub( '"','', header )
                              header = re.sub( "'",'', header )
                              
                              # scrape the version number from the line
                              addon_name = (( re.compile( "id\=(.+?) " , re.DOTALL ).findall( header ) )[0]).strip()

                              addon_version_number = (( re.compile( "version\=(.+?) " , re.DOTALL ).findall( header ) )[0]).strip()

                              # add the addon to the addon dict
                              addons[addon_name] = addon_version_number

            return addons

        def _read_addon_xml( self ):
                # hacky regex's to read addon.xml
                string = self._read_local_file( self.addon_xml_path )
                if string:
                                string = re.sub( '"','', string)
                                string = re.sub( "'",'', string)

                                string = (re.compile('\<extension point\=xbmc\.addon\.repository(.+?)\<\/extension\>', re.DOTALL).findall( string ))[0]

                                # now grab relevant values from addon.xml and save them as a dict
                                addons_xml = (re.compile('\<info(.+?)\<\/info\>', re.DOTALL).findall( string ))[0]
                                addons_xml = re.sub( ' compressed\=false\>' , '' , addons_xml )
                                addons_xml = re.sub( ' compressed\=true\>' , '' , addons_xml )

                                checksum = (re.compile('\<chec(.+?)\<\/checksum\>', re.DOTALL).findall( string ))[0]
                                checksum = re.sub( 'ksum\>' , '' , checksum )

                                datadir = (re.compile('\<datadir(.+?)\<\/datadir\>', re.DOTALL).findall( string ))[0]
                                
                                if 'zip=false>' in datadir: datadirzip = False
                                elif 'zip=true>' in datadir: datadirzip = True
                                
                                datadir = re.sub( ' zip\=false\>' , '' , datadir )
                                datadir = re.sub( ' zip\=true\>' , '' , datadir )


                                self.addon_xml = { 'addons.xml' : addons_xml.strip() , 'md5' : checksum.strip() , 'datadir' : datadir.strip() , 'datadirzip' : datadirzip }

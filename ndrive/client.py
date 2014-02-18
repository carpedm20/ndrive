# -*- coding: utf-8 -*-

"""
ndrive
======

ndrive is a Naver Ndrive wrapper for python

Getting started
---------------

    git clone https://github.com/carpedm20/pyndrive.git

Copyright
---------

Copyright 2014 Kim Tae Hoon

"""

import os, sys
import urllib2
import requests
import json
import magic
import datetime
import re

from .auth import naver_login
from .urls import ndrive_urls as nurls
from .utils import byte_readable

class ndrive(object):
    """
    This class lets you make Ndrive API calls. First, you need to 
    log in with Ndrive account or set NID_AUT and NID_SES manually.

    """
    debug = False

    # requests session
    # Cookies : NID_AUT, NID_SES, useridx
    session = requests.session()

    def __init__(self, debug = False, NID_AUT = None, NID_SES= None):
        """Initialize ``NdriveClient`` instance.

        Using given user information, login to ndrive server and create a session

        Args:
            NID_AUT: Naver account authentication info
            NID_SES: Naver account session info

        Returns:

        """
        self.debug = debug
        self.session.headers["User-Agent"] = \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) Chrome/32.0.1700.76 Safari/537.36"
        self.session.cookies.set('NID_AUT', NID_AUT)
        self.session.cookies.set('NID_SES', NID_SES)

    def login(self, user_id, password, svctype = "Android NDrive App ver", auth = 0):
        """Log in Naver and get cookie

        Agrs:
            user_id: Naver account's login id
            password: Naver account's login password

        Returns:
            True: Login success
            False: Login failed

        Remarks:
            self.cookie is a dictionary with 5 keys: path, domain, NID_AUT, nid_inf, NID_SES
        """
        self.user_id = user_id
        self.password = password

        if self.user_id == None or self.password == None:
            print "[*] Error __init__: user_id and password is needed"
            return False

        try:
            cookie = naver_login(user_id, password)
        except:
            return False

        self.session.cookies.set('NID_AUT', cookie["NID_AUT"])
        self.session.cookies.set('NID_SES', cookie["NID_SES"])

        s = self.getRegisterUserInfo(svctype, auth)

        if s is True:
            return True
        else:
            print "[*] Error getRegisterUserInfo: failed"
            return False

    def checkAccount(self):
        if self.useridx is None:
            return False, "Error checkStatus: useridx is not defined"
        elif self.user_id is None:
            return False, "Error checkStatus: userId is not defined"
        else:
            return True, None

    def GET(self, func, data):
        """GET http request to execute Ndrive API

        Args:
            func:
              The function name you want to execute in Ndrive API.
            params:
              Parameter data for HTTP request.

        Returns:
            metadata:
              Result of the function in dict form.
            False:
              Failed to execute Ndrive API function.
        """
        if func not in ['getRegisterUserInfo']:
            s, message = self.checkAccount()

            if s is False:
                return False, message

        url = nurls[func]
        r = self.session.get(url, params = data)

        if self.debug:
            print r.text

        try:
            try:
                metadata = json.loads(r.text)
            except:
                metadata = json.loads(r.text[r.text.find('{'):-1])

            message = metadata['message']
            if message == 'success':
                return True, metadata['resultvalue']
            else:
                return False, message
        except:
            for e in sys.exc_info():
                print e
            sys.exit(1)
            return False, "Error %s: Failed to send GET request" %func

    def POST(self, func, data):
        """POST http request to execute Ndrive API

        Args:
            func:
              The function name you want to execute in Ndrive API.
            params:
              Parameter data for HTTP request.

        Returns:
            metadata:
              Result of the function in dict form.
            False:
              Failed to execute Ndrive API function.
        """
        s, message = self.checkAccount()
        if s is False:
            return False, message

        url = nurls[func]
        r = self.session.post(url, data = data)

        if self.debug:
            print r.text.decode("unicode-escape").encode("utf-8")

        try:
            metadata = json.loads(r.text)
            message = metadata['message']
            if message == 'success':
                try:
                    return True, metadata['resultvalue']
                except:
                    return True, metadata['resultcode']
            else:
                return False, "Error %s: %s" %(func, message)
        except:
            #for e in sys.exc_info():
            #    print e
            #sys.exit(1)
            return False, "Error %s: Failed to send POST request" %func

    def getRegisterUserInfo(self, svctype = "Android NDrive App ver", auth = 0):
        """Retrieve information about useridx

        Args:
            svctype:
              Information about the platform you are using right now.
            auth:
              ???

        Returns:
            True:
              Success to get useridx
            False:
              Failed to get useridx

        """
        data = {'userid': self.user_id,
                'svctype': svctype,
                'auth': auth
               }

        s, metadata = self.GET('getRegisterUserInfo', data)

        if s is True:
            self.useridx = metadata['useridx']
            return True
        else:
            print metadata
            return False
            
    def checkStatus(self):
        """Check status

        Args:

        Returns:
            True:
              Sucess
            False:
              Failed

        """
        self.checkAccount()

        data = {'userid': self.user_id,
                'useridx': self.useridx
               }
        r = self.session.post(nurls['checkStatus'], data = data)

        p = re.compile(r'\<message\>(?P<message>.+)\</message\>')
        message = p.search(r.text).group('message')

        if message == 'success':
            return True
        else:
            return False

    def uploadFile(self, file_obj, full_path, overwrite = False):
        """Upload a file as Ndrive really do.

        Args:
            file_obj
              A file-like object to check whether possible to upload.
              You can pass a string as a file_obj or a real file object.
            full_path:
              The full path to upload the file to, *including the file name*.
              If the destination directory does not yet exist, it will be created.
                ex) /Picture/flower.png
            overwrite:
              Whether to overwrite an existing file at the given path. (Default ``False``.)

        Remarks:
            How Ndrive uploads a file to its server:
              1. POST /CheckStatus.ndrive
              2. POST /GetDiskSpace.ndrive
              3. POST /CheckUpload.ndrive
              4. PUT /FILE_PATH
              5. POST /GetList.ndrive
              6. POST /GetWasteInfo.ndrive
              7. POST /GetDiskSpace.ndrive
        """
        s = self.checkStatus()
        s = self.getDiskSpace()
        s = self.checkUpload(file_obj, full_path, overwrite)

        if s is True:
            self.put(file_obj, full_path, overwrite)

    def getDiskSpace(self):
        """Get disk space information.

        Returns:
            metadata:
              Disk information in DICT format

              - expandablespace
              - filemaxsize
              - largefileminsize
              - largefileunusedspace
              - largefileusedspace
              - paymentspace
              - totallargespace
              - totalspace
              - unusedspace
              - usedspace
        """
        data = {'userid': self.user_id,
                'useridx': self.useridx,
               }
        s, metadata = self.POST('getDiskSpace',data)

        if s is True:
            usedspace = byte_readable(metadata['usedspace'])
            totalspace = byte_readable(metadata['totalspace'])
            print "Capacity: %s / %s" % (usedspace, totalspace)

            return metadata
        else:
            print message

    def checkUpload(self, file_obj, full_path = '/', overwrite = False):
        """Check whether it is possible to upload a file.

        Args:
            file_obj
              A file-like object to check whether possible to upload.
              You can pass a string as a file_obj or a real file object.
            full_path: 
              The full path to upload the file to, *including the file name*.
              If the destination directory does not yet exist, it will be created.
                ex) /Picture/flower.png
            overwrite:
              Whether to overwrite an existing file at the given path. (Default ``False``.)
            
        Returns:
            True:
              Possible to upload a file with a given file_size
            False:
              Impossible to upload a file with a given file_size

        """
        try:
            file_obj = file_obj.name
        except:
            file_obj = file_obj # do nothing

        file_size = os.stat(file_obj).st_size
        now = datetime.datetime.now().isoformat()

        data = {'uploadsize': file_size,
                'overwrite': overwrite if 'T' else 'F',
                'getlastmodified': now,
                'dstresource': full_path,
                'userid': self.user_id,
                'useridx': self.useridx,
                }

        s, metadata = self.POST('checkUpload', data)

        if not s:
            print metadata

        return s

    def put(self, file_obj, full_path, overwrite = False):
        """Upload a file.

        Args:
            file_obj
              A file-like object to check whether possible to upload.
              You can pass a string as a file_obj or a real file object.
            full_path: 
              The full path to upload the file to, *including the file name*.
              If the destination directory does not yet exist, it will be created.
                ex) /Picture/flower.png

        Returns:
            True:
              Success to upload a file.
            False:
              Failed to upload a file.
        """
        try:
            file_obj = open(file_obj, 'r')
        except:
            file_obj = file_obj # do nothing

        content = file_obj.read()
        file_name = os.path.basename(full_path)

        now = datetime.datetime.now().isoformat()
        url = nurls['put'] + full_path

        if overwrite:
            overwrite = 'T'
        else:
            overwrite = 'F'

        headers = {'userid': self.user_id,
                   'useridx': self.useridx,
                   'MODIFYDATE': now,
                   'Content-Type': magic.from_file(file_obj.name, mime=True),
                   'charset': 'UTF-8',
                   'Origin': 'http://ndrive2.naver.com',
                   'OVERWRITE': overwrite,
                   'X-Requested-With': 'XMLHttpRequest',
                   'NDriveSvcType': 'NHN/DRAGDROP Ver',
        }
        r = self.session.put(url = url, data = content, headers = headers)
        message = json.loads(r.text)['message']

        if message != 'success':
            print "Error put: " + message
            return False
        else:
            print "Success put: " + file_obj.name
            return True

    def delete(self, full_path):
        """Delete a file in full_path

        Args:
            full_path: 
              The full path to delete the file to, *including the file name*.
                ex) /Picture/flower.png

        Returns:
            True:
              Success to delete the file
            False:
              Failed to delete the file
        """
        now = datetime.datetime.now().isoformat()
        url = nurls['delete'] + full_path

        headers = {'userid': self.user_id,
                   'useridx': self.useridx,
                   'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                   'charset': 'UTF-8',
                   'Origin': 'http://ndrive2.naver.com',
        }
        try:
            r = self.session.delete(url = url, headers = headers)
        except:
            print "Error delete: wrong full_path"
            return False

        message = json.loads(r.text)['message']

        if message != 'success':
            print "Error delete: " + message
            return False
        else:
            return True

    def getList(self, full_path, type = 1, dept = 0, sort = 'name', order = 'asc', startnum = 0, pagingrow = 1000, dummy = 56184):
        """Get a list of files

        Args:
            full_path: 
              The full path to get the file list.
                ex) /Picture/

            type: 1 => only directories with idxfolder property
                  2 => only files
                  3 => directories and files with thumbnail info
                      ex) viewHeight, viewWidth for Image file
                  4 => only directories except idxfolder
                  5 => directories and files without thumbnail info

            depth: Dept for file list
            sort: name => 이름
                  file => file type, 종류
                  length => size of file, 크기
                  date => edited date, 수정한 날짜
                  credate => creation date, 올린 날짜
                  protect => protect or not, 중요 표시

            order: Order by (asc, desc)
            startnum: ???
            pagingrow: start index ?
            dummy: ???

        Returns:
            List of dict:
              List of files for a path in dict form.
                ex)
                  [
                    {
                      u'copyright': u'N',
                      u'creationdate': u'2013-05-12T21:17:23+09:00',
                      u'filelink': None,
                      u'fileuploadstatus': u'1',
                      u'getcontentlength': 0,
                      u'getlastmodified': u'2014-01-26T12:23:07+09:00',
                      u'href': u'/Codes/',
                      u'lastaccessed': u'2013-05-12T21:17:23+09:00',
                      u'lastmodifieduser': None,
                      u'priority': u'1',
                      u'protect': u'N',
                      u'resourceno': 204041859,
                      u'resourcetype': u'collection',
                      u'sharedinfo': u'F',
                      u'sharemsgcnt': 0,
                      u'shareno': 0,
                      u'subfoldercnt': 5,
                      u'thumbnailpath': u'N',
                      u'virusstatus': u'N'
                    }
                  ]
            False:
              Failed to get list.
        """
        if type not in range(1, 6):
            print "Error getList: `type` should be between 1 to 5"
            return False
        data = {'orgresource': full_path,
                'type': type,
                'dept': dept,
                'sort': sort,
                'order': order,
                'startnum': startnum,
                'pagingrow': pagingrow,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
               }

        s, metadata = self.POST('getList', data)

        if s is True:
            return metadata
        else:
            print metadata
            return False

    def doMove(self, from_path, to_path, overwrite = False, bShareFireCopy = 'false', dummy = 56147):
        """Move a file.

        Args:
            from_path:
              The path to the file or folder to be moved.
            to_path:
              The destination path of the file or folder to be copied.
              File name should be included in the end of to_path.
                ex) /Picture/flower.png
            overwrite:
              Whether to overwrite an existing file at the given path. (Default ``False``.)
            bShareFireCopy:
              ???
            dummy:
              ???

        Returns:
            True:
              Success to move a file.
            False:
              Failed to move a file.
        """
        if overwrite:
            overwrite = 'F'
        else:
            overwrite = 'T'

        data = {'orgresource': from_path,
                'dstresource': to_path,
                'overwrite': overwrite,
                'bShareFireCopy': bShareFireCopy,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }

        s, metadata = self.POST('doMove', data)

        return s

    def makeDirectory(self, full_path, dummy = 40841):
        """Make a directory
        
        Args:
            full_path:
              The full path to get the directory property.
              Should be end with '/'.
                ex) /folder/

        Returns:
            True:
              Success to make a directory.
            False:
              Failed to make a directory.
        """
        if full_path[-1] is not '/':
            full_path += '/'

        data = {'dstresource': full_path,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }

        s, metadata = self.POST('makeDirectory', data)

        return s

    def makeShareUrl(self, full_path, passwd):
        """Make a share url of directory

        Args:
            full_path:
              The full path of directory to get share url.
              Should be end with '/'.
                ex) /folder/
            passwd:
              Access password for shared directory
        Returns:
            URL:
              share url for a directory
            False:
              Failed to share a directory
        """
        if full_path[-1] is not '/':
            full_path += '/'

        data = {'_callback': 'window.__jindo_callback._347',
                'path': full_path,
                'passwd': passwd,
                'userid': self.user_id,
                'useridx': self.useridx,
                }

        s, metadata = self.GET('shareUrl', data)

        if s:
            print "URL: %s" % (metadata['href'])
            return metadata['href']
        else:
            print "Error makeShareUrl: %s" % (metadata)
            return False

    def getFileLink(self, full_path):
        """Get a link of file
        
        Args:
            full_path:
              The full path of file to get file link
              Should be end with '/'.
                ex) /folder/
        Returns:
            URL:
              share url for a directory
            False:
              Failed to share a directory
        """
        prop = self.getProperty(full_path)

        if not prop:
            print "Error getFileLink: wrong full_path"
            return False
        else:
            prop_url = prop['filelinkurl']
            if prop_url:
                print "URL: " + prop_url
                return prop_url
            else:
                resourceno = prop["resourceno"]
                url = self.createFileLink(resourceno)

                if url:
                    return url
                else:
                    return False

    def createFileLink(self, resourceno):
        """Make a link of file

        Args:
            resourceno:
              Resource number of a file to create link
        Returns:
            URL:
              share url for a directory
            False:
              Failed to share a directory
        Remarks:
            If you don't know ``resourceno``, you'd better use getFileLink.
        """
        data = {'_callback': 'window.__jindo_callback._8920',
                'resourceno': resourceno,
                'userid': self.user_id,
                'useridx': self.useridx,
                }

        s, metadata = self.GET('createFileLink', data)

        if s:
            print "URL: %s" % (metadata['short_url'])
            return metadata['short_url']
        else:
            print "Error createFileLink: %s" % (metadata)
            return False

    def getProperty(self, full_path, dummy = 56184):
        """Get a file property

        Args:
            full_path: 
              The full path to get the file or directory property.
                ex) /Picture/flower.png
            dummy:
              ???

        Returns:
            Dict object:
              Property information of a file.

              - creationdate
              - exif
              - filelink
              - filelinkurl
              - filetype => 1: document, 2: image, 3: video, 4: music, 5: zip
              - fileuploadstatus
              - getcontentlength
              - getlastmodified
              - href
              - lastaccessed
              - protect
              - resourceno
              - resourcetype
              - thumbnail
              - totalfilecnt
              - totalfoldercnt
              - virusstatus

            False:
              Failed to get property of a file.
        """
        data = {'orgresource': full_path,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }

        s, metadata = self.POST('getProperty', data)

        if s is True:
            return metadata
        else:
            return False

    def getVersionList(self, full_path, startnum = 0, pagingrow = 50, dummy = 54213):
        """Get a version list of a file or dierectory.

        Args:
            full_path: 
              The full path to get the file or directory property.
                ex) /Picture/flower.png
            startnum: Start version index.
            pagingrow: Max # of version list.

        Returns:
            List of dict:
              Version list of a file or directory in Dict format.

              - createuser
              - filesize
              - getlastmodified
              - href
              - versioninfo
              - versionkey

            False:
              Failed to get property.
              If there is no history, also return False.
        """
        data = {'orgresource': full_path,
                'startnum': startnum,
                'pagingrow': pagingrow,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }

        s, metadata = self.POST('getVersionList', data)

        if s is True:
            return metadata
        else:
            print "Error getVersionList: Cannot get version list"
            return False

    def getVersionListCount(self, full_path, dummy = 51234):
        """Get a count of version list.

        Args:
            full_path: 
              The full path to get the file or directory property.
                ex) /Picture/flower.png

        Returns:
            Integer:
              Number of a version list.
            False:
              Failed to get count of a version list.

        """
        data = {'orgresource':full_path,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }
        s, metadata = self.POST('getVersionListCount', data)

        if s is True:
            return metadata['count']
        else:
            return False

    def setProperty(self, full_path, protect, dummy = 7046):
        """Set property of a file.

        Args:
            full_path: 
              The full path to get the file or directory property.
                ex) /Picture/flower.png
            protect:
              'Y' or 'N', 중요 표시

        Returns:
            True: Success to set property.
            False: Failed to set property.
        """
        data = {'orgresource': full_path,
                'protect': protect,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }
        s, metadata = self.POST('setProperty', data)

        if s is True:
            return True
        else:
            return False

    def getMusicAlbumList(self, tagtype = 0, startnum = 0, pagingrow = 100, dummy = 51467):
        """Get music album list.

        Args:
            tagtype
              ???
            startnum
            pagingrow

        Returns:
            List of dict:
              Music album list as dict format.
                ex)
                  [
                    {
                      u'album':u'Greatest Hits Coldplay',
                      u'artist':u'Coldplay',
                      u'href':u'/Coldplay - Clocks.mp3',
                      u'musiccount':1,
                      u'resourceno':12459548378,
                      u'tagtype':1,
                      u'thumbnailpath':u'N',
                      u'totalpath':u'/'
                    }
                  ]
            False:
              Failed to get music album list.
        """
        data = {'tagtype': tagtype,
                'startnum': startnum,
                'pagingrow': pagingrow,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }
        s, metadata = self.POST('getMusicAlbumList', data)

        if s is True:
            return metadata
        else:
            return False
    def doSearch(self, filename, filetype = None, type = 3, full_path = '/', sharedowner = 'A', datatype = 'all', sort = 'update', order = 'desc', searchtype = 'filesearch', startnum = 0, pagingrow = 100, includeworks = 'N', bodysearch = 'N', dummy = 36644):
        """Get music album list.

        Args:
            filename:
              Query to search.
            filetype:
              Type of file.
              ex) None: all, 1: document, 2:image, 3: video, 4: msuic, 5: zip
            type: 1 => only directories with idxfolder property
                  2 => only files
                  3 => directories and files with thumbnail info
                      ex) viewHeight, viewWidth for Image file
                  4 => only directories except idxfolder
                  5 => directories and files without thumbnail info
            full_path:
              Directory path to search recursively.
            sharedowner:
              File priority to search.
              ex) P: priority files only, A: all files.
            datatype:
              ???
            sort:
              Order criteria of search result
              ex) update, date ...
            order:
              Order of files.
              ex) desc or inc
            searchtype:
              ???
            startnum:
              Start index of search result
            pagingrow:
              Number of result from startnum
            includeworks:
              Whether to include Naver Work files to result.
            bodysearch:
              Search content of file (?)
        Returns:
            List of dict:
              List of search results include filename.

              - authtoken
              - content
              - copyright
              - creationdate
              - domaintype
              - filelink
              - fileuploadstatus
              - getcontentlength
              - getlastmodified
              - hilightfilename
              - href
              - lastaccessed
              - owner
              - ownerid
              - owneridc
              - owneridx
              - ownership
              - protect
              - resourceno
              - resourcetype
              - root
              - root_shareno
              - s_type
              - sharedfoldername
              - sharedinfo
              - shareno
              - subpath
              - thumbnailpath
              - virusstatus
        """
        data = {'filename': filename,
                'filetype': filetype,
                'dstresource': full_path,
                'sharedowner': sharedowner,
                'datatype': datatype,
                'sort': sort,
                'order': order,
                'searchtype': searchtype,
                'startnum': startnum,
                'pagingrow': pagingrow,
                'includeworks': includeworks,
                'bodysearch': bodysearch,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }
        s, metadata = self.POST('doSearch', data)

        if s is True:
            if metadata:
                print "Success doSearch: no result found"
            return metadata
        else:
            return False

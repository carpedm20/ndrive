#!/usr/bin/python
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

import os
import urllib2
import requests
import json
import magic
import datetime

from .auth import naver_login
from .urls import ndrive_urls as NdriveUrls

class ndrive(object):
    """
    This class lets you make Ndrive API calls. First, you need to 
    log in with Ndrive account or set NID_AUT and NID_SES manually.

    """

    # requests session
    # Cookies : NID_AUT, NID_SES, useridx
    session = requests.session()

    def __init__(self, NID_AUT = None, NID_SES= None):
        """Initialize ``NdriveClient`` instance.

        Using given user information, login to ndrive server and create a session

        Args:
            NID_AUT: Naver account authentication info
            NID_SES: Naver account session info

        Returns:

        """
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
            return True

    def GET(self, func, data):
        """GET http request to execute Ndrive API

        Args:
            func:
              The function name you want to execute in Ndrive API.
            params:
              Parameter data for HTTP request.

        Returns:
            metadata:
              Result of the function in JSON form.
            False:
              Failed to execute Ndrive API function.
        """
        s, message = checkAccount()
        if s is False:
            return False, message

        url = NdriveUrls[func]
        r = self.session.get(url, params = data)

        try:
            metadata = json.loads(r.text)
            message = metadata['message']
            if message == 'success':
                return True, metadata['resultvalue']
            else:
                return False, message
        except:
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
              Result of the function in JSON form.
            False:
              Failed to execute Ndrive API function.
        """
        s, message = checkAccount()
        if s is False:
            return False, message

        url = NdriveUrls[func]
        r = self.session.post(url, data = data)

        try:
            metadata = json.loads(r.text)
            message = metadata['message']
            if message == 'success':
                return True, metadata['resultvalue']
            else:
                return False, "Error %s: %s" %(func, message)
        except:
            return False, "Error %s: Failed to send GET request" %func

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
        else:
            print message
            
    def checkStatus(self):
        """Check status

        Args:

        Returns:
            True:
              Sucess
            False:
              Failed

        """
        checkAccount()

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

    def uploadFile(self, file_path, upload_path = '', overwrite = False):
        """Upload a file as Ndrive really do.

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
        s = self.checkUpload(file_path, upload_path, overwrite)

        if s is True:
            self.put(file_path, upload_path)

    def getDiskSpace(self):
        """Get disk space information.

        Returns:
            metadata:
              Disk information in JSON format

        """
        data = {'userid': self.user_id,
                'useridx': self.useridx,
               }
        s, metadata = self.POST('getDiskSpace',data)

        if s is True:
            return metadata
        else:
            print message

    def checkUpload(self, file_obj, full_path, overwrite = False):
        """Check whether it is possible to upload a file.

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
              Possible to upload a file with a given file_size
            False:
              Impossible to upload a file with a given file_size

        """
        try:
            file_obj = f.name
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

        s, metadata = self.POST('ehckUpload', data)

        return s

    def put_file(self, file_obj, full_path):
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

        content = f.read()
        file_name = os.path.basename(file_path)

        now = datetime.datetime.now().isoformat()
        url = nurls['put'] + upload_path + file_name

        headers = {'userid': self.user_id,
                   'useridx': self.useridx,
                   'MODIFYDATE': now,
                   'Content-Type': magic.from_file(file_path, mime=True),
                   'charset': 'UTF-8',
                   'Origin': 'http://ndrive2.naver.com',
        }
        r = self.session.put(url = url, data = content, headers = headers)
        message = json.loads(r.text)['message']

        if message != 'success':
            print "Error put: " + message
            return False
        else:
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
        url = nurls['put'] + upload_path + file_name

        headers = {'userid': self.user_id,
                   'useridx': self.useridx,
                   'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                   'charset': 'UTF-8',
                   'Origin': 'http://ndrive2.naver.com',
        }
        r = self.session.delete(url = url, headers = headers)
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
            JSON string:
              List of files for a path in JSON form.
            False:
              Failed to get list.
        """
        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                'orgresource': orgresource,
                'type': type,
                'dept': dept,
                'sort': sort,
                'order': order,
                'startnum': startnum,
                'pagingrow': pagingrow,
                }

        s, metadata = self.POST('getResult', data)

        if s is True:
            return metadata
        else:
            print metadata
            return False

    def doMove(self, from_path, to_path, stresource = 'F', bShareFireCopy = 'false', dummy = 56147):
        """Move a file.

        Args:
            from_path:
              The path to the file or folder to be moved.
            to_path:
              The destination path of the file or folder to be copied.
              File name should be included in the end of to_path.
                ex) /Picture/flower.png
                
            stresource:
              ???
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
        data = {'orgresource': full_path,
                'dstresource': to_path,
                'overwrite': overwrite,
                'bShareFireCopy': bShareFireCopy,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }

        s, metadata = self.POST('doMove', data)

        return s

    def getProperty(self, full_path, dummy = 56184):
        """Get a file property

        Args:
            full_path: 
              The full path to get the file or directory property.
                ex) /Picture/flower.png
            dummy:
              ???

        Returns:
            JSON string:
              Property information of a file.
            False:
              Failed to get property of a file.
        """
        data = {'full_path': orgresource,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }

        s, metadata = self.POST('getProperty', data)

        if s is True:
            return metadata
        else:
            return False

    def getVersionList(self, full_path, startnum = 0, pagingrow = 50):
        """Get a version list of a file or dierectory.

        Args:
            full_path: 
              The full path to get the file or directory property.
                ex) /Picture/flower.png
            startnum: Start version index.
            pagingrow: Max # of version list.

        Returns:
            JSON string:
              Version list of a file or directory in JSON format.
            False:
              Failed to get property.
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
            return False

    def getVersionListCount(self, full_path):
        """Get a count of version list.

        Args:
            full_path: 
              The full path to get the file or directory property.
                ex) /Picture/flower.png

        Returns:
            Integer:
              Count of a version list.
            False:
              Failed to get count of a version list.

        """
        data = {'orgresource':full_path,
                'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                }
        s, metadata = self.POST('getVersionList', data)

        if s is True:
            return int(metadata['count'])
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
        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'orgresource': orgresource,
                'protect': protect,
                'dummy': dummy,
                }
        s, metadata = self.POST('setProperty', data)

        if s is True:
            return True
        else:
            return False

    def getMusicAlbumList(self, tagtype = 0, startnum = 0, pagingrow = 100):
        """Get music album list.

        Args:
            tagtype
              ???
            startnum
            pagingrow

        Returns:
            Json string:
              Music album list as JSON format.
            False:
              Failed to get music album list.
        """
        data = {'tagtype': tagtype,
                'startnum': startnum,
                'pagingrow': pagingrow,
                'userid': self.user_id,
                'useridx': self.useridx,
                }
        s, metadata = self.POST('setProperty', data)

        if s is True:
            return metadata
        else:
            return False

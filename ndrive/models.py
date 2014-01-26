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
from .urls import ndrive_urls as nurls

class FileInfo(object):

    #: Security protect
    #: Y: protected 중요 표시
    #: N: not protected 
    protect = None

    #: Resource number
    #: Integer number
    resourceno = None

    #: Share message count
    #: Integer number
    sharemsgcnt = None

    #: Copyright
    #: Y: 
    #: N: 
    copyright = None

    #: Subfolder count
    subfoldercnt = None

    #: Resource type
    #: collection: 
    resourcetype = None

    #: File upload status
    #: 1: Default
    fileuploadstatus = None

    #: Priority
    #: 1: Default
    priority = None

    #: File link
    #: None: No link for a file
    #: 
    filelink = None

    #: href
    href = None

    #: Thumbnail path
    thumbnailpath = None

    #: Sahred info
    #: T:
    #: F:
    sharedinfo = None

    #: Get last modified date
    #: ex) 2014-01-26T12:23:07+09:00
    getlastmodified = None

    #: Share number
    #: Integer number
    shareno = None

    #: Last modified user
    #: None: 
    lastmodifieduser = None

    #: Get content Length
    #: Integer number
    getcontentlength = None

    #: Last accessed date
    #: ex) 2014-01-26T12:23:07+09:00
    lastaccessed = None

    #: Virus status
    #: Y: File is detected as virus
    #: N: File is not detected as virus
    virusstatus = None

    #: idxfolder
    #: ???
    idxfolder = None

    #: Creation date
    #: ex) 2014-01-26T12:23:07+09:00
    creationdate = None

    # Spcial properties for "Image" file
    #   nocache, viewWidth, viewHeight
    nocache = None
    viewWidth = None
    viewHeight = None

    #: Total file count
    #: Integer number
    totalfilecnt = None

    #: Total folder count
    #: Integer number
    totalfoldercnt = None

    #: File type
    #: 1: document, 문서 파일
    #: 2: image, 사진 파일
    #: 3: video, 동영상 파일
    #: 4: music, 음악 파일
    #: 5: zip, 압축 파일
    #: 
    filetype = None

    #: Exif
    #: Y: Yes exif info
    #: N: No exif info
    exif = None

    #: Has thumbnail
    #: Y: Has thumbnail
    #: N: No thumbnail
    thumbnail = None

    #: File link ulr
    #: null:
    filelinkurl = None

    def __repr__(self):
        return '[%s] resourceno: %s, resourcetype: %s' % (
            self.href.encode('utf-8'),
            self.resourceno,
            self.resourcetype,
        )

    def setJson(self, j):
        self.json = j

class ndrive:
    # requests session
    # Cookies : NID_AUT, NID_SES, useridx
    session = requests.session()

    def __init__(self, NID_AUT = None, NID_SES= None):
        """Initialize ndrive instance

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


    def getRegisterUserInfo(self, svctype = "Android NDrive App ver", auth = 0):
        """Get registerUserInfo

        Args:
            svctype: Platform information
            auth: ???

        Returns:
            True: Success
            False: Failed

        """
        data = {'userid': self.user_id, 'svctype': svctype, 'auth': auth}
        r = self.session.get(nurls['getRegisterUserInfo'], params = data)

        j = json.loads(r.text)

        if j['message'] != 'success':
            print "[*] Error getRegisterUserInfo: " + j['message']
            return False

        else:
            self.useridx = j['resultvalue']['useridx']
            return True
        
    def checkStatus(self):
        """Check status

        Args:

        Returns:
            True: Sucess
            False: Failed

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

    def checkAccount(self):
        if self.useridx is None:
            print "[*] Error checkStatus: useridx is not defined"
            return False

        elif self.user_id is None:
            print "[*] Error checkStatus: userId is not defined"
            return False

    def uploadFile(self, file_path, upload_path = '', overwrite = False):
        """uploadFile

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

    def getDiskSpace(self, file_path, upload_path = '', overwrite = False):
        """getDiskSpace

        Args:
            file_path: Full path for a file you want to checkUpload
            upload_path: Ndrive path where you want to upload file
                ex) /Picture/

        Returns:
            True: Possible to upload a file with a given file_size
            False: Impossible to upload a file with a given file_size

        """

        self.checkAccount()

        url = nurls['checkUpload']

        file_size = os.stat(file_path).st_size
        file_name = os.path.basename(file_path)

        now = datetime.datetime.now().isoformat()

        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'getlastmodified': now,
                'dstresource': upload_path + file_name,
                'overwrite': overwrite,
                'uploadsize': file_size,
               }
        r = self.session.post(nurls['getDiskSpace'], data = data)

        return resultManager(r.text)

    def checkUpload(self, file_path, upload_path = '', overwrite = False):
        """Check upload

        Args:
            file_path: Full path for a file you want to checkUpload
            upload_path: Ndrive path where you want to upload file
                ex) /Picture/

        Returns:
            True: Possible to upload a file with a given file_size
            False: Impossible to upload a file with a given file_size

        """
        url = nurls['checkUpload']

        file_size = os.stat(file_path).st_size
        file_name = os.path.basename(file_path)

        now = datetime.datetime.now().isoformat()

        data = {'uploadsize': file_size,
                'overwrite': overwrite if 'T' else 'F',
                'getlastmodified': now,
                'dstresource': upload_path + file_name,
                'userid': self.user_id,
                'useridx': self.useridx,
                }

        r = self.session.post(url = url, data = data)

        return self.resultManager(r.text)

    def put(self, file_path, upload_path = ''):
        """PUT

        Args:
            file_path: Full path for a file you want to upload
            upload_path: Ndrive path where you want to upload file
                ex) /Picture/

        Returns:
            True: Upload success
            False: Upload failed

        """
        f = open(file_path, "r")
        c = f.read()

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
        r = self.session.put(url = url, data = c, headers = headers)

        return self.resultManager(r.text)

    def delete(self, file_path):
        """DELETE

        Args:
            file_path: Full path for a file you want to delete 
            upload_path: Ndrive path where you want to delete file
                ex) /Picture/

        Returns:
            True: Delete success
            False: Delete failed

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

        return self.resultManager(r.text)

    def getList(self, dummy = 56184, orgresource = '/', type = 1, dept = 0, sort = 'name', order = 'asc', startnum = 0, pagingrow = 1000):
        """GetList

        Args:
            dummy: ???
            orgresource: Directory path to get the file list
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

        Returns:
            FileInfo list: List of files for a path
            False: Failed to get list

        """
        
        url = nurls['getList']

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

        r = self.session.post(url = url, data = data)

        try:
            j = json.loads(r.text)
        except:
            print '[*] Success checkUpload: 0 result'

            return []

        if j['message'] != 'success':
            print '[*] Error checkUpload: ' + j['message']

            return False
        else:
            files = []

            for i in j['resultvalue']:
                f = FileInfo()

                f.protect = i['protect']
                f.resourceno = i['resourceno']
                f.copyright = i['copyright']
                f.subfoldercnt = i['subfoldercnt']
                f.resourcetype = i['resourcetype']
                f.fileuploadstatus = i['fileuploadstatus']
                f.prority = i['priority']
                f.filelink = i['filelink']
                f.href = i['href']
                f.thumbnailpath = i['thumbnailpath']
                f.sharedinfo = i['sharedinfo']
                f.getlastmodified = i['getlastmodified']
                f.shareno = i['shareno']
                f.lastmodifieduser = i['lastmodifieduser']
                f.getcontentlength = i['getcontentlength']
                f.lastaccessed = i['lastaccessed']
                f.virusstatus = i['virusstatus']
                f.idxfolder = i['idxfolder']
                f.creationdate = i['creationdate']
                f.nocache = i['nocache']
                f.viewWidth = i['viewWidth']
                f.viewHeight = i['viewHeight']

                f.setJson(j['resultvalue'])
                
                files.append(f)

            return files

    def doMove(self, orgresource, dstresource, dummy = 56184, stresource = 'F', bShareFireCopy = 'false'):
        """DoMove

        Args:
            dummy: ???
            orgresource: Path for a file which you want to move
            dstresource: Destination path
            bShareFireCopy: ???

        Returns:
            True: Move success
            False: Move failed
            
        """

        url = nurls['doMove']
        
        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                'orgresource': orgresource,
                'dstresource': dstresource,
                'overwrite': overwrite,
                'bShareFireCopy': bShareFireCopy,
                }

        r = self.session.post(url = url, data = data)

        try:
            j = json.loads(r.text)
        except:
            print '[*] Success checkUpload: 0 result'

            return False

        return self.resultManager(r.text)

    def getProperty(self, orgresource, dummy = 56184):
        """GetProperty

        Args:
            dummy: ???
            orgresource: File path

        Returns:
            FileInfo object:
            False: Failed to get property

        """

        url = nurls['getProperty']

        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'dummy': dummy,
                'orgresource': orgresource,
                }

        r = self.session.post(url = url, data = data)
        j = json.loads(r.text)

        if self.resultManager(r.text):
            f = FileInfo()
            result = j['resultvalue']

            f.resourcetype = result['resourcetype']
            f.resourceno = result['resourceno']

            return f

        else:
            return False

    def getVersionList(self, orgresource, startnum = 0, pagingrow = 50):
        """GetVersionList

        Args:
            orgresource: File path
            startnum: Start version index
            pagingrow: Max # of version list

        Returns:
            FileInfo object:
            False: Failed to get property

        """

        url = nurls['getVersionList']

        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'orgresource': orgresource,
                'startnum': startnum,
                'pagingrow': pagingrow,
                }

        r = self.session.post(url = url, data = data)
        j = json.loads(r.text)

        if self.resultManager(r.text):
            f = FileInfo()
            result = j['resultvalue']

            f.resourcetype = result['resourcetype']
            f.resourceno = result['resourceno']
            ######### ??????

            return f

        else:
            return False

    def getVersionListCount(self, orgresource):
        """GetVersionListCount

        Args:
            orgresource: File path

        Returns:
            Integer number: # of version list
            False: Failed to get property

        """

        url = nurls['getVersionListCount']

        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'orgresource': orgresource,
                }

        r = self.session.post(url = url, data = data)
        j = json.loads(r.text)

        if j['message'] != 'success':
            print "[*] Error getVersionListCount: " + j['message']
            return False
        else:
            return int(j['resultvalue']['count'])

    def setProperty(self, orgresource, protect, dummy = 7046):
        """SetProperty

        Args:
            orgresource: File path
            protect: 'Y' or 'N', 중요 표시

        Returns:
            Integer number: # of version list
            False: Failed to get property

        """

        url = nurls['setProperty']

        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'orgresource': orgresource,
                'protect': protect,
                'dummy': dummy,
                }

        r = self.session.post(url = url, data = data)

        return resultManager(r.text)

    def getMusicAlbumList(self, tagtype = 0, startnum = 0, pagingrow = 100):
        """GetMusicAlbumList

        Args:
            tagtype = ???
            startnum
            pagingrow

        Returns:
            ???
            False: Failed to get property

        """

        url = nurls['setProperty']

        data = {'userid': self.user_id,
                'useridx': self.useridx,
                'tagtype': tagtype,
                'startnum': startnum,
                'pagingrow': pagingrow,
                }

        r = self.session.post(url = url, data = data)

        return resultManager(r.text) # need to edit

    def resultManager(self, text):
        """
        resultcode & message:
            0 = success => if "resultvalue" = null: no result to show
            11 = Not Exist Path
            36 = File Infomation Not Found
            2002 = Invalidation Cookie
        
        """
        j = json.loads(text)

        if j['message'] != 'success':
            print "[*] Error : " + j['message']
            return False
        else:
            return True


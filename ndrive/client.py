# -*- coding: utf-8 -*-

"""

====================================
ndrive
====================================

What is ndrive
==============

ndrive is a Naver Ndrive wrapper for python


Getting started
===============

    git clone https://github.com/carpedm20/pyndrive.git

Copyright
=========

Copyright 2014 Kim Tae Hoon

"""

import os, sys
from os.path import expanduser
import urllib, urllib2
import requests
import simplejson as json
import magic
import datetime
import re

from .auth import getCookie
from .urls import ndrive_urls as nurls
from .utils import byte_readable

###############################################################################
class Ndrive(object):
    """Initialize ``NdriveClient`` instance.

    Using given user information, login to ndrive server and create a session

    :param bool debug: (optional) print all metadata of http requests
    :param str NID_AUT: (optional) Naver account authentication info
    :param str NID_SES: (optional) Naver account session info

    Usage::

        >>> from ndrive import Ndrive
        >>> nd = Ndrive()
    """

    debug = False
    session = requests.session()

    def __init__(self, debug = False, NID_AUT = None, NID_SES= None):
        self.debug = debug
        self.session.headers["User-Agent"] = \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) Chrome/32.0.1700.76 Safari/537.36"
        self.session.cookies.set('NID_AUT', NID_AUT)
        self.session.cookies.set('NID_SES', NID_SES)

    def login(self, user_id, password, svctype = "Android NDrive App ver", auth = 0):
        """Log in Naver and get cookie

            >>> s = nd.login("YOUR_ID", "YOUR_PASSWORD")

        :param str user_id: Naver account's login id
        :param str password: Naver account's login password
        :param str svctype: Service type
        :param auth: ???

        :return: ``True`` when success to login or ``False``
        """
        self.user_id = user_id
        self.password = password

        if self.user_id == None or self.password == None:
            print "[*] Error __init__: user_id and password is needed"
            return False

        try:
            cookie = getCookie(user_id, password)
        except:
            print "[*] Error getCookie: failed"
            return False

        self.session.cookies.set('NID_AUT', cookie["NID_AUT"])
        self.session.cookies.set('NID_SES', cookie["NID_SES"])

        s, metadata = self.getRegisterUserInfo(svctype, auth)

        if s is True:
            return True
        else:
            print "[*] Error getRegisterUserInfo: " + metadata['message']
            return False

    def checkAccount(self):
        if self.useridx is None:
            return False, "Error checkStatus: useridx is not defined"
        elif self.user_id is None:
            return False, "Error checkStatus: userId is not defined"
        else:
            return True, None

    def GET(self, func, data):
        """Send GET request to execute Ndrive API

        :param func: The function name you want to execute in Ndrive API.
        :param params: Parameter data for HTTP request.

        :returns: metadata when success or False when failed
        """
        if func not in ['getRegisterUserInfo']:
            s, message = self.checkAccount()

            if s is False:
                return False, message

        url = nurls[func]
        r = self.session.get(url, params = data)
        r.encoding = 'utf-8'

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
        """Send POST request to execute Ndrive API

        :param func: The function name you want to execute in Ndrive API.
        :param params: Parameter data for HTTP request.

        :returns: ``metadata`` when success or ``False`` when failed
        """
        s, message = self.checkAccount()
        if s is False:
            return False, message

        url = nurls[func]
        r = self.session.post(url, data = data)
        r.encoding = 'utf-8'

        if self.debug:
            print r.text.encode("utf-8")

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

        :param svctype: Information about the platform you are using right now.
        :param auth: Authentication type

        :return: ``True`` when success or ``False`` when failed
        """
        data = {'userid': self.user_id,
                'svctype': svctype,
                'auth': auth
               }

        s, metadata = self.GET('getRegisterUserInfo', data)

        if s is True:
            self.useridx = metadata['useridx']
            return True, metadata
        else:
            return False, metadata
            
    def checkStatus(self):
        """Check status

        Check whether it is possible to access Ndrive or not.

        :return: ``True`` when success or ``False`` when failed.
        """
        self.checkAccount()

        data = {'userid': self.user_id,
                'useridx': self.useridx
               }
        r = self.session.post(nurls['checkStatus'], data = data)
        r.encoding = 'utf-8'

        p = re.compile(r'\<message\>(?P<message>.+)\</message\>')
        message = p.search(r.text).group('message')

        if message == 'success':
            return True
        else:
            return False

    def uploadFile(self, file_obj, full_path, overwrite = False):
        """Upload a file as Ndrive really do.

            >>> nd.uploadFile('~/flower.png','/Picture/flower.png',True)

        This function imitates the process when Ndrive uploads a local file to its server. The process follows 7 steps:
              1. POST /CheckStatus.ndrive
              2. POST /GetDiskSpace.ndrive
              3. POST /CheckUpload.ndrive
              4. PUT /FILE_PATH
              5. POST /GetList.ndrive
              6. POST /GetWasteInfo.ndrive
              7. POST /GetDiskSpace.ndrive

            nd.uploadFile('./flower.png','/Picture/flower.png')

        :param file_obj: A file-like object to check whether possible to upload. You can pass a string as a file_obj or a real file object.
        :param full_path: The full path to upload the file to, *including the file name*. If the destination directory does not yet exist, it will be created. 
        :param overwrite: Whether to overwrite an existing file at the given path. (Default ``False``.)
        """
        s = self.checkStatus()
        s = self.getDiskSpace()
        s = self.checkUpload(file_obj, full_path, overwrite)

        if s is True:
            self.put(file_obj, full_path, overwrite)

    def getDiskSpace(self):
        """Get disk space information.

            >>> disk_info = nd.getDiskSpace()

        :return: ``metadata`` if success or ``error message``

        :metadata:
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

            >>> s = nd.checkUpload('~/flower.png','/Picture/flower.png')

        :param file_obj: A file-like object to check whether possible to upload. You can pass a string as a file_obj or a real file object.
        :param str full_path: The full path to upload the file to, *including the file name*. If the destination directory does not yet exist, it will be created. 
        :param overwrite: Whether to overwrite an existing file at the given path. (Default ``False``.)
            
        :return: ``True`` if possible to upload or ``False`` if impossible to upload.
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

    def downloadFile(self, from_path, to_path = ''):
        """Download a file.

            >>> nd.downloadFile('/Picture/flower.png', '~/flower.png')

        :param from_path: The full path to download the file to, *including the file name*. If the destination directory does not yet exist, it will be created.
        :param to_path: The full path of a file to be saved in local directory.

        :returns: File object
        """

        if to_path == '':
            file_name = os.path.basename(from_path)
            to_path = os.path.join(os.getcwd(), file_name)

        url = nurls['download'] + from_path

        data = {'attachment':2,
                'userid': self.user_id,
                'useridx': self.useridx,
                'NDriveSvcType': "NHN/ND-WEB Ver",
               }

        if '~' in to_path:
            to_path = expanduser(to_path)

        with open(to_path, 'wb') as handle:
            request = self.session.get(url, params = data, stream=True)

            for block in request.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            return handle

    def put(self, file_obj, full_path, overwrite = False):
        """Upload a file.

            >>> nd.put('./flower.png','/Picture/flower.png')
            >>> nd.put(open('./flower.png','r'),'/Picture/flower.png')

        :param file_obj: A file-like object to check whether possible to upload. You can pass a string as a file_obj or a real file object.
        :param full_path: The full path to upload the file to, *including the file name*. If the destination directory does not yet exist, it will be created.

        :return: ``True`` when succcess to upload a file or ``False``
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
        r.encoding = 'utf-8'

        message = json.loads(r.text)['message']

        if message != 'success':
            print "Error put: " + message
            return False
        else:
            print "Success put: " + file_obj.name
            return True

    def delete(self, full_path):
        """Delete a file in full_path

            >>> nd.delete('/Picture/flower.png')

        :param full_path: The full path to delete the file to, *including the file name*.

        :return: ``True`` if success to delete the file or ``False``
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
            r.encoding = 'utf-8'
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

            >>> nd_list = nd.getList('/', type=3)
            >>> print nd_list

        There are 5 kinds of ``type``:
            - 1 => only directories with idxfolder property
            - 2 => only files
            - 3 => directories and files with thumbnail info (like viewHeight, viewWidth for Image file)
            - 4 => only directories except idxfolder
            - 5 => directories and files without thumbnail info

        There are 5 kindes of ``sort``:
            - file : file type, 종류
            - length : size of file, 크기
            - date : edited date, 수정한 날짜
            - credate : creation date, 올린 날짜
            - protect : protect or not, 중요 표시

        :param full_path: The full path to get the file list.

        :param type: 1, 2, 3, 4 or 5

        :param depth: Dept for file list

        :param sort: name => 이름

        :param order: Order by (asc, desc)

        :return: metadata (list of dict) or False when failed to get list

        :metadata:
            - u'copyright': u'N',
            - u'creationdate': u'2013-05-12T21:17:23+09:00',
            - u'filelink': None,
            - u'fileuploadstatus': u'1',
            - u'getcontentlength': 0,
            - u'getlastmodified': u'2014-01-26T12:23:07+09:00',
            - u'href': u'/Codes/',
            - u'lastaccessed': u'2013-05-12T21:17:23+09:00',
            - u'lastmodifieduser': None,
            - u'priority': u'1',
            - u'protect': u'N',
            - u'resourceno': 204041859,
            - u'resourcetype': u'collection',
            - u'sharedinfo': u'F',
            - u'sharemsgcnt': 0,
            - u'shareno': 0,
            - u'subfoldercnt': 5,
            - u'thumbnailpath': u'N',
            - u'virusstatus': u'N'
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

            >>> nd.doMove('/Picture/flower.png', '/flower.png')

        :param from_path: The path to the file or folder to be moved.
        :param to_path: The destination path of the file or folder to be copied. File name should be included in the end of to_path.
        :param overwrite: Whether to overwrite an existing file at the given path. (Default ``False``.)
        :param bShareFireCopy: ???

        :return: ``True`` if success to move a file or ``False``.
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

            >>> nd.makeDirectory('/test')
        
        :param full_path: The full path to get the directory property. Should be end with '/'.

        :return: ``True`` when success to make a directory or ``False``
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

            >>> nd.makeShareUrl('/Picture/flower.png', PASSWORD)

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

            >>> file_link = nd.getFileLink('/Picture/flower.png')
        
        :params full_path: The full path of file to get file link. Path should start and  end with '/'.

        :return: ``Shared url`` or ``False`` if failed to share a file or directory through url
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

        If you don't know ``resourceno``, you'd better use ``getFileLink``.

        :param resourceno: Resource number of a file to create link

        :return: ``Shared url`` or ``False`` when failed to share a file
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

        :param full_path: The full path to get the file or directory property.

        :return: ``metadata`` if success or ``False`` if failed to get property

        :metadata:
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

        :param full_path: The full path to get the file or directory property. Path should start with '/'
        :param startnum: Start version index.
        :param pagingrow: Max # of version list in one page.

        :returns: ``metadata`` if succcess or ``False`` (failed to get history or there is no history)

        :metadata:
              - createuser
              - filesize
              - getlastmodified
              - href
              - versioninfo
              - versionkey
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

        :param full_path: The full path to get the file or directory property.

        :returns: ``Integer`` (number of version lists) or ``False`` if failed to get a version list
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

        :param full_path: The full path to get the file or directory property.
        :param protect: 'Y' or 'N', 중요 표시

        :return: ``True`` when success to set property or ``False``
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

        :param tagtype: ???

        :return: ``metadata`` or ``False``

        :metadata:
            - u'album':u'Greatest Hits Coldplay',
            - u'artist':u'Coldplay',
            - u'href':u'/Coldplay - Clocks.mp3',
            - u'musiccount':1,
            - u'resourceno':12459548378,
            - u'tagtype':1,
            - u'thumbnailpath':u'N',
            - u'totalpath':u'/'
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

        There are 4 kinds in ``type``:
            - 1 : only directories with idxfolder property
            - 2 : only files
            - 3 : directories and files with thumbnail info (like viewHeight, viewWidth for Image file)
            - 4 : only directories except idxfolder
            - 5 : directories and files without thumbnail info

        Tyere are 5 kindes of ``filetype``:
            ex) None: all, 1: document, 2:image, 3: video, 4: msuic, 5: zip

        :param filename: Query to search.
        :param filetype: Type of a file to search.
        :param full_path: Directory path to search recursively.
        :param sharedowner: File priority to search. (P: priority files only, A: all files.)
        :param datatype: Data type of a file to search
        :param sort: Order criteria of search result. ('update', 'date' ...)
        :param order: Order of files. ('desc' or 'inc')
        :param searchtype: ???
        :param includeworks: Whether to include Naver Work files to result.
        :param bodysearch: Search content of file.

        :returns: ``metadata`` or ``False``

        :metadata:
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
                return {}
            return metadata
        else:
            print "Failed doSearch: search failed"
            return False

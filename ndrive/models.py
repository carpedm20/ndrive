"""
ndrive
======

ndrive is a Naver Ndrive wrapper for python

Getting started
---------------

    git clone https://github.com/carpedm20/pyndrive.git

Copyright
---------

ndrive is following an MIT License.

"""

import os
import mechanize
import urllib2
import requests
import json
import magic
import datetime

from .auth import naver_login
from .urls import ndrive_urls as nurls

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
        if self.useridx is None:
            print "[*] Error checkStatus: useridx is not defined"
            return False

        elif self.user_id is None:
            print "[*] Error checkStatus: userId is not defined"
            return False

        data = {'userid' : self.user_id,
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
        s = self.checkUpload(file_path, upload_path, overwrite)

        if s is True:
            self.put(file_path, upload_path)

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
        j = json.loads(r.text)

        if j['message'] != 'success':
            print '[*] Error checkUpload: ' + j['message']

            return False
        else:
            print '[*] Success checkUpload'
            return True

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

        print r.text

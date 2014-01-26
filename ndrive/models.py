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

    def login(self, user_id, password):
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
            print "Error __init__: user_id and password is needed"
            return None

        try:
            cookie = naver_login(user_id, password)
        except:
            return False

        self.session.cookies.set('NID_AUT', cookie["NID_AUT"])
        self.session.cookies.set('NID_SES', cookie["NID_SES"])

        return True

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
            print "Error checkStatus: useridx is not defined"
            return False

        elif self.user_id is None:
            print "Error checkStatus: userId is not defined"
            return False

        data = {'userid' : self.userId, 'useridx': self.useridx}
        r = self.session.post(nurls['checkStatus'], data = data)

        p = re.compile(r'\<message\>(?P<message>.+)\</message\>')
        message = p.search(r.text).group('message')

        if message == 'success':
            return True
        else:
            return False

    def put(self, file_path):
        """PUT

        Args:
            file_path: Full path for the file you want to upload

        Returns:
            True: Upload success
            False: Upload failed

        """
        f = open(file_path, "r")
        c = f.read()

        now = datetime.datetime.now().isoformat()

        url = nurls['put'] + '/' + fileName
        headers = {'userid': self.userId,
                   'charset': 'UTF-8',
                   'useridx': self.useridx,
                   'Origin': 'http://ndrive2.naver.com',
                   'MODIFYDATE': datetime.datetime.now().isoformat(),
                   'Content-Type': magic.from_file(fileName, mime=True)
        }
        r = self.session.put(url = url, data = c, headers = headers)

        print r.text

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
import json
from login import naverLogin
class ndrive:
    def __init__(self, NID_AUT = None, NID_SES= None):
        """Initialize ndrive instance

        Using given user information, login to ndrive server and create a session

        Args:
            NID_AUT : Naver account authentication info
            NID_SES : Naver account session info

        Returns:

    """
        self.NID_AUTH = NID_AUT
        self.NID_SES = NID_SES

    def login(self, userId, password):
        """Log in Naver and get cookie

        Agrs:
            user_id: Naver account's login id
            password: Naver account's login password

        Returns:
            True : Login success
            False : Login failed

        Remarks:
            self.cookie is a dictionary with 5 keys: path, domain, NID_AUT, nid_inf, NID_SES
        """
        self.userId = userId
        self.password = password

        if self.userId == None or self.password == None:
            print "Error __init__: user_id and password is needed"
            return None

        try:
            cookie = naverLogin(userId, password)
        except:
            return False

        #self.cookie = cookie
        self.NID_AUT = cookie["NID_AUT"]
        self.NID_SES = cookie["NID_SES"]
            
        return True

    

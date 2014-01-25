"""
pyndrive
======

pyndrive is a Naver Ndrive wrapper for python

Getting started
---------------

    git clone https://github.com/carpedm20/pyndrive.git

Copyright
---------

Copyright © 2014 Kim Tae Hoon.

"""

import mechanize
import urllib2
import json
from login import Login
class ndrive:
    def __init__(self, user_id = None, password = None):
    """Initialize ndrive instance

    Using given user information, login to ndrive server and create a session

    Args:
        user_id: Naver login id
        password: Naver login password

    Returns:


    Remarks:
        self.cookie is a dictionary with 5 keys: path, domain, NID_AUT, nid_inf, NID_SES
    """
        if user_id == None || password == None:
            print "Error __init__: user_id and password is needed"
            return None
            
        self.user_id = user_id
        self.password = password

        login = Login(userId, password)
        self.cookie = login.cookie

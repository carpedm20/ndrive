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
        self.NID_AUT = NID_AUT
        self.NID_SES = NID_SES
        self.useridx = None

        baseUrl = "http://ndrive2.naver.com"

        self.urls = {}

        """GET /GetRegisterUserInfo.ndrive

        Params:
            userid=carpedm20
            svctype=Android%20NDrive%20App%20ver
            auth=0

        Returns:
            {
                "resultcode":0,
                "message":"success",
                "resultvalue":{
                    "userid":"carpedm20",
                    "useridx":xxxxxxx,
                    "setidc":2,
                    "cmsdomain":"ndrive2.naver.com",
                    "isdormancy":"false",
                    "islow":"Y",
                    "isshareagree":"F",
                    "regdate":"2011-07-17T23:51:19+09:00",
                    "useworks":"N",
                    "startpage":"N",
                    "usedocviewer":"Y",
                    "ndriveskin":"WH   ",
                    "officeskin":"WH   ",
                    "usedocindex":"N",
                    "payment":"F"
                }
            }
        """
        self.urls['getRegisterUserInfo'] = baseUrl + "/GetRegisterUserInfo.ndrive"

        """POST /CheckStatus.ndrive

        Params:
            userid = carpedm20
            useridx = 6794877

        Returns:
            <?xml version="1.0" encoding="utf-8" ?>
            <result>
                .<resultcode>0</resultcode>
                .<message>success</message>
            </result>
        """
        self.urls['checkStatus'] = baseUrl + "/CheckStatus.ndrive"

        """POST /GetDiskSpace.ndrive

        Params:
            userid = carpedm20
            useridx = 6794877

        Returns:
            {
            ."resultcode":0,
            ."message":"success",
            ."resultvalue":{
            .."totalspace":32212254720,
            .."usedspace":31821225985,
            .."unusedspace":391028735,
            .."paymentspace":0,
            .."expandablespace":354334801920,
            .."largefileusedspace":14842667181,
            .."largefileunusedspace":17369587539,
            .."totallargespace":32212254720,
            .."largefileminsize":52428800,
            .."filemaxsize":4294967296
            .}
            }
        """

        self.urls['getDiskSpace'] = baseUrl + "/GetDiskSpace.ndrive"

        """POST /CheckUpload.ndrive

        Params:
            uploadsize = 33621
            overwrite = F
            getlastmodified = 2014-01-25T13%3A52%3A41%2B09%3A00
            dstresource = %2Fsolar2.png
            userid = carpedm20
            useridx = 6794877

        Returns:
            {
            ."resultcode":0,
            ."message":"success"
            }
        """

        self.urls['checkUpload'] = baseUrl + "/CheckUpload.ndrive"

        """PUT /fileName

        Params:
            rawFile

        Returns:
            {
            ."resultcode":0,
            ."message":"success"
            }
        """
        self.urls['put'] = baseUrl # + fileName

        """POST GetList.ndrive

        Params:
            userid = carpedm20
            useridx = 6794877
            dummy = 56184
            orgresource = %2F
            type = 1
            depth = 0
            sort = name
            order = asc
            startnum = 0
            pagingrow = 1000

        Returns:
            {
            ."resultcode":0,
            ."message":"success",
            ."resultvalue":[
            ..{
            ..."href":"\/FolderName\/",
            ..."priority":"1",
            ..."resourceno":204041859,
            ..."getcontentlength":0,
            ..."protect":"N",
            ..."resourcetype":"collection",
            ..."thumbnailpath":"N",
            ..."creationdate":"2013-05-12T21:17:23+09:00",
            ..."getlastmodified":"2014-01-09T04:47:14+09:00",
            ..."lastaccessed":"2013-05-12T21:17:23+09:00",
            ..."subfoldercnt":5,
            ..."fileuploadstatus":"1",
            ..."sharedinfo":"F",
            ..."shareno":0,
            ..."virusstatus":"N",
            ..."copyright":"N",
            ..."sharemsgcnt":0,
            ..."filelink":null,
            ..."lastmodifieduser":null
            ..},
        """
        self.urls['getList'] = baseUrl + "/GetList.ndrive"

        """POST /GetWasteInfo.ndrive

        Params:
            userid=carpedm20
            useridx=6794877
            dummy=27764

        Returns:
            {
            ."resultcode":0,
            ."message":"success",
            ."resultvalue":{
            .."cycle":50,
            .."getcontentlength":"78045"
            .}
            }
        """
        self.urls['getWasteInfo'] = baseUrl + "/GetWasteInfo.ndrive"

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

        self.NID_AUT = cookie["NID_AUT"]
        self.NID_SES = cookie["NID_SES"]

        self.cookies = {"NID_AUT": self.NID_AUT, "NID_SES": self.NID_SES}
            
        return True

    def getRegisterUserInfo(self, svctype = "Android NDrive App ver", auth = 0):
        """Get registerUserInfo

        Args:
            svctype : Platform information
            auth : ???

        Returns:
            True : Success
            False : Failed

        """
        data = {'userid': self.userId, 'svctype': svctype, 'auth': auth}
        r = requests.get(self.urls['getRegisterUserInfo'], params = data, cookies = self.cookies)

        j = json.loads(r.text)

        if j['message'] != 'success':
            return False

        else:
            self.useridx = j['resultvalue']['useridx']
            return True
        
    def checkStatus(self):
        """Check status

        """
        if self.useridx is None:
            print "Error checkStatus: useridx is not defined"
            return False

        elif self.userId is None:
            print "Error checkStatus: userId is not defined"
            return False

        data = {'userid' : self.userId, 'useridx': self.useridx}
        r = requests.post(self.urls['checkStatus'], params = data, cookies = self.cookies)

        p = re.compile(r'\<message\>(?P<message>.+)\</message\>')
        message = p.search(r.text).group('message')

        if message == 'success':
            return True
        else:
            return False

    def put(self, fileName):
        """PUT

        """
        f = open(fileName, "r")
        c = f.read()

        headers = {'userid': self.userId, 'charset': 'UTF-8', 'useridx': self.useridx, 'Origin': 'http://ndrive2.naver.com','MODIFYDATE': datetime.datetime.now().isoformat(), 'Content-Type': magic.from_file(fileName, mime=True)}
        r = requests.put(self.urls['put'] + '/' + fileName, data = c, cookies = self.cookies, headers = headers)

        print r.text

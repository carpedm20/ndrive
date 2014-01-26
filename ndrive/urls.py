"""
ndrive.models
=============

Thjis module contains the primary urls for ndrive
"""

ndrive_urls = {}
base_url = "http://ndrive2.naver.com"

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
ndrive_urls['getRegisterUserInfo'] = base_url + "/GetRegisterUserInfo.ndrive"

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
ndrive_urls['checkStatus'] = base_url + "/CheckStatus.ndrive"

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

ndrive_urls['getDiskSpace'] = base_url + "/GetDiskSpace.ndrive"

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

ndrive_urls['checkUpload'] = base_url + "/CheckUpload.ndrive"

"""PUT /fileName

Params:
    rawFile

Returns:
    {
    ."resultcode":0,
    ."message":"success"
    }
"""
ndrive_urls['put'] = base_url # + fileName

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
ndrive_urls['getList'] = base_url + "/GetList.ndrive"

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
ndrive_urls['getWasteInfo'] = base_url + "/GetWasteInfo.ndrive"


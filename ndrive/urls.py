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
    ."message":"success",
    ."resultvalue":{
    .."totalspace":32212254720,
    .."usedspace":31821325853,
    .."unusedspace":390928867,
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

Information about waste, 휴지동 크기

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

"""POST /GetWasteListCount.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    dummy=47304
    ownerid=
    owneridx=

Returns:
    {
        "resultcode":0,
        "message":"success",
        "resultvalue":{
            "count":2
        }
    }
"""
ndrive_urls['getWasteListCount'] = base_url + "/GetWasteListCount.ndrive"

"""POST /GetWasteList.ndrive

File list in waste, 휴지동 파일 리스트

Params:
    userid=carpedm20
    useridx=6794877
    dummy=27764
    sort=deletedate
    order=desc
    startnum=0
    pagingrow=100
    type=3

Returns:
        {
        "resultcode":0,
        "message":"success",
        "resultvalue":[
            {
                "href":"FILE_PATH",
                "resourcetype":"property",
                "getlastmodified":"2014-01-26T02:16:29+09:00",
                "getcontentlength":66247,
                "deletedate":"2014-01-26T17:29:03+09:00",
                "resourceno":12457657175,
                "physhref":"\/.recycled\/ndrive_-427244713",
                "orgpath":"\/"
            },
            ...
        ]
    }
"""
ndrive_urls['getWasteList'] = base_url + "/GetWasteList.ndrive"

"""DELETE /PHYSHREF

    ex) /.recycled/solar.png_-427837829
    ex) / => Empty waste

Completely delete a file

Params:

Returns:
    {
        "resultcode":0,
        "message":"success"
    }
"""
ndrive_urls['deleteWasteFile'] = base_url

"""POST /DoMove.ndrive 

Params:
    userid=carpedm20
    useridx=6794877
    dummy=38404
    orgresource=%2Fsolar2.png
    dstresource=%2FUNIST%2F
    overwrite=F
    bShareFireCopy=false

Returns:
    {
        "resultcode":0,
        "message":"success"
    }
"""
ndrive_urls['doMove'] = base_url + "/DoMove.ndrive"

"""POST /DoCopy.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    dummy=38404
    orgresource=%2Fsolar2.png
    dstresource=%2FUNIST%2F
    overwrite=F
    bShareFireCopy=false

Returns:
    {
        "resultcode":0,
        "message":"success"
    }
"""
ndrive_urls['doCopy'] = base_url + "/DoCopy.ndrive"

"""POST /GetProperty.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    dummy=38404
    orgresource=FILE_PATH

Returns:
    {
        "resultcode":0,
        "message":"success"
    }
"""
ndrive_urls['getProperty'] = base_url + "/GetProperty.ndrive"

"""POST /GetVersionList.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    orgresource=FILE_PATH
    startnum=0
    pagingrow=50

Returns:
    {
        "resultcode":0,
        "message":"success",
        "resultvalue":[
            {
                "href":"FILE_PATH",
                "getlastmodified":"2014-01-26T13:11:57+09:00",
                "versioninfo":"O",
                "versionkey":32401988,
                "filesize":97656,
                "createuser":"carpedm20"
            }
        ]
    }
"""
ndrive_urls['getVersionList'] = base_url + "/GetVersionList.ndrive"

"""POST /GetVersionListCount.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    orgresource=FILE_PATH
    
Returns:
    {
        "resultcode":0,
        "message":"success",
        "resultvalue":{
            "count":1
        }
    }
"""
ndrive_urls['getVersionListCount'] = base_url + "/GetVersionListCount.ndrive"

"""POST /SetProperty.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    dummy=7046
    orgresource=FILE_PATH
    protect=Y

Returns:
    {
        "resultcode":0,
        "message":"success",
        "resultvalue":{
            "href":"FILE_PATH",
            "protect":"Y"
        }
    }
"""
ndrive_urls['setProperty'] = base_url + "/SetProperty.ndrive"

"""POST /GetMusicAlbumList.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    dummy=84125
    tagtype=0
    startnum=0
    pagingrow=100

Returns:
    {
        "resultcode":0,
        "message":"success",
        "resultvalue":null
    }
"""
ndrive_urls['getMusicAlbumList'] = base_url + "/GetMusicAlbumList.ndrive"

"""POST /DoSearch.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    dummy=46209
    sharedowner=P
        ex) P: priority files only, A: all files
    sort=update
        ex) update, date, 
    order=desc
    startnum=0
    pagingrow=100
    includeworks=Y
    type=3

    # bellow is for query search
    filename=123
    filetype=0
    dstresource=%2F
    bodysearch=N
    highlighttag=%3Cem%20style%3D%22color%3A%23019a30%22%3E%24SEARCH%3C%2Fem%3E

    #
    startdate=2014-01-13T00%3A00%3A00%2B90%3A00
    enddate=2014-01-27T23%3A59%3A59%2B09%3A00

Returns:
        {
        "resultcode":0,
        "message":"success",
        "resultvalue":[
            {
                "href":"\/OS-01장.doc",
                "owner":"carpedm20",
                "resourceno":12444576841,
                "getcontentlength":136192,
                "protect":"Y",
                "resourcetype":"property",
                "creationdate":"2014-01-16T17:24:42+09:00",
                "getlastmodified":"2014-01-16T17:24:42+09:00",
                "lastaccessed":"2014-01-16T17:24:42+09:00",
                "fileuploadstatus":"1",
                "thumbnailpath":"N",
                "shareno":0,
                "root_shareno":0,
                "sharedinfo":"F",
                "ownerid":"carpedm20",
                "owneridx":6794877,
                "owneridc":"",
                "ownership":"W",
                "root":"",
                "sharedfoldername":"",
                "subpath":"",
                "s_type":"normal",
                "copyright":"N",
                "virusstatus":"N",
                "authtoken":"",
                "filelink":"N",
                "content":"",
                "hilightfilename":"OS-01장.doc",
                "domaintype":""
            }
        ]
    }
"""
naver_urls['doSearch'] = base_url + "/DoSearch.ndrive"

"""POST /DoSearchCount.ndrive

Params:
    userid=carpedm20
    useridx=6794877
    dummy=36644
    filetype=2
    filename=
    dstresource=%2F
    sharedowner=A
    datetype=all
    searchtype=filesearch
    includeworks=Y
    bodysearch=N

Return:
    {
        "resultcode":0,
        "message":"success",
        "resultvalue":{
            "count":9883
        }
    }
"""
naver_urls['doSearchCount'] = base_url + "/DoSearchCount.ndrive"

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

import json

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

